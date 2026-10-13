"""Turn the design canvas pages (.dc.html) into a plain static website for GitHub Pages."""
import copy, json, os, re, shutil, subprocess, sys
from bs4 import BeautifulSoup, NavigableString, Comment, Tag
from bs4.element import Stylesheet, Script
from phrases import phrases

SCR = '/tmp/claude-0/-home-claude/c688d5d6-9989-53bd-beaf-fcf58ec780d4/scratchpad'
PROJ = f'{SCR}/michi/project'
OUT = f'{SCR}/site'
ACCESS_KEY = os.environ.get('W3F_KEY', 'YOUR_WEB3FORMS_ACCESS_KEY')

PAGES = {
    'Main.dc.html': ('index.html', 'MICHI inc. | DOTをつなぎ、未知なる道を創る'),
    'Concept.dc.html': ('concept.html', 'VISION / CONCEPT / SERVICE | MICHI inc.'),
    'About.dc.html': ('about.html', 'ABOUT CEO | MICHI inc.'),
    'Works.dc.html': ('works.html', 'WORKS | MICHI inc.'),
    'Media.dc.html': ('media.html', 'MEDIA | MICHI inc.'),
    'Talks.dc.html': ('talks.html', 'TALKS | MICHI inc.'),
    'Contact.dc.html': ('contact.html', 'CONTACT | MICHI inc.'),
    'Company.dc.html': ('company.html', '会社概要 | MICHI inc.'),
    'Privacy.dc.html': ('privacy.html', 'プライバシーポリシー | MICHI inc.'),
}
DESC = 'MICHI inc.（株式会社MICHI）は、成長しようとする人や企業、地域の点をつなぎ、ブランドの創造・体験設計・組織づくりに伴走するブランドクリエイションスタジオです。代表取締役CEO 北原規稚子。'

PAGE_DESC = {
    'index.html': DESC,
    'concept.html': '「DOTをつなぎ、未知なる道を創る」MICHI inc.のビジョンと、「どう売るか」の前に「核となる価値」を創るコンセプト、ブランドを創る・ブランド体験を届ける・ブランドで成長する組織を育てる3つのサービスをご紹介します。',
    'about.html': '株式会社MICHI 代表取締役CEO 北原規稚子のプロフィール。ライオン、資生堂でブランドづくりを手がけ、資生堂では副CMO・マーケティング本部長などを歴任。2025年にMICHI inc.を設立。社外取締役や講師としても活動しています。',
    'works.html': 'MICHI inc.（株式会社MICHI）のブランディング・マーケティング支援、講演などの実績一覧です。',
    'media.html': 'MICHI inc. 代表取締役CEO 北原規稚子のメディア掲載・出演（記事、インタビュー、テレビ、動画など）の一覧です。',
    'talks.html': '北原規稚子（MICHI inc. 代表取締役CEO）の登壇・講演・出演情報。ad:tech tokyo、日経クロストレンドフォーラム、MarkeZine Dayなど。',
    'contact.html': 'ブランディング・マーケティング支援、講演・研修・ワークショップのご依頼など、MICHI inc.へのお問い合わせはこちらから。',
    'company.html': '株式会社MICHI（MICHI inc.）の会社概要。代表者、設立、所在地（東京都港区北青山）、事業内容をご案内します。',
    'privacy.html': '株式会社MICHI（MICHI inc.）のプライバシーポリシー（個人情報の取り扱いについて）。',
}

ORG_LD = {
    "@context": "https://schema.org", "@type": "Organization", "@id": "https://michi-inc.net/#org",
    "name": "株式会社MICHI", "alternateName": ["MICHI inc.", "MICHI"], "url": "https://michi-inc.net/",
    "logo": "https://michi-inc.net/assets/michi-inc-black.png", "foundingDate": "2025-01-23",
    "description": DESC,
    "telephone": "+81-3-6681-0234",
    "address": {"@type": "PostalAddress", "postalCode": "107-0061", "addressRegion": "東京都", "addressLocality": "港区", "streetAddress": "北青山一丁目3番1号 アールキューブ青山3階", "addressCountry": "JP"},
    "founder": {"@id": "https://michi-inc.net/about.html#person"},
}
PERSON_LD = {
    "@context": "https://schema.org", "@type": "Person", "@id": "https://michi-inc.net/about.html#person",
    "name": "北原規稚子", "alternateName": "Michiko Kitahara", "jobTitle": "代表取締役CEO",
    "worksFor": {"@id": "https://michi-inc.net/#org"}, "url": "https://michi-inc.net/about.html",
    "image": "https://michi-inc.net/assets/ceo.jpg",
    "sameAs": ["https://www.facebook.com/share/1BNkp1RXkc/"],
}

