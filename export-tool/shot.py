import sys
from playwright.sync_api import sync_playwright
pages=sys.argv[1].split(',')
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,vw,vh,mobile in [('m',390,844,True),('d',1440,900,False)]:
        ctx=b.new_context(viewport={'width':vw,'height':vh},device_scale_factor=1,is_mobile=mobile,has_touch=mobile,reduced_motion='reduce')
        pg=ctx.new_page()
        errs=[]
        pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
        pg.on('pageerror', lambda e: errs.append(str(e)))
        for f in pages:
            pg.goto(f'http://127.0.0.1:8765/{f}'); pg.wait_for_timeout(1500)
            pg.screenshot(path=f'shots/{name}-{f}.png', full_page=True)
            w=pg.evaluate('document.documentElement.scrollWidth')
            print(name,f,'scrollWidth',w,'errors',errs); errs.clear()
        ctx.close()
    b.close()
