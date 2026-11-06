#!/usr/bin/env python3
"""archkit — bộ đồ nghề vẽ bản vẽ kiến trúc hệ thống bằng SVG dựng tay (diagrams as code).

Dùng cho skill /tool-diagram v2. Copy file này vào cạnh script dựng sơ đồ của dự án rồi `from archkit import *`.

Có gì:
  Svg        — khung vẽ: box / person / cyl / boundary / arrow / badge / legend
  seq()      — sequence diagram từ danh sách bước
  catalog()  — bảng danh mục giao tiếp (HTML)
  page()     — bọc thành trang HTML có khung tên bản vẽ

Quy ước màu (KIND) = ai sở hữu thành phần, KHÔNG phải tầng kỹ thuật:
  build  = tự xây        module = thành phần bên trong hệ tự xây
  saas   = mua / SaaS    ext    = bên thứ ba
  person = người dùng    gap    = chưa đặc tả / ngoài phạm vi (nét đứt đỏ)
Kiểu mũi tên (style):
  sync = gọi đồng bộ · async = sự kiện / webhook · manual = thủ công · use = người dùng sử dụng
  ret  = kết quả trả về (sequence) · gap = chưa đặc tả
"""
import html

E = html.escape

INK = '#0f172a'
MUT = '#475569'
LINE = '#334155'
RED = '#DC2626'
KIND = {
    'build': ('#EEF2FF', '#4338CA'),   # tự xây
    'module': ('#FFFFFF', '#6366F1'),  # thành phần bên trong engine
    'saas': ('#ECFDF5', '#047857'),    # mua / SaaS, mình vận hành
    'ext': ('#F1F5F9', '#64748B'),     # bên thứ ba
    'person': ('#FFFBEB', '#B45309'),  # người dùng
    'gap': ('#FEF2F2', RED),           # chưa đặc tả / ngoài phạm vi
}
SANS = "'Inter',system-ui,-apple-system,sans-serif"
MONO = "'JetBrains Mono',ui-monospace,Menlo,monospace"