BLOBS = {
    'db8e8414d2caf95087d5662d0046ac87': 'visuals/jlive.jpg',
    '97fab58dca688becf6e2b35a3444cda9': 'visuals/anotheraddress.jpg',
    '07e38e2e01125b1d27e8f7ce62675b84': 'visuals/toppa-online.jpg',
    '1ba04541731568ec8cb997f80fa0d246': 'visuals/heart.jpg',
    'f38d5ea2a419011ec336bd5c2f1bdbcc': 'visuals/hands.jpg',
    '3a1fddf7981de7dbca9cd18baf992697': 'visuals/brand-identity.jpg',
    'b7ce03e0a46804408bca2e656f8a7b0f': 'visuals/score.jpg',
    'faf6f00bfbb2924255927d37e13d8d8d': 'visuals/runway.jpg',
    'a3f953cc88cea4569e80e7f53477fc69': 'visuals/branding.jpg',
    '6c668ebc530493ccb12e3b8dc4816ce9': 'visuals/newspaper.jpg',
    'f2411ec82daefc924bc15fd7d2af4be0': 'visuals/art-science.jpg',
    '558ca2295c762d1d1240c0e936cf2b64': 'visuals/cosmetics.jpg',
    'c05f7508756b3e7486b74868b50adb64': 'visuals/thinking.jpg',
    'e24775b609882eb7317bf26902b06113': 'visuals/skincare.jpg',
    '404a83901f49b3f231f10536e1263f9a': 'logos/michi-inc-black.png',
    '5a70e1ab78d97b163da96e4084e2b1d6': 'logos/michi-inc-white.png',
    '795af6e51ea3de31c592170cf54f4265': 'logos/michi-frame-black.png',
    '0c24335e46dd9e3d3258a0ed9efc96cc': 'logos/michi-frame-white.png',
    '41d25df8cdd472315052b9a7f4f68278': 'logos/michi-white-noframe.png',
    '66b776f20b5c6ece3c2b63f11e857aaa': 'logos/ceo.jpg',
    '3b112f729e1fc247e25ba9968dafde69': 'midot/midot-visual.jpg',
    '7151b594c12ef93b40c9e6d1bb2498b7': 'midot/midot-logo-black.png',
    '5e950c32ae527de545a7889d0b4e38ba': 'talks/mx2025.jpg',
    '03d1ad185428140d490307000d07d45d': 'talks/cmojapan.jpg',
    'deffdf827b2822f99c8aed24c372bc50': 'talks/touji.jpg',
    '49cc742bf816a03c40a1a9b1e1efeb56': 'talks/msworld.jpg',
    '0b678d7212e4a0a95d1b946e84e2fd04': 'talks/brandsummit.jpg',
    '8827d70a88b2410aa16ce18930d2b047': 'talks/retailmedia.jpg',
    'bdda47c35b1ba8d68572a53517a64289': 'talks/book.jpg',
    '4038b920bdf4c10401b90046867ebef4': 'talks/adtech2025.jpg',
    'd7ead871af5f7e1ff4e5c95329574b53': 'talks/ficc.jpg',
    '9e3b764f374ec39d35c984ef66b1375e': 'talks/interfm.jpg',
    'b311ef81665a3d4fee5f72316fef1261': 'talks/adtai.jpg',
    '6ca027182dea328efc012bbd1db9ecdc': 'talks/shosa.jpg',
    'd92213428901d134bdc6952e8f614f02': 'talks/reframe.jpg',
    '634b54562aa19fa59f077f2f0f50b05e': 'talks/midot-expo.jpg',
    '2e94fba1e71e46f7b4fef185b865bbc0': 'talks/interview.jpg',
    '8ffa9796beabf0775f6874b36c7fa92d': 'talks/core.jpg',
    'd127536e95e42b813b2ca66a13259185': 'talks/toppa.jpg',
    '573c0f3a1c7d70a52e2c4d880ab4884c': 'talks/reframe12.jpg',
    '911dec9859ec1ade6b408c7de5832043': 'talks/xtrend.jpg',
    '29eae3d2553628237fd8b44d0e88daed': 'talks/markezineday.jpg',
    'cca76d39c269df2aaf85aabf46716252': 'talks/adtech2026.jpg',
    '54e587d62b2bbe59e9a420e9349a0284': 'talks/innerbeauty.jpg',
    '2d5189aa6e2c8ef3380b4d7135f338cf': 'talks/shopperx.jpg',
    '21e36d0212dcc6a0f52d639e017b9471': 'talks/adtech2026b.jpg',
    '336d82074d465c5a376dd3990eca51ab': 'talks/rms2026.jpg',
    '6db1601405f9facaa33b9dd0f7bac055': 'talks/atami.jpg',
    'fdf892390333d05111564fe10f803ca9': 'talks/kotler.jpg',
    '410a64372e34d2576574cf46481e1eb2': 'talks/brandsummit2.jpg',
    '2f6cc41ec4891c92f741e4a0274dc001': 'talks/msworld2.jpg',
    'b84b73ef0497e2ee967eabaa282b0c14': 'talks/xtrend2.jpg',
    '9b8e39345e7ab7a0657592bbae89dbe1': 'talks/rms2026b.jpg',
    '518422eafe1ecdb6cc840ecf8a75383b': 'talks/innerbeauty2.jpg',
    '3dd3793eea78dafa0807abedabf9af13': 'talks/adtai2.jpg',
    '6b9b94fec0eb67a35e9cb062ed23debc': 'talks/core-banner.jpg',
}

