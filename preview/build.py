#!/usr/bin/env python3
"""Preview local de la plantilla Tebex (sin cuenta de Tebex).

Renderiza los .html de la raíz con Jinja2 (casi idéntico a Twig) usando datos
de mentira, y genera una página por plantilla en preview/out/.

    pip install jinja2
    python preview/build.py          # genera preview/out/*.html
    python preview/build.py --serve  # además abre http://localhost:8000

No incluye el CSS/JS base de Tebex (tema Flat): se aproxima con Bootstrap 3 por
CDN, así que puede haber pequeñas diferencias con la tienda real.
"""
import argparse, functools, http.server, os, pathlib, re, socketserver
from jinja2 import ChainableUndefined, Environment, BaseLoader, TemplateNotFound

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path(__file__).resolve().parent / "out"

IMG = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='160'>"
       "<defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='%23ff2fd0'/>"
       "<stop offset='1' stop-color='%23a855ff'/></linearGradient></defs>"
       "<rect width='240' height='160' rx='18' fill='url(%23g)'/></svg>")
SKIN = "https://minotar.net/avatar/{}/40.png"


class Loader(BaseLoader):
    """Carga plantillas de la raíz; los includes que no existen (los de Tebex) quedan vacíos."""
    def get_source(self, env, name):
        p = ROOT / name
        if p.is_file():
            src = p.read_text(encoding="utf-8")
            src = re.sub(r"\{%-?\s*elseif\b", "{% elif", src)  # Twig -> Jinja
            src = re.sub(r"\{\{\s*([\w.]+) \? (.+?) : (.+?) \}\}", r"{{ (\2) if \1 else (\3) }}", src)  # ternario Twig
            return src, str(p), lambda: True
        if name.endswith(".html"):
            return "", name, lambda: True
        raise TemplateNotFound(name)


def money(v, *a):
    try:
        return f"{float(v):.2f}"
    except (TypeError, ValueError):
        return v


def pkg(i, name, price, **kw):
    d = dict(id=i, name=name, price=price, customPrice=False, basket=False, quantity=1, ign="",
             image=dict(url=IMG, borderless=False), discount=dict(applied=False, original=price, percentage=0),
             countdownEnds=None, currency="EUR")
    d.update(kw)
    return d


def mock():
    p1 = pkg(1, "VIP Crystal", 9.99)
    p2 = pkg(2, "Elite Rank", 19.99, discount=dict(applied=True, original=29.99, percentage=33))
    p3 = pkg(3, "Cosmetic Pack", 4.5, countdownEnds=86400 * 2)
    p4 = pkg(4, "Mythic Pet", 7.0)
    cats = [
        dict(id=1, name="Rangos", active=True, subcategories=[dict(id=11, name="VIP"), dict(id=12, name="Elite")],
             description="<p>Apoya al servidor y consigue ventajas exclusivas.</p>", displayType="grid",
             packages=[p1, p2, p3, p4]),
        dict(id=2, name="Cosméticos", active=False, subcategories=[], description="", displayType="list",
             packages=[p3, p4]),
    ]
    basket = dict(currency="EUR", username="Steve", ign="Steve", price=14.49, packages=[p1, p3], coupons=[])
    return dict(
        store=dict(name="Crystal Network", favicon="", logo="", currency="EUR", css="", useCheckout=True,
                   currencies=[dict(code=c) for c in ("EUR", "USD", "GBP")], categories=cats,
                   pages=[dict(slug="normas", title="Normas", active=False)], googleAnalytics=""),
        basket=basket, steve="Steve",
        page=dict(title="Preview", category="index", message=dict(display=False), slug="x", metaData=dict(content="<p>Contenido de la página.</p>")),
        modules="", loginform='<form><input class="form-control" placeholder="Minecraft username"><br><button class="btn btn-success btn-block">Continue</button></form>',
        delivery="", privacyForm="", params=dict(amount="", email="", ign="", txn=""), search="",
        checkout=dict(gateways=[dict(id=1, name="PayPal", gateway="paypal", image=IMG, offset=0)],
                      expiryYears=[2027, 2028], amazonpay=False, braintree=False, kount=False, playerReferrals=False),
        options=dict(package=pkg(1, "VIP Crystal", 9.99, category=1), servers=[dict(id=1, name="Survival")],
                     options=[dict(id=1, name="Extra", price=2.0)]),
        payments=[dict(ign="Steve", name="VIP Crystal", price=9.99, currency="EUR", time="hace 2h", skin=SKIN.format("Steve"),
                       order_date="2026-10-01", payment_status="completed", commands_due=0, commands_executed=2, commands_scheduled=0)],
        payment=dict(ign="Steve", name="VIP Crystal", price=9.99, currency="EUR", time="hace 2h", skin=SKIN.format("Steve"),
                     order_date="2026-10-01", payment_status="completed", commands_due=0, commands_executed=2, commands_scheduled=0),
        index=dict(description="<p>Descripción de la portada editable desde Webstore &gt; Design &gt; Homepage.</p>"),
        thanks="<p>¡Gracias por tu compra!</p>", gateway=dict(note="<p>Sigue las instrucciones de pago.</p>", scripts=""),
        category=cats[0], package=p1, coupon=dict(code="CRYSTAL10", description="10% de descuento"),
    )


