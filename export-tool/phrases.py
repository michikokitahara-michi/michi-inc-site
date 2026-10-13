"""Split Japanese text into natural phrases so lines only wrap between them."""
import re

OPEN = set('「『（(〈《【［“‘')
CLOSE = set('」』）)〉》】］”’、。，．・！？!?：:；;')
PARTICLE_END = set('をはがにでとのへもやてたるすずなく')
SMALL = set('ぁぃぅぇぉっゃゅょゎァィゥェォッャュョヮヵヶーゝゞヽヾ々〜～')


def cls(ch):
    o = ord(ch)
    if ch in OPEN: return 'O'
    if ch in CLOSE: return 'C'
    if ch.isspace(): return 'S'
    if ch in SMALL: return 'X'
    if 0x3041 <= o <= 0x309F: return 'H'
    if 0x30A0 <= o <= 0x30FF or 0x31F0 <= o <= 0x31FF: return 'T'
    if 0x4E00 <= o <= 0x9FFF or 0x3400 <= o <= 0x4DBF: return 'K'
    return 'A'


def phrases(text):
    if not text: return [text]
    out, cur = [], text[0]
    depth, close_at = 0, -1
    for i in range(1, len(text) + 1):
        if i == len(text): break
        p, c = text[i - 1], text[i]
        cp, cc = cls(p), cls(c)
        if cp == 'O':
            depth += 1
        if cp == 'C' and p in '」』）)】］”':
            depth = max(0, depth - 1)
        brk = False
        if cc in ('C', 'X'):
            brk = False
        elif cp == 'S':
            brk = True
        elif cp == 'C' and cc == 'H' and p in '」』）)】］”':
            brk = False
        elif cp == 'C' and cc != 'C':
            brk = True
        elif cc == 'O' and cp != 'O':
            brk = True
        elif cp == 'H' and cc in ('K', 'T', 'A') and p in PARTICLE_END:
            brk = True
        elif cp == 'A' and cc in ('K',) and p.isdigit() is False and p.isascii():
            brk = True
        if brk and depth > 0:
            j = text.find('」', i)
            if j == -1: j = text.find('』', i)
            if j == -1: j = text.find('）', i)
            if j != -1 and j - i <= 12 and cp != 'S':
                brk = False
        if brk:
            out.append(cur); cur = c
        else:
            cur += c
    out.append(cur)
    return out


if __name__ == '__main__':
    for s in ['「どう売るか」の前に、「核となる価値」を創る。', '時代を形づくる女性リーダー100名に選出（EMPOWERMENT LEADER）',
              '優れた顧客体験を生み出すこれからのマーケティングウェイ with リテールメディア', 'お問い合わせありがとうございます。',
              'マーケターはいても「価値創造人材」は少ない？元資生堂・北原氏がたどり着いた「最高のチーム」の作り方',
              'フィリップ・コトラー『Essentials of Modern Marketing, Japan Edition』に、資生堂時代に携わった「ファンデ美容液」の事例が掲載',
              'ブランドで成長する組織をつくる', 'ART & SCIENCE マーケティング']:
        print(' | '.join(phrases(s)))