HOLE = re.compile(r'\{\{\s*([^}]+?)\s*\}\}')


def lookup(path, scope):
    path = path.strip()
    if path == 'true': return True
    if path == 'false': return False
    if re.fullmatch(r'-?\d+(\.\d+)?', path): return float(path) if '.' in path else int(path)
    cur = scope
    for part in path.split('.'):
        if isinstance(cur, dict) and part in cur: cur = cur[part]
        elif isinstance(cur, list) and part.isdigit(): cur = cur[int(part)]
        else: return None
    return cur


def to_text(v):
    if v is None: return ''
    if v is True: return 'true'
    if v is False: return 'false'
    return str(v)


def interp(s, scope):
    return HOLE.sub(lambda m: to_text(lookup(m.group(1), scope)), s)


def render_children(parent, scope):
    for node in list(parent.contents):
        if isinstance(node, (Comment,)):
            node.extract(); continue
        if isinstance(node, (Stylesheet, Script)):
            continue
        if isinstance(node, NavigableString):
            if '{{' in node:
                node.replace_with(interp(str(node), scope))
            continue
        if not isinstance(node, Tag):
            continue
        if node.name == 'sc-for':
            m = HOLE.fullmatch(node.get('list', '').strip())
            items = lookup(m.group(1), scope) if m else []
            as_ = node.get('as', 'item')
            for i, item in enumerate(items or []):
                wrap = Tag(name='div')
                for ch in node.contents: wrap.append(copy.copy(ch))
                render_children(wrap, {**scope, as_: item, '$index': i})
                for ch in list(wrap.contents): node.insert_before(ch.extract())
            node.decompose(); continue
        if node.name == 'sc-if':
            m = HOLE.fullmatch(node.get('value', '').strip())
            cond = lookup(m.group(1), scope) if m else False
            if cond:
                wrap = Tag(name='div')
                for ch in node.contents: wrap.append(copy.copy(ch))
                render_children(wrap, scope)
                for ch in list(wrap.contents): node.insert_before(ch.extract())
            node.decompose(); continue
        for attr in list(node.attrs):
            val = node.attrs[attr]
            if attr.startswith('on') or attr.startswith('hint-'):
                del node.attrs[attr]; continue
            if isinstance(val, list):
                val = ' '.join(val)
            if isinstance(val, str) and '{{' in val:
                v = interp(val, scope).strip() if attr == 'class' else interp(val, scope)
                node.attrs[attr] = v
        render_children(node, scope)


JP = re.compile(r'[\u3040-\u30ff\u4e00-\u9fff]')