def module_ctx(base, name, module):
    return dict(base, module=module)


def render_modules(env, base):
    mods = [
        ("module.featuredpackage.html", dict(display=True, package=pkg(2, "Elite Rank", 19.99, discount=dict(applied=True, original=29.99, percentage=33)))),
        ("module.topdonator.html", dict(donor=True, ign="Alex", skin=SKIN.format("Alex"), total=120, displayAmount=True, period="monthly")),
        ("module.goal.html", dict(percentage=64, displayAmount=True, bar=dict(style="striped", animated=True))),
        ("module.payments.html", dict(displayTime=True, displayPackage=True, displayPrice=True,
                                      payments=[dict(ign=n, name="VIP Crystal", price=9.99, currency="EUR", time="hace 1h", skin=SKIN.format(n)) for n in ("Steve", "Alex", "Notch", "Herobrine")])),
        ("module.serverstatus.html", dict(display=True, online=True, ip="play.crystal.net", port=25565, players=dict(online=42, max=200))),
        ("module.giftcardbalance.html", dict(header="Gift card balance")),
    ]
    html = ""
    for tpl, m in mods:
        html += env.get_template(tpl).render(**module_ctx(base, tpl, m))
    return html


PAGES = {  # archivo -> (page.category, extra)
    "index.html": ("index", {}), "category.html": ("category", {}), "checkout.html": ("checkout", {}),
    "options.html": ("options", {}), "username.html": ("username", {}), "orderstatus.html": ("orderstatus", {}),
    "complete.html": ("complete", {}), "checkout-card.html": ("checkout", {"_tpl": "checkout.html"}), "cms-page.html": ("page", {}), "instructions.html": ("instructions", {}),
}


def post(html, css):
    html = html.replace("/templates/209/css/style.min.css", "https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.4.1/css/bootstrap.min.css")
    html = html.replace("/templates/209/js/bootstrap.min.js", "https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.4.1/js/bootstrap.min.js")
    html = re.sub(r'<script src="/templates/209/js/(skin\.min|site)\.js"></script>', "", html)
    return html


def build():
    env = Environment(loader=Loader(), autoescape=False, undefined=ChainableUndefined)
    env.filters.update(raw=lambda x: x, money=money, number_format=lambda v, d=2, dp=".", ts=",": f"{float(v):,.{d}f}",
                       date=lambda v, f="": str(v))
    env.globals.update(url=lambda: '', __=lambda s, *a: s, _p=lambda s, n=1, d=None: f"{n} package" + ("s" if n != 1 else ""))
    base = mock()
    css = (ROOT / "style.css").read_text(encoding="utf-8")
    base["store"]["css"] = css
    base["modules"] = render_modules(env, base)
    OUT.mkdir(exist_ok=True)
    links = []
    for name, (cat, extra) in PAGES.items():
        extra = dict(extra); tpl = extra.pop("_tpl", name)
        ctx = dict(base, **extra)
        if name == "checkout-card.html":
            ctx["store"] = dict(base["store"], useCheckout=False)
        ctx["page"] = dict(base["page"], category=cat, title=name)
        try:
            html = env.get_template(tpl).render(**ctx)
        except Exception as e:  # una plantilla rota no debe impedir ver las demás
            html = f"<pre style='color:red'>Error renderizando {name}: {e!r}</pre>"
            print("ERROR", name, repr(e))
        (OUT / name).write_text(post(html, css), encoding="utf-8")
        links.append(name)
    items = "".join(f"<a href='{n}'>{n}</a>" for n in links)
    idx = ("<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
           "<title>Preview</title><style>body{margin:0;min-height:100vh;background:#05030c;color:#fff;font-family:Inter,system-ui,sans-serif;"
           "display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px}"
           "h1{margin:0;letter-spacing:-.02em}nav{display:grid;gap:10px;width:min(320px,90vw)}"
           "a{background:#0a0a0a;color:#fff;text-decoration:none;padding:14px 20px;border-radius:20px;font-weight:600}"
           "a:hover{background:#1a1a1a}p{opacity:.6;margin:0}</style>"
           f"<h1>Preview de la plantilla</h1><p>Elige una página</p><nav>{items}</nav>")
    (OUT / "_index.html").write_text(idx, encoding="utf-8")
    (OUT / "index_menu.html").write_text(idx, encoding="utf-8")
    print("Generado en", OUT)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--serve", action="store_true")
    ap.add_argument("--port", type=int, default=8000)
    a = ap.parse_args()
    build()
    if a.serve:
        class H(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path in ("/", ""):
                    self.path = "/index.html"
                super().do_GET()
        h = functools.partial(H, directory=str(OUT))
        with socketserver.TCPServer(("", a.port), h) as s:
            print(f"Abre http://localhost:{a.port}/  (menú: /_index.html)")
            s.serve_forever()
