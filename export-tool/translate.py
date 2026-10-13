"""Create translated copies of the design pages: michi/project_<lang>/ from michi/project/ using work/<lang>.json"""
import json, re, sys, os, glob, shutil
SCR = '/tmp/claude-0/-home-claude/c688d5d6-9989-53bd-beaf-fcf58ec780d4/scratchpad'
lang = sys.argv[1]
d = json.load(open(f'{SCR}/export-tool/i18n/{lang}.json', encoding='utf-8'))
src = f'{SCR}/michi/project'; dst = f'{SCR}/michi/project_{lang}'
shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst)
JP = re.compile(r'[぀-ヿ㐀-鿿！-｠]')
items = sorted(d.items(), key=lambda kv: -len(kv[0]))
left = {}
for f in glob.glob(f'{src}/*.dc.html'):
    c = open(f, encoding='utf-8').read()
    # drop the Japanese rendering of the Chanel quote (EN line already present)
    c = re.sub(r'\n<p style="margin: 16px 0 0; font-family: \'Shippori Mincho\', serif; font-size: 15px; line-height: 2; color: #444444"><span style="display: inline-block">美しさは、</span>.*?</p>', '', c)
    for ja, en in items:
        if not en and en != '': continue
        attr = en.replace('&', '&amp;').replace('&amp;amp;', '&amp;').replace('"', '&quot;')
        js = en.replace('\\', '\\\\').replace("'", "\\'")
        c = re.sub(r'>(\s*)' + re.escape(ja) + r'(\s*)<', lambda m: '>' + m.group(1) + en + m.group(2) + '<', c)
        c = c.replace('="' + ja + '"', '="' + attr + '"')
        c = c.replace("'" + ja + "'", "'" + js + "'")
    # Latin text: keep phrase groups, but move trailing spaces outside so words don't fuse; unwrap long phrases
    def fix(m):
        t = m.group(1)
        if not t.strip(): return ''
        if len(t.strip()) > 30: return t
        return '<span style="display: inline-block">' + t.rstrip() + '</span>' + (' ' if t != t.rstrip() else '')
    c = re.sub(r'<span style="display: inline-block">([^<]*)</span>', fix, c)
    body = re.sub(r'<style>.*?</style>', '', c, flags=re.S)
    rest = [m for m in re.findall(r'[^<>\'"{}\n]*[぀-ヿ㐀-鿿][^<>\'"{}\n]*', body) if JP.search(m)]
    if rest: left[os.path.basename(f)] = rest[:20]
    open(f'{dst}/{os.path.basename(f)}', 'w', encoding='utf-8').write(c)
shutil.copy(f'{src}/canvas.json', dst)
for k, v in left.items(): print('LEFT', k, v)