def wrap_phrases(root):
    """Keep Japanese phrases together so short lines only wrap between natural phrases."""
    for node in list(root.find_all(string=True)):
        if isinstance(node, (Comment, Stylesheet, Script)):
            continue
        txt = str(node)
        core = txt.strip()
        if len(core) < 6 or len(core) > 130 or not JP.search(core):
            continue
        skip = False
        for anc in node.parents:
            if not isinstance(anc, Tag): continue
            if anc.name in ('script', 'style', 'title', 'textarea', 'option', 'head', 'button'):
                skip = True; break
            cls_ = anc.get('class') or []
            if 'ph' in cls_ or 'w' in cls_ or 'nb' in cls_ or 'chip' in cls_:
                skip = True; break
            if 'inline-block' in (anc.get('style') or '') and anc.name == 'span':
                skip = True; break
        if skip: continue
        display = False
        for anc in node.parents:
            if not isinstance(anc, Tag): continue
            st = anc.get('style') or ''
            if anc.name in ('h1', 'h2', 'h3', 'legend') or 'Shippori Mincho' in st or 'font-weight: 500' in st or 'font-weight: 700' in st:
                display = True; break
            if anc.name in ('p', 'li', 'div', 'section'):
                break
        if not display and len(core) > 40:
            continue
        parts = phrases(txt)
        if len(parts) >= 2 and len(parts[-1].strip()) <= 3:
            parts[-2:] = [parts[-2] + parts[-1]]
        if len(parts) < 2 and len(core) > 24: continue
        frag = BeautifulSoup('', 'html.parser')
        outer = frag.new_tag('span')
        for p in parts:
            core_p = p.rstrip()
            lead = p[:len(p) - len(p.lstrip())]
            if lead: outer.append(NavigableString(lead))
            sp = frag.new_tag('span', attrs={'class': 'w'})
            sp.string = core_p.lstrip()
            outer.append(sp)
            if core_p != p: outer.append(NavigableString(' '))
        node.replace_with(outer)