class Svg:
    def __init__(self, w, h):
        self.w, self.h, self.o = w, h, []

    def add(self, s):
        self.o.append(s)

    def text(self, x, y, lines, size=11, weight=400, fill=INK, anchor='start',
             mono=False, halo=False, lh=None, italic=False):
        if isinstance(lines, str):
            lines = [lines]
        lh = lh or round(size * 1.3, 1)
        fam = MONO if mono else SANS
        st = ' style="paint-order:stroke;stroke:#fff;stroke-width:4px;stroke-linejoin:round"' if halo else ''
        it = ' font-style="italic"' if italic else ''
        out = '<text x="%s" y="%s" font-family="%s" font-size="%s" font-weight="%s" fill="%s" text-anchor="%s"%s%s>' % (
            x, y, fam, size, weight, fill, anchor, it, st)
        for i, ln in enumerate(lines):
            out += '<tspan x="%s" dy="%s">%s</tspan>' % (x, 0 if i == 0 else lh, E(ln) if ln else '&#160;')
        self.add(out + '</text>')

    def rect(self, x, y, w, h, fill, stroke, rx=6, dash=None, sw=1.3):
        da = ' stroke-dasharray="%s"' % dash if dash else ''
        self.add('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (
            x, y, w, h, rx, fill, stroke, sw, da))

    def box(self, x, y, w, h, title, tech=None, desc=(), kind='build', center=False,
            tsize=12.5, dsize=10.5, pad=10):
        f, st = KIND[kind]
        self.rect(x, y, w, h, f, st, dash='5 4' if kind == 'gap' else None)
        tx = x + w / 2 if center else x + pad
        an = 'middle' if center else 'start'
        tl = [title] if isinstance(title, str) else list(title)
        ty = y + 6 + tsize
        self.text(tx, ty, tl, size=tsize, weight=700, anchor=an, lh=round(tsize * 1.2, 1))
        ty += round(tsize * 1.2, 1) * (len(tl) - 1)
        if tech:
            ty += 13
            self.text(tx, ty, '[' + tech + ']', size=9.3, fill=MUT, anchor=an, mono=True)
        if desc:
            ty += dsize + 5
            self.text(tx, ty, list(desc), size=dsize, fill='#334155', anchor=an, lh=round(dsize * 1.32, 1))

    def person(self, x, y, w, h, title, sub=None, kind='person'):
        f, st = KIND[kind]
        self.rect(x, y, w, h, f, st, rx=10)
        cx, cy = x + 17, y + h / 2
        self.add('<circle cx="%s" cy="%s" r="5.2" fill="none" stroke="%s" stroke-width="1.4"/>' % (cx, cy - 8, st))
        self.add('<path d="M%s %s q0 -10 9 -10 q9 0 9 10" fill="none" stroke="%s" stroke-width="1.4"/>' % (
            cx - 9, cy + 11, st))
        tl = [title] if isinstance(title, str) else list(title)
        n = len(tl) + (1 if sub else 0)
        ty = y + h / 2 - (n - 1) * 7 + 4
        self.text(x + 34, ty, tl, size=11.5, weight=700, lh=14)
        if sub:
            self.text(x + 34, ty + 14 * len(tl), sub, size=9.5, fill=MUT)

    def cyl(self, x, y, w, h, title, tech=None, desc=(), kind='build'):
        f, st = KIND[kind]
        ry = 9
        self.add('<path d="M%s %s v%s a%s %s 0 0 0 %s 0 v-%s" fill="%s" stroke="%s" stroke-width="1.3"/>' % (
            x, y + ry, h - 2 * ry, w / 2, ry, w, h - 2 * ry, f, st))
        self.add('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" stroke="%s" stroke-width="1.3"/>' % (
            x + w / 2, y + ry, w / 2, ry, f, st))
        ty = y + 2 * ry + 16
        self.text(x + 12, ty, title, size=12.5, weight=700)
        if tech:
            ty += 13
            self.text(x + 12, ty, '[' + tech + ']', size=9.3, fill=MUT, mono=True)
        if desc:
            ty += 15
            self.text(x + 12, ty, list(desc), size=10.5, fill='#334155', lh=13.8)

    def boundary(self, x, y, w, h, label, color='#64748B', fill='none', bottom=False):
        self.rect(x, y, w, h, fill, color, rx=10, dash='7 5', sw=1.2)
        ly = y + h - 8 if bottom else y + 15
        self.text(x + 12, ly, label.upper(), size=9.8, weight=700, fill=color)

    def arrow(self, pts, style='sync', label=None, lpos=None, lanchor='middle', num=None, npos=None,
              lsize=10):
        d = 'M' + ' L'.join('%s %s' % (p[0], p[1]) for p in pts)
        dash = {'sync': '', 'async': ' stroke-dasharray="6 4"', 'manual': ' stroke-dasharray="2 4"',
                'gap': ' stroke-dasharray="6 4"', 'use': '', 'ret': ' stroke-dasharray="6 4"'}[style]
        col = {'gap': RED, 'use': '#94A3B8'}.get(style, LINE)
        mk = {'gap': 'ah-red', 'use': 'ah-grey', 'ret': 'ah-open'}.get(style, 'ah')
        wd = 1.15 if style == 'use' else 1.5
        self.add('<path d="%s" fill="none" stroke="%s" stroke-width="%s"%s marker-end="url(#%s)"/>' % (
            d, col, wd, dash, mk))
        if label and lpos:
            self.text(lpos[0], lpos[1], label, size=lsize, fill=RED if style == 'gap' else '#1e293b',
                      anchor=lanchor, halo=True, lh=round(lsize * 1.25, 1))
        if num is not None and npos:
            self.badge(npos[0], npos[1], num)

    def badge(self, x, y, num, fill=INK):
        self.add('<circle cx="%s" cy="%s" r="8.5" fill="%s" stroke="#fff" stroke-width="1.5"/>' % (x, y, fill))
        self.text(x, y + 3.2, str(num), size=9, weight=700, fill='#fff', anchor='middle')

    def dot(self, x, y):
        self.add('<circle cx="%s" cy="%s" r="2.6" fill="%s"/>' % (x, y, LINE))

    def line(self, x1, y1, x2, y2, color='#CBD5E1', dash=None, sw=1):
        da = ' stroke-dasharray="%s"' % dash if dash else ''
        self.add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s/>' % (
            x1, y1, x2, y2, color, sw, da))

    def legend(self, x, y, w, kinds=None, styles=None, badge=True):
        """Khung chú giải cao 84px. kinds: [(kind, nhãn)], styles: [(style, nhãn)]."""
        kinds = kinds or [('person', 'Người dùng'), ('build', 'Tự xây'), ('saas', 'Mua / SaaS'),
                          ('ext', 'Bên thứ ba'), ('gap', 'Chưa đặc tả')]
        styles = styles or [('sync', 'gọi đồng bộ (API)'), ('async', 'sự kiện / webhook'),
                            ('manual', 'thủ công'), ('use', 'sử dụng'), ('gap', 'chưa đặc tả')]
        self.rect(x, y, w, 84, '#fff', '#CBD5E1', rx=8)
        self.text(x + 14, y + 16, 'CHÚ GIẢI', size=9.8, weight=700, fill=MUT)
        lx = x + 14
        for k, lbl in kinds:
            f, st = KIND[k]
            self.rect(lx, y + 26, 16, 12, f, st, rx=3, dash='4 3' if k == 'gap' else None)
            self.text(lx + 22, y + 36, lbl, size=10.2)
            lx += 34 + len(lbl) * 6.2
        if badge:
            self.badge(lx + 14, y + 32, 7)
            self.text(lx + 27, y + 36, 'số giao tiếp', size=10.2)
        ax = x + 14
        for stl, lbl in styles:
            self.arrow([(ax, y + 62), (ax + 30, y + 62)], style=stl)
            self.text(ax + 36, y + 65.5, lbl, size=10.2)
            ax += 36 + len(lbl) * 6.0 + 16

    def render(self):
        defs = '''<defs>
<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7.5" markerHeight="7.5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="%s"/></marker>
<marker id="ah-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7.5" markerHeight="7.5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="%s"/></marker>
<marker id="ah-grey" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#94A3B8"/></marker>
<marker id="ah-open" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10" fill="none" stroke="%s" stroke-width="1.6"/></marker>
</defs>''' % (LINE, RED, LINE)
        return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s" role="img">%s%s</svg>' % (
            self.w, self.h, defs, ''.join(self.o))


