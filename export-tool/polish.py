import re, glob
P='/tmp/claude-0/-home-claude/c688d5d6-9989-53bd-beaf-fcf58ec780d4/scratchpad/michi/project/'
CSS = """
/* MICHI design refinements */
header.site{position:sticky !important;top:0;z-index:40;background:rgba(255,255,255,0.94);box-shadow:0 0 0 100vmax rgba(255,255,255,0.94);clip-path:inset(0 -100vmax);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px)}
.dia{background-image:radial-gradient(circle,#D6D6D2 2.2px,transparent 2.8px),radial-gradient(circle,#D6D6D2 2.2px,transparent 2.8px);background-size:28px 28px;background-position:0 0,14px 14px}
.phead{position:relative;overflow:hidden}
.phead::before{content:"";position:absolute;top:0;right:0;width:min(48%,560px);height:100%;background-image:radial-gradient(circle,#D6D6D2 2.2px,transparent 2.8px),radial-gradient(circle,#D6D6D2 2.2px,transparent 2.8px);background-size:28px 28px;background-position:0 0,14px 14px;-webkit-mask-image:linear-gradient(to left,#000 10%,transparent 95%);mask-image:linear-gradient(to left,#000 10%,transparent 95%);pointer-events:none}
.phead>*{position:relative;z-index:1}
.cta{position:relative;overflow:hidden}
.cta::before{content:"";position:absolute;inset:0;background-image:radial-gradient(circle,#2E2E2E 2.2px,transparent 2.8px),radial-gradient(circle,#2E2E2E 2.2px,transparent 2.8px);background-size:28px 28px;background-position:0 0,14px 14px;-webkit-mask-image:radial-gradient(ellipse at center,transparent 35%,#000 85%);mask-image:radial-gradient(ellipse at center,transparent 35%,#000 85%);pointer-events:none}
.cta>*{position:relative;z-index:1}
.eyebrow{display:flex;align-items:center;gap:12px}
.eyebrow::before{content:"";width:7px;height:7px;border-radius:50%;background:currentColor;flex:none}
.eyebrow::after{content:"";width:36px;height:1px;background:currentColor;opacity:0.45;flex:none}
.eyebrow.c{justify-content:center}
.photo{position:relative}
.photo::before{content:"";position:absolute;right:-22px;bottom:-22px;width:62%;height:62%;background-image:radial-gradient(circle,#BDBDB8 2.2px,transparent 2.8px),radial-gradient(circle,#BDBDB8 2.2px,transparent 2.8px);background-size:22px 22px;background-position:0 0,11px 11px;z-index:0}
.photo img{position:relative;z-index:1}
.btn-o,.btn-f,.btn-w{transition:background-color .35s ease,color .35s ease,box-shadow .35s ease}
.btn-o:hover{background:#111111 !important;color:#FFFFFF !important}
.btn-f:hover{background:#FFFFFF !important;color:#111111 !important;box-shadow:inset 0 0 0 1px #111111}
.btn-w:hover{background:transparent !important;color:#FFFFFF !important;box-shadow:inset 0 0 0 1px #FFFFFF}
.card{transition:border-color .35s ease,box-shadow .35s ease}
.card:hover{border-color:#111111 !important;box-shadow:0 18px 40px -28px rgba(0,0,0,.45)}
.card img{transition:transform .8s cubic-bezier(.2,.7,.2,1)}
.card:hover img{transform:scale(1.025)}
.gnav a{position:relative}
@media (min-width: 961px){.gnav a:not([style*="background"])::after{content:"";position:absolute;left:50%;bottom:4px;width:5px;height:5px;border-radius:50%;background:#111111;transform:translateX(-50%) scale(0);transition:transform .3s ease}.gnav a:hover::after,.gnav a[aria-current]::after{transform:translateX(-50%) scale(1)}.gnav a[aria-current]{text-decoration:none !important}}
"""
LABEL = re.compile(r'<p style="margin: 0; font-size: 12px; font-weight: 700; letter-spacing: 0.32em; color: #(5A5A5A|B5B5B5)">')
for f in sorted(glob.glob(P+'*.dc.html')):
    s = open(f, encoding='utf-8').read()
    n = {}
    if '/* MICHI design refinements */' not in s:
        s = s.replace('</style>\n</helmet>', CSS + '</style>\n</helmet>', 1)
    s = s.replace('<header style="position: relative;', '<header class="site" style="position: relative;', 1)
    # centered eyebrows directly after a text-align:center container
    s, n['eyeC'] = re.subn(r'(text-align: center">\n)<p style="margin: 0; font-size: 12px; font-weight: 700; letter-spacing: 0.32em; color: #(5A5A5A|B5B5B5)">', r'\1<p class="eyebrow c" style="margin: 0; font-size: 12px; font-weight: 700; letter-spacing: 0.32em; color: #\2">', s)
    s, n['eye'] = LABEL.subn(lambda m: f'<p class="eyebrow" style="margin: 0; font-size: 12px; font-weight: 700; letter-spacing: 0.32em; color: #{m.group(1)}">', s)
    s, n['cta'] = re.subn(r'<section style="background: #111111; color: #F5F5F2">', '<section class="cta" style="background: #111111; color: #F5F5F2">', s)
    s, n['phead'] = re.subn(r'<section style="border-top: 1px solid #EEEEEE">', '<section class="phead" style="border-top: 1px solid #EEEEEE">', s, count=1)
    s, n['dia'] = re.subn(r'<section style="border-top: 1px solid #EEEEEE; background: radial-gradient\(circle, #DADADA 2px, transparent 2.5px\) 0 0 / 28px 28px, #FFFFFF">', '<section class="dia" style="border-top: 1px solid #EEEEEE; background-color: #FFFFFF">', s)
    s, n['works'] = re.subn(r'<section id="works" style="background: #F6F6F3">', '<section id="works" class="phead" style="background: #F6F6F3">', s)
    s, n['btn_o'] = re.subn(r'<a (href="[^"]*") style="([^"]*border: 1px solid #111111; text-decoration: none[^"]*)">', r'<a \1 class="btn-o" style="\2">', s)
    s, n['btn_f'] = re.subn(r'<a (href="[^"]*") style="([^"]*background: #111111; color: #FFFFFF; text-decoration: none[^"]*)">', r'<a \1 class="btn-f" style="\2">', s)
    s, n['btn_w'] = re.subn(r'<a (href="[^"]*") style="([^"]*background: #FFFFFF; color: #111111; text-decoration: none[^"]*)">', r'<a \1 class="btn-w" style="\2">', s)
    s, n['card_a'] = re.subn(r'<a href="\{\{a\.url\}\}" style="display: flex; flex-direction: column; border: 1px solid #DDDDD8;', '<a href="{{a.url}}" class="card" style="display: flex; flex-direction: column; border: 1px solid #DDDDD8;', s)
    s, n['card_t'] = re.subn(r'<li style="(flex: 0 0 clamp\(260px, 78vw, 340px\); scroll-snap-align: start; display: flex; flex-direction: column; border: 1px solid #DDDDD8; background: #FFFFFF)">', r'<li class="card" style="\1">', s)
    s, n['card_t2'] = re.subn(r'<li style="(display: flex; flex-direction: column; border: 1px solid #DDDDD8)">', r'<li class="card" style="\1">', s)
    s, n['photo'] = re.subn(r'<img src="/_blob/66b776f20b5c6ece3c2b63f11e857aaa" alt="北原 規稚子" style="flex: 1 1 320px; min-width: 0; max-width: (\d+)px; aspect-ratio: 1 / 1; object-fit: cover; display: block">',
        r'<div class="photo" style="flex: 1 1 320px; min-width: 0; max-width: \1px; margin: 0 22px 22px 0"><img src="/_blob/66b776f20b5c6ece3c2b63f11e857aaa" alt="北原 規稚子" style="width: 100%; aspect-ratio: 1 / 1; object-fit: cover; display: block"></div>', s)
    open(f, 'w', encoding='utf-8').write(s)
    print(f.split('/')[-1], {k: v for k, v in n.items() if v})