def vals(path, state=None):
    out = subprocess.run(['node', f'{SCR}/export-tool/vals.js', path, json.dumps(state or {})], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def page_links(html):
    for src, (dst, _) in PAGES.items():
        d = './' if dst == 'index.html' else dst
        html = html.replace(f'href="{src}#', f'href="{d}#').replace(f'href="{src}"', f'href="{d}"')
    return html


EXT_ICON = '<svg class="ext-ic" aria-hidden="true" viewBox="0 0 12 12" width="0.85em" height="0.85em" style="display:inline-block;vertical-align:-0.06em;margin-left:0.45em;flex:none" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"><path d="M7 1.5h3.5V5"/><path d="M10.5 1.5 5.5 6.5"/><path d="M9 7.5v2.25a.75.75 0 0 1-.75.75h-6a.75.75 0 0 1-.75-.75v-6A.75.75 0 0 1 2.25 3H4.5"/></svg><span style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap">（新しいタブで開きます）</span>'


def external_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    for a in soup.find_all('a', href=True):
        h = a['href']
        if not h.startswith('http') or 'michi-inc.net' in h:
            continue
        a['target'] = '_blank'
        a['rel'] = 'noopener noreferrer'
        done = False
        for t in a.find_all(string=True):
            if t.strip().endswith('→'):
                t.replace_with(t.rstrip().rstrip('→').rstrip())
                parent = t.parent if t.parent else a
                done = 'pending'
        # place icon after the arrow-label element (or at end of the anchor)
        target = None
        for el in a.find_all(True):
            if el.string is not None and el.string.strip() and el.string.strip() in ('READ', 'DETAIL'):
                target = el
        if target is None:
            for t in a.find_all(string=True):
                if t.strip() in ('READ', 'DETAIL'):
                    target = t
        frag = BeautifulSoup(EXT_ICON, 'html.parser')
        if target is not None and hasattr(target, 'append'):
            target.append(frag)
        elif target is not None:
            target.insert_after(frag)
        else:
            a.append(frag)
    return str(soup)


USED = set()


def map_blobs(html):
    def rep(m):
        bid = m.group(1)
        if bid not in BLOBS: raise SystemExit(f'unknown asset {bid}')
        USED.add(bid)
        return 'assets/' + os.path.basename(BLOBS[bid])
    return re.sub(r'/_blob/([0-9a-f]{32})', rep, html)


NAV_JS = """<script>
(function(){
  var b=document.querySelector('.mbtn'),n=document.querySelector('.gnav');if(!b||!n)return;
  var ham=b.innerHTML,x='<svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="5" y1="5" x2="19" y2="19"></line><line x1="19" y1="5" x2="5" y2="19"></line></svg>';
  b.addEventListener('click',function(){var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');b.innerHTML=o?x:ham;});
  n.addEventListener('click',function(e){if(e.target.closest('a')&&n.classList.contains('open')){n.classList.remove('open');b.setAttribute('aria-expanded','false');b.innerHTML=ham;}});
})();
</script>"""

ACC_JS = """<script>
(function(){
  var ids=['vision','concept','service'];
  function show(t,scroll){
    if(ids.indexOf(t)<0)return;
    ids.forEach(function(i){var d=document.getElementById(i);if(d)d.open=(i===t);});
    if(scroll){var el=document.getElementById(t);setTimeout(function(){el.scrollIntoView({block:'start'});},30);}
  }
  var h=location.hash.slice(1);if(h)show(h,true);
  window.addEventListener('hashchange',function(){show(location.hash.slice(1),true);});
  document.addEventListener('click',function(e){
    var a=e.target.closest('a[href]');if(!a)return;
    var m=a.getAttribute('href').match(/^(?:concept\.html)?#(vision|concept|service)$/);
    if(!m&&a.getAttribute('href')==='concept.html')m=[0,'vision'];
    if(!m)return;
    e.preventDefault();history.replaceState(null,'','#'+m[1]);show(m[1],true);
  });
})();
</script>"""

FORM_JS = """<script>
(function(){
  var f=document.getElementById('contact-form'),done=document.getElementById('contact-done'),err=document.getElementById('contact-error');if(!f)return;
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var btn=f.querySelector('button[type=submit]');btn.disabled=true;btn.textContent='送信中…';err.hidden=true;
    fetch('https://api.web3forms.com/submit',{method:'POST',headers:{'Accept':'application/json'},body:new FormData(f)})
      .then(function(r){return r.json();})
      .then(function(d){if(!d.success)throw new Error(d.message||'error');f.hidden=true;done.hidden=false;done.scrollIntoView({behavior:'smooth',block:'center'});})
      .catch(function(){err.hidden=false;btn.disabled=false;btn.textContent='送信する';});
  });
})();
</script>"""

REVEAL_JS = """<script>
(function(){
  if(!('IntersectionObserver' in window)||window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  var els=[].slice.call(document.querySelectorAll('main section, body > div > section')).slice(1);
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
  els.forEach(function(el){el.classList.add('rv');io.observe(el);});
})();
</script>"""

FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" fill="#fff"/><line x1="8" y1="22" x2="24" y2="10" stroke="#111" stroke-width="2"/><circle cx="8" cy="22" r="5" fill="#111"/><circle cx="24" cy="10" r="5" fill="#111"/></svg>'


def build(src, dst, title):
    _ld = []
    if dst in ('index.html', 'company.html'): _ld.append(ORG_LD)
    if dst == 'about.html': _ld.append(PERSON_LD)
    LD = ''.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + '</script>\n' for x in _ld)
    path = f'{PROJ}/{src}'
    raw = open(path, encoding='utf-8').read()
    soup = BeautifulSoup(raw, 'html.parser')
    xdc = soup.find('x-dc')
    helmet = xdc.find('helmet').extract()
    scope = vals(path)
    render_children(xdc, scope)
    wrap_phrases(xdc)
    head_extra = ''.join(str(c) for c in helmet.contents if isinstance(c, Tag))
    body = ''.join(str(c) for c in xdc.contents)

    extra_js = NAV_JS + REVEAL_JS
    if src == 'Contact.dc.html':
        sent_soup = BeautifulSoup(raw, 'html.parser')
        sx = sent_soup.find('x-dc'); sx.find('helmet').extract()
        render_children(sx, vals(path, {'sent': True}))
        wrap_phrases(sx)
        status = sx.find(attrs={'role': 'status'})
        status['id'] = 'contact-done'; status['hidden'] = ''
        b2 = BeautifulSoup(body, 'html.parser')
        form = b2.find('form')
        form['id'] = 'contact-form'
        form['action'] = 'https://api.web3forms.com/submit'
        form['method'] = 'POST'
        form.find('input', attrs={'name': 'access_key'})['value'] = ACCESS_KEY
        err = BeautifulSoup('<p id="contact-error" role="alert" hidden style="margin: 0; padding: 14px 16px; border: 1px solid #111111; font-size: 14px">送信できませんでした。時間をおいて再度お試しいただくか、michiko.kitahara@michi-inc.com まで直接ご連絡ください。</p>', 'html.parser')
        form.find('button', attrs={'type': 'submit'}).parent.insert_before(err)
        form.insert_after(copy.copy(status))
        body = str(b2)
        extra_js += FORM_JS

    if dst == 'concept.html':
        extra_js += ACC_JS

    html = f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{PAGE_DESC[dst]}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{PAGE_DESC[dst]}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://michi-inc.net/assets/ogp.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="https://michi-inc.net/{'' if dst=='index.html' else dst}">