# ───────────────────────── SEQUENCE DIAGRAM ─────────────────────────
def wrap2(text, maxw, cw=5.6):
    """Ngắt nhãn thành 2 dòng khi dài hơn khoảng giữa hai lifeline."""
    if len(text) * cw <= maxw or ' ' not in text:
        return [text]
    mid = len(text) // 2
    cands = [i for i, c in enumerate(text) if c == ' ']
    cut = min(cands, key=lambda i: abs(i - mid))
    return [text[:cut], text[cut + 1:]]


def seq(parts, items, width=1790, pw=160):
    """parts: [(key, title, tech, kind, x)] · items: list of tuples
    ('frame', label) · ('end',) · ('m', a, b, text, style) · ('self', a, text) · ('note', a, b, text)"""
    xs = {p[0]: p[4] for p in parts}
    # tính chiều cao
    y = 86
    plan = []
    num = 0
    frames = []
    stack = []
    for it in items:
        if it[0] == 'frame':
            y += 14
            stack.append([it[1], y, None, it[2] if len(it) > 2 else '#64748B'])
            y += 52
        elif it[0] == 'end':
            fr = stack.pop()
            fr[2] = y + 4
            frames.append(fr)
            y += 16
        elif it[0] == 'm':
            num += 1
            lines = it[3] if isinstance(it[3], list) else wrap2(it[3], abs(xs[it[2]] - xs[it[1]]) - 36)
            y += 12 * (len(lines) - 1)
            plan.append(('m', it[1], it[2], lines, it[4], y, num))
            y += 36
        elif it[0] == 'self':
            num += 1
            lines = it[2] if isinstance(it[2], list) else [it[2]]
            plan.append(('self', it[1], lines, y, num))
            y += 30 + 12 * (len(lines) - 1) + 10
        elif it[0] == 'note':
            lines = it[3] if isinstance(it[3], list) else [it[3]]
            plan.append(('note', it[1], it[2], lines, y, it[4] if len(it) > 4 else 'gap'))
            y += 16 + 13 * len(lines) + 12
    H = y + 30
    s = Svg(width, H)
    # khung pha
    for label, y1, y2, col in frames:
        s.rect(24, y1, width - 48, y2 - y1, 'none', col, rx=6, dash='7 5', sw=1.1)
        wlab = 22 + len(label) * 6.9
        s.add('<path d="M24 %s h%s v12 l-10 10 h-%s z" fill="%s"/>' % (y1, wlab, wlab - 10, col))
        s.text(32, y1 + 15, label, size=10.2, weight=700, fill='#fff')
    # lifeline
    for key, title, tech, kind, x in parts:
        s.line(x, 70, x, H - 20, color='#94A3B8', dash='4 4', sw=1.1)
    for key, title, tech, kind, x in parts:
        w = pw
        if kind == 'person':
            s.person(x - w / 2, 16, w, 54, title, sub=tech)
        else:
            s.box(x - w / 2, 16, w, 54, title, tech=tech, kind=kind, center=True, tsize=12)
    for p in plan:
        if p[0] == 'm':
            _, a, b, lines, style, yy, n = p
            xa, xb = xs[a], xs[b]
            d = 1 if xb > xa else -1
            s.arrow([(xa + 0, yy), (xb - d * 2, yy)], style=style)
            s.badge(xa + d * 13, yy, n)
            mid = (xa + xb) / 2 + d * 8
            s.text(mid, yy - 11 - 12.2 * (len(lines) - 1), lines, size=10.4, anchor='middle', halo=True, lh=12.2)
        elif p[0] == 'self':
            _, a, lines, yy, n = p
            x = xs[a]
            s.add('<path d="M%s %s h34 v20 h-32" fill="none" stroke="%s" stroke-width="1.5" marker-end="url(#ah)"/>' % (
                x, yy - 6, LINE))
            s.badge(x + 13, yy - 6, n)
            s.text(x + 42, yy + 2, lines, size=10.4, halo=True, lh=12.2)
        elif p[0] == 'note':
            _, a, b, lines, yy, k = p
            x1 = min(xs[a], xs[b]) - 70
            x2 = max(xs[a], xs[b]) + 70
            f, st = KIND[k]
            s.rect(x1, yy - 8, x2 - x1, 13 * len(lines) + 14, f, st, rx=5, dash='5 4' if k == 'gap' else None, sw=1.1)
            s.text((x1 + x2) / 2, yy + 8, lines, size=10.2, anchor='middle',
                   fill='#7f1d1d' if k == 'gap' else '#334155', lh=13)
    return s.render()