<meta property="og:site_name" content="MICHI inc.">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="assets/icon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="assets/icon-180.png">
<link rel="manifest" href="site.webmanifest">
<meta name="apple-mobile-web-app-title" content="MICHI inc.">
<meta name="theme-color" content="#111111">
{LD}<link rel="canonical" href="https://michi-inc.net/{'' if dst=='index.html' else dst}">
<script>if(/\/index\.html$/.test(location.pathname))history.replaceState(null,'',location.pathname.replace(/index\.html$/,'')+location.search+location.hash)</script>
{head_extra}
<style>.w{{display:inline-block}}body{{line-break:strict}}.rv{{opacity:0;transform:translateY(28px);transition:opacity 1s ease,transform 1s cubic-bezier(.2,.7,.2,1)}}.rv.in{{opacity:1;transform:none}}</style>
</head>
<body>
{body}
{extra_js}
</body>
</html>
"""
    html = page_links(map_blobs(html))
    leftover = HOLE.findall(html)
    if leftover: raise SystemExit(f'{src}: unresolved holes {leftover[:5]}')
    if '.dc.html' in html: raise SystemExit(f'{src}: leftover .dc.html link')
    if re.search(r'<sc-(for|if)', html): raise SystemExit(f'{src}: leftover sc- tag')
    html = external_links(html)
    open(f'{OUT}/{dst}', 'w', encoding='utf-8').write(html)
    return len(html)


if __name__ == '__main__':
    if os.path.exists(OUT):
        for n in os.listdir(OUT):
            if n == '.git': continue
            p = f'{OUT}/{n}'
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    os.makedirs(f'{OUT}/assets', exist_ok=True)
    for src, (dst, title) in PAGES.items():
        print(dst, build(src, dst, title))
    for bid in sorted(USED):
        shutil.copy(f'{SCR}/{BLOBS[bid]}', f'{OUT}/assets/{os.path.basename(BLOBS[bid])}')
    shutil.copy(f'{SCR}/logos/ceo.jpg', f'{OUT}/assets/ceo.jpg')
    open(f'{OUT}/assets/favicon.svg', 'w').write(FAVICON)
    shutil.copy(f'{SCR}/visuals/ogp.jpg', f'{OUT}/assets/ogp.jpg')
    for _s in (32, 180, 192, 512): shutil.copy(f'{SCR}/visuals/icon-{_s}.png', f'{OUT}/assets/icon-{_s}.png')
    open(f'{OUT}/site.webmanifest', 'w').write('{"name":"MICHI inc.","short_name":"MICHI inc.","start_url":"/","display":"standalone","background_color":"#111111","theme_color":"#111111","icons":[{"src":"/assets/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"/assets/icon-512.png","sizes":"512x512","type":"image/png"}]}')
    open(f'{OUT}/.nojekyll', 'w').write('')
    REDIRECTS = {'concept': 'concept.html', 'about-ceo': 'about.html', 'news': 'media.html', 'works': 'works.html', 'voices': 'index.html', 'contact': 'contact.html', '概要': 'company.html', 'プライバシーポリシー': 'privacy.html', 'cookie-設定': 'privacy.html'}
    for d, target in REDIRECTS.items():
        os.makedirs(f'{OUT}/{d}', exist_ok=True)
        open(f'{OUT}/{d}/index.html', 'w', encoding='utf-8').write(f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=../{target}"><link rel="canonical" href="../{target}"><title>MICHI inc.</title></head><body><a href="../{target}">MICHI inc.</a></body></html>')
    import datetime
    today = datetime.date.today().isoformat()
    urls = ''.join(f'<url><loc>https://michi-inc.net/{"" if d == "index.html" else d}</loc><lastmod>{today}</lastmod></url>' for d, _ in PAGES.values())
    open(f'{OUT}/sitemap.xml', 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    open(f'{OUT}/robots.txt', 'w').write('User-agent: *\nAllow: /\n\nSitemap: https://michi-inc.net/sitemap.xml\n')
    shutil.copy(f'{SCR}/export-tool/llms.txt', f'{OUT}/llms.txt')
    print('assets', len(os.listdir(f'{OUT}/assets')))