# ───────────────────────── TRANG HTML ─────────────────────────
CSS = '''
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',system-ui,-apple-system,sans-serif;color:#0f172a;background:#fff;-webkit-font-smoothing:antialiased}
.page{max-width:1850px;margin:0 auto;padding:26px 30px 44px}
.tb{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;border-bottom:2px solid #0f172a;padding-bottom:12px;margin-bottom:16px}
.tb .k{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:11px;font-weight:600;color:#475569;letter-spacing:.06em;text-transform:uppercase}
.tb h1{font-size:24px;font-weight:800;letter-spacing:-.02em;margin-top:4px}
.tb p{font-size:13px;color:#475569;margin-top:5px;max-width:900px;line-height:1.5}
.meta{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:10.5px;color:#334155;border:1px solid #cbd5e1;border-collapse:collapse;flex:0 0 auto}
.meta td{border:1px solid #cbd5e1;padding:4px 9px;white-space:nowrap}
.meta td:first-child{color:#64748b;background:#f8fafc}
.meta .w{color:#b91c1c;font-weight:600}
svg{display:block;width:100%;height:auto}
h2{font-size:15px;font-weight:700;margin:26px 0 4px}
h2 small{font-weight:400;color:#64748b;font-size:12.5px;margin-left:6px}
.fig{border:1px solid #e2e8f0;border-radius:8px;padding:10px 6px 6px;margin-top:10px}
table.cat{width:100%;border-collapse:collapse;font-size:12.5px;margin-top:10px}
table.cat th{font-size:10.5px;text-transform:uppercase;letter-spacing:.06em;color:#475569;text-align:left;border-bottom:2px solid #0f172a;padding:7px 10px}
table.cat td{border-bottom:1px solid #e2e8f0;padding:7px 10px;vertical-align:top;line-height:1.45}
table.cat td:first-child{width:38px}
table.cat .n{display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#0f172a;color:#fff;font-size:10.5px;font-weight:700}
table.cat .t{font-weight:600;white-space:nowrap}
table.cat .ty{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:10.5px;color:#334155;white-space:nowrap}
table.cat .ref{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:10.5px;color:#64748b;white-space:nowrap}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:26px}
.note{font-size:12.5px;color:#475569;line-height:1.55;margin-top:8px}
.note b{color:#0f172a}
ul.l{margin:8px 0 0 18px;font-size:12.8px;line-height:1.6;color:#1e293b}
.gapc{color:#b91c1c}
'''


def catalog(rows, headers=('#', 'Từ → đến', 'Kiểu', 'Nội dung', 'Tham chiếu')):
    """Bảng danh mục giao tiếp. rows: [(số, 'A → B', kiểu, nội dung, tham chiếu)]."""
    th = ''.join('<th>%s</th>' % E(h) for h in headers)
    tr = ''.join(
        '<tr><td><span class="n">%s</span></td><td class="t">%s</td><td class="ty">%s</td><td>%s</td><td class="ref">%s</td></tr>' % (
            n, E(a), E(t), E(d), E(r)) for n, a, t, d, r in rows)
    return '<table class="cat"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (th, tr)


def page(title, kicker, h1, sub, body, meta):
    """Trang HTML có khung tên bản vẽ.
    meta: [(nhãn, giá trị)] hoặc [(nhãn, giá trị, True)] để tô đỏ (cảnh báo: nguồn chưa QC…).
    Nên có đủ: Nguồn · Phạm vi (hiện trạng / trạng thái đích) · Tình trạng · Bản vẽ (mã · phiên bản · ngày)."""
    rows = ''
    for m in meta:
        warn = ' class="w"' if len(m) > 2 and m[2] else ''
        rows += '<tr><td>%s</td><td%s>%s</td></tr>' % (E(m[0]), warn, E(m[1]))
    return '''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>%s</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>%s</style>
</head>
<body>
<div class="page">
<div class="tb">
  <div><div class="k">%s</div><h1>%s</h1><p>%s</p></div>
  <table class="meta">%s</table>
</div>
%s
</div>
</body>
</html>
''' % (E(title), CSS, E(kicker), E(h1), E(sub), rows, body)
