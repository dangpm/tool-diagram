#!/usr/bin/env python3
"""build_views.py — Bản đồ AI code + hệ thống riêng, cho người không code (skill /tool-diagram v2).

  ARCH-01  sơ đồ thành phần + giao tiếp  → máy bạn, GitHub, VPS, Cloudflare, API ngoài nối nhau thế nào
  SEQ-01   sequence diagram               → lúc XÂY và lúc CHẠY, ai gọi ai theo thứ tự

Build:  python3 build_views.py
Render: python3 ../../lib/render_png.py arch-01.html arch-01.png 1460 2
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lib'))  # dùng archkit của repo; dự án thật thì copy archkit.py vào cạnh file này

from archkit import Svg, seq, catalog, page, E

DATE = '28.10.2026'
META = [('Nguồn', 'Mô hình tham chiếu chung, không vẽ từ 1 hệ cụ thể'),
        ('Phạm vi', 'Hệ điển hình: 1 app chạy trên 1 VPS'),
        ('Người đọc', 'Chủ dự án không code'),
        ('Tình trạng', 'Bản giáo dục, chưa QC', True)]
BUILD = '#4338CA'   # badge lúc XÂY
RUN = '#047857'     # badge lúc CHẠY


def link(s, pts, n, npos, run=False, **kw):
    """Mũi tên + badge màu theo luồng (XÂY = tím, CHẠY = xanh)."""
    s.arrow(pts, **kw)
    s.badge(npos[0], npos[1], n, fill=RUN if run else BUILD)


# ───────────────────────── ARCH-01 ─────────────────────────
def arch():
    s = Svg(1400, 940)

    # Người dùng
    s.person(240, 24, 220, 58, 'Bạn', sub='ra yêu cầu, duyệt kết quả')
    s.person(820, 24, 240, 58, 'Khách hàng · nhân viên', sub='mở tenban.com trên điện thoại')

    # Máy của bạn
    s.boundary(40, 120, 400, 345, 'Máy của bạn — chỉ chạy khi mở máy', color=BUILD)
    s.box(60, 150, 360, 110, 'Claude Code · Cursor · Codex', tech='thuê bao · thợ code AI', kind='saas',
          desc=['Đọc file, viết code, chạy lệnh, deploy.', 'Làm thật trên máy, không chỉ trả lời.',
                '', 'Gập máy là thợ nghỉ, nhà vẫn chạy.'])
    s.box(60, 330, 160, 100, 'MCP', tech='ổ cắm cho AI', kind='saas',
          desc=['nối Notion, ClickUp,', 'Drive, Gmail…'])
    s.box(240, 330, 180, 100, 'Thư mục dự án', tech='code + .env',
          desc=['Mã nguồn của app.', '.env giữ API key.'])

    # GitHub
    s.box(500, 340, 170, 80, 'GitHub', tech='SaaS · repo private', kind='saas',
          desc=['Lưu mọi phiên bản.', '= nút Undo khi hỏng.'])

    # Cloudflare
    s.box(720, 130, 380, 96, 'Cloudflare', tech='SaaS · gói free đủ cho đa số', kind='saas',
          desc=['Trỏ tên miền (DNS) · khoá HTTPS', 'Chặn bot · cache · giấu IP thật của VPS'])

    # VPS
    s.boundary(690, 270, 670, 375, 'VPS — máy chủ thuê, chạy 24/7', color=RUN)
    s.box(730, 300, 280, 96, 'Web / App', tech='code của bạn · chạy trong Docker',
          desc=['Trang web, form, API riêng.', 'Vẫn chạy khi bạn tắt máy.'])
    s.cyl(1060, 300, 280, 110, 'Database', tech='nguồn sự thật của app',
          desc=['khách · đơn · lịch hẹn', 'Mất là mất luôn.'])
    s.box(730, 440, 280, 80, 'Tự động hoá', tech='cron · n8n',
          desc=['Việc chạy theo giờ, không ai bấm.'])
    s.box(1060, 440, 280, 80, 'Backup ra ngoài VPS', tech='HAY BỊ QUÊN', kind='gap',
          desc=['S3 · R2 · Drive, mỗi ngày.', 'Thử khôi phục ít nhất 1 lần.'])
    s.box(730, 550, 280, 70, 'Log · giám sát', tech='nhật ký app',
          desc=['Ghi lỗi, ai làm gì lúc nào.'])

    # Dịch vụ ngoài
    s.boundary(40, 700, 1320, 120, 'Dịch vụ ngoài — API, trả theo lượt, mở bằng API key', bottom=True)
    apis = [('Dữ liệu & công việc', 'Sheets · Notion · ClickUp', 'đọc / ghi qua API'),
            ('Quảng cáo', 'Meta · Google · TikTok', 'số liệu, tạo chiến dịch'),
            ('Thanh toán', 'Stripe · VNPay · PayOS', 'thu tiền, báo đã trả'),
            ('Gửi tin', 'Zalo OA · Telegram · Email', 'xác nhận, nhắc lịch, cảnh báo'),
            ('AI', 'Claude · OpenAI · Gemini', 'trả lời, tóm tắt, phân loại')]
    for i, (t, tech, d) in enumerate(apis):
        s.box(60 + i * 258, 722, 240, 70, t, tech=tech, desc=[d], kind='ext')

    # Lúc XÂY
    link(s, [(350, 82), (350, 150)], 1, (350, 116), style='use')
    link(s, [(330, 260), (330, 330)], 2, (330, 295))
    link(s, [(420, 380), (500, 380)], 3, (460, 380))
    link(s, [(670, 360), (730, 360)], 4, (700, 360))
    link(s, [(420, 190), (720, 190)], 5, (570, 190), label='cài tên miền qua API', lpos=(570, 180))
    link(s, [(140, 260), (140, 330)], 6, (140, 295))
    link(s, [(140, 430), (140, 700)], 7, (140, 560), label=['đọc / ghi tool', 'trong lúc làm'],
         lpos=(156, 556), lanchor='start')

    # Lúc CHẠY
    link(s, [(940, 82), (940, 130)], 'A', (940, 106), run=True, style='use')
    link(s, [(980, 226), (980, 300)], 'B', (980, 263), run=True)
    link(s, [(1010, 335), (1060, 335)], 'C', (1035, 335), run=True)
    s.line(1010, 480, 1035, 480, color='#334155', sw=1.5)
    s.dot(1035, 480)
    link(s, [(1010, 375), (1035, 375), (1035, 700)], 'D', (1035, 575), run=True,
         label=['app + tự động hoá', 'gọi API: thu tiền,', 'gửi tin, gọi AI'], lpos=(1052, 568), lanchor='start')
    link(s, [(710, 700), (710, 385), (730, 385)], 'E', (710, 610), run=True, style='async',
         label=['webhook báo về', '(khách đã trả tiền…)'], lpos=(696, 606), lanchor='end')
    link(s, [(1200, 410), (1200, 440)], 'F', (1200, 425), run=True, style='gap')
    link(s, [(900, 620), (900, 700)], 'G', (900, 655), run=True, style='gap',
         label=['cảnh báo khi sập', '(hay bị quên)'], lpos=(914, 652), lanchor='start')

    # Chú giải
    s.legend(40, 840, 1320,
             kinds=[('person', 'Người dùng'), ('build', 'Tự xây (code của bạn)'),
                    ('saas', 'Thuê / SaaS bạn vận hành'), ('ext', 'Bên thứ ba (API)'),
                    ('gap', 'Hay bị quên, phải tự thêm')],
             styles=[('sync', 'gọi đồng bộ (API)'), ('async', 'webhook báo về'), ('use', 'sử dụng'),
                     ('gap', 'hay bị quên')],
             badge=False)
    s.badge(950, 872, 1, fill=BUILD)
    s.text(964, 876, 'lúc XÂY (bạn + AI)', size=10.2)
    s.badge(1110, 872, 'A', fill=RUN)
    s.text(1124, 876, 'lúc CHẠY (khách dùng, 24/7)', size=10.2)
    return s.render()


ARCH_IF = [
    (1, 'Bạn → Claude Code', 'Sử dụng', 'Nói yêu cầu bằng tiếng Việt, đọc kết quả, duyệt.', 'XÂY'),
    (2, 'Claude Code → Thư mục dự án', 'Đồng bộ', 'Đọc file, viết code, chạy thử, tự sửa lỗi.', 'XÂY'),
    (3, 'Thư mục dự án → GitHub', 'Đồng bộ', 'Lưu bản (git push). Mỗi lần lưu là một mốc để quay lại.', 'XÂY'),
    (4, 'GitHub → Web / App trên VPS', 'Đồng bộ', 'Deploy: VPS kéo bản mới, build, khởi động lại.', 'XÂY'),
    (5, 'Claude Code → Cloudflare', 'Đồng bộ', 'Trỏ tenban.com về IP của VPS, bật HTTPS.', 'XÂY'),
    (6, 'Claude Code → MCP', 'Đồng bộ', 'AI cắm vào tool bạn đang dùng.', 'XÂY'),
    (7, 'MCP → Dịch vụ ngoài', 'Đồng bộ', 'Đọc Notion, tạo task ClickUp, kéo số liệu Ads ngay trong lúc làm.', 'XÂY'),
    ('A', 'Khách → Cloudflare', 'Sử dụng', 'Gõ tên miền. Cloudflare tra ra nhà nằm ở đâu.', 'CHẠY'),
    ('B', 'Cloudflare → Web / App', 'Đồng bộ', 'Lọc bot, tấn công, rồi mới chuyển người thật vào VPS.', 'CHẠY'),
    ('C', 'Web / App → Database', 'Đồng bộ', 'Đọc và ghi: lịch hẹn, khách, đơn.', 'CHẠY'),
    ('D', 'App, tự động hoá → Dịch vụ ngoài', 'Đồng bộ', 'Thu tiền, gửi Zalo xác nhận, nhờ AI trả lời. Tính tiền theo lượt.', 'CHẠY'),
    ('E', 'Dịch vụ ngoài → Web / App', 'Webhook', 'Cổng thanh toán báo “khách đã trả tiền”, app cập nhật đơn.', 'CHẠY'),
    ('F', 'Database → Backup ngoài VPS', 'Hay bị quên', 'Sao lưu mỗi ngày ra nơi khác VPS. VPS chết vẫn còn dữ liệu.', 'CHẠY'),
    ('G', 'Log → Gửi tin', 'Hay bị quên', 'App sập thì nhắn Telegram / Zalo cho bạn, đừng để khách báo trước.', 'CHẠY'),
]

COMPARE = [
    ('Ai làm', 'Bạn kéo thả trong khuôn có sẵn', 'AI trả lời, bạn tự copy đi làm', 'AI tự viết, tự chạy, tự deploy'),
    ('Làm được tới đâu', 'Tới giới hạn tính năng nền tảng', 'Tới giới hạn khung chat', 'Gần như mọi thứ có API'),
    ('Chi phí khi lớn', 'Tăng theo số task, số người dùng', 'Thuê bao cố định', 'VPS cố định, API theo lượt dùng'),
    ('Dữ liệu nằm ở', 'Server của nền tảng', 'Lịch sử chat', 'Database của bạn'),
    ('Khi hỏng, ai lo', 'Nền tảng lo hạ tầng', 'Không có gì chạy để hỏng', 'Bạn lo, có AI phụ sửa'),
    ('Hợp nhất cho', 'Web giới thiệu, form, luồng đơn giản', 'Viết, hỏi, nghĩ ý tưởng', 'Tool nội bộ, nối nhiều hệ, tự động hoá riêng'),
]

CARE = [
    ('Chìa khoá (API key, mật khẩu)', '6 · 7 · D', 'Lộ chìa thì người lạ xài tiền và đọc dữ liệu của bạn.',
     ['Để trong .env, không dán vào code, không đẩy lên GitHub, không gửi qua chat nhóm.',
      'Repo GitHub để Private. Mỗi dịch vụ một chìa, lộ chìa nào thu hồi chìa đó.']),
    ('Tiền chạy ngầm', 'D', 'Code lặp lỗi gọi API cả đêm, sáng ra hoá đơn vài trăm đô.',
     ['Đặt hạn mức chi (spending limit) cho AI API và mọi dịch vụ tính theo lượt.',
      'Xem hoá đơn mỗi tháng. Tắt VPS, dịch vụ không còn dùng.']),
    ('Dữ liệu', 'C · F', 'VPS chết hoặc AI chạy nhầm lệnh xoá, mất sạch sổ cái.',
     ['Backup database mỗi ngày ra ngoài VPS (F). Thử khôi phục 1 lần.',
      'Lưu GitHub thường xuyên (3), mỗi việc một lần lưu.']),
    ('Cửa nhà VPS', 'B', 'Bị dò mật khẩu, cài phần mềm đào coin, bị dùng đi tấn công người khác.',
     ['Đăng nhập bằng SSH key, tắt đăng nhập mật khẩu. Bật firewall, chỉ mở đúng cổng.',
      'Khách đi qua Cloudflare (B), không vào thẳng IP. Cập nhật hệ điều hành định kỳ.']),
    ('Sập im lặng', 'G', 'App chết ba ngày, khách biết trước bạn.',
     ['Gắn theo dõi uptime báo Telegram / Zalo (G). Automation phải báo khi lỗi, không chỉ khi xong.',
      'Ghi lịch hết hạn: tên miền, token (Meta thường ~60 ngày), thẻ thanh toán, ổ đĩa sắp đầy.']),
    ('Quyền của AI', '2 · 4', 'AI làm nhanh, làm sai cũng nhanh, kể cả trên hệ thống thật.',
     ['Tách bản thử (staging) và bản thật (production).',
      'Bắt AI hỏi trước khi xoá, deploy, chạy lệnh lên bản thật. Đọc tóm tắt thay đổi trước khi duyệt.']),
    ('Ai đứng tên', 'mọi vùng', 'Freelancer nghỉ, cầm theo tài khoản tên miền và VPS.',
     ['Tên miền, Cloudflare, VPS, GitHub, API: email công ty, bật xác thực 2 lớp.',
      'Người làm thuê chỉ được mời vào, không giữ quyền chủ.']),
    ('Trí nhớ', 'máy bạn', 'AI không nhớ gì giữa các phiên. Ba tháng sau không ai biết app chạy thế nào.',
     ['Viết README + file luật dự án (CLAUDE.md): app ở đâu, deploy ra sao, chìa nào dùng cho gì.',
      'Cất bản vẽ này cùng code, sửa khi hệ thay đổi.']),
]

EXTRA_CSS = '''<style>
.k2{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:10px}
@media (max-width:1200px){.k2{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:640px){.k2{grid-template-columns:1fr}}
.risk{border:1px solid #e2e8f0;border-radius:8px;padding:12px 14px}
.risk h3{font-size:13.5px;font-weight:700;display:flex;justify-content:space-between;gap:10px}
.risk h3 span{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:10.5px;font-weight:600;color:#64748b;white-space:nowrap}
.risk .c{font-size:12.3px;color:#b91c1c;background:#FEF2F2;border-radius:5px;padding:5px 8px;margin-top:7px}
.risk ul{margin:7px 0 0 18px;font-size:12.6px;line-height:1.55;color:#1e293b}
table.cmp td.hi,table.cmp th.hi{background:#EEF2FF}
.tw{overflow-x:auto}
.tw table{min-width:760px}
.fig{overflow-x:auto}
.fig svg{min-width:900px}
@media (max-width:760px){.page{padding:18px 14px 30px}.tb{flex-direction:column;align-items:flex-start}}
</style>'''


def color_badges(html):
    """Badge trong bảng cùng màu với sơ đồ: số = XÂY, chữ = CHẠY."""
    for n, *_ in ARCH_IF:
        html = html.replace('<span class="n">%s</span>' % n, '<span class="n" style="background:%s">%s</span>' % (
            BUILD if isinstance(n, int) else RUN, n))
    return html


def compare_html():
    head = ('<tr><th></th><th>Nocode<br><small>Wix · Make · Zapier · Glide</small></th>'
            '<th>Chat với AI<br><small>ChatGPT · Claude trên web</small></th>'
            '<th class="hi">AI code + hệ riêng<br><small>Claude Code + VPS + Cloudflare + API</small></th></tr>')
    rows = ''.join('<tr><td class="t">%s</td><td>%s</td><td>%s</td><td class="hi">%s</td></tr>' % tuple(E(c) for c in r)
                   for r in COMPARE)
    return '<div class="tw"><table class="cat cmp"><thead>%s</thead><tbody>%s</tbody></table></div>' % (head, rows)


def care_html():
    out = ''
    for t, where, cons, items in CARE:
        lis = ''.join('<li>%s</li>' % E(i) for i in items)
        out += '<div class="risk"><h3>%s<span>%s</span></h3><p class="c">%s</p><ul>%s</ul></div>' % (
            E(t), E(where), E(cons), lis)
    return '<div class="k2">%s</div>' % out


# ───────────────────────── SEQ-01 ─────────────────────────
PARTS = [
    ('ban', 'Bạn', None, 'person', 90),
    ('cc', 'Claude Code', 'thợ code AI', 'saas', 260),
    ('gh', 'GitHub', 'kho code', 'saas', 430),
    ('kh', 'Khách', None, 'person', 600),
    ('cf', 'Cloudflare', 'cổng', 'saas', 770),
    ('app', 'Web / App', 'trên VPS', 'build', 940),
    ('db', 'Database', 'trên VPS', 'build', 1110),
    ('api', 'Dịch vụ ngoài', 'API', 'ext', 1280),
]
STEPS = [
    ('frame', '1 · LÚC XÂY — bạn ngồi với AI, vài giờ đến vài ngày', BUILD),
    ('m', 'ban', 'cc', 'nói yêu cầu bằng tiếng Việt', 'sync'),
    ('self', 'cc', ['đọc thư mục, viết code,', 'chạy thử, tự sửa lỗi']),
    ('m', 'cc', 'ban', 'kết quả để duyệt', 'ret'),
    ('m', 'ban', 'cc', 'duyệt', 'sync'),
    ('m', 'cc', 'gh', 'lưu bản (git push)', 'sync'),
    ('m', 'cc', 'app', 'deploy bản mới lên VPS', 'sync'),
    ('self', 'app', ['build + khởi động lại']),
    ('m', 'cc', 'cf', 'trỏ tên miền về VPS', 'sync'),
    ('note', 'cc', 'gh', ['Hay bị quên: bắt AI hỏi trước khi', 'xoá / deploy lên bản thật.'], 'gap'),
    ('end',),
    ('frame', '2 · LÚC CHẠY — khách dùng mỗi ngày, không cần bạn', RUN),
    ('m', 'kh', 'cf', 'mở tenban.com', 'sync'),
    ('self', 'cf', ['lọc bot, bật HTTPS']),
    ('m', 'cf', 'app', 'chuyển yêu cầu sạch', 'sync'),
    ('m', 'app', 'db', 'lưu lịch hẹn', 'sync'),
    ('m', 'app', 'api', 'thu tiền · gửi Zalo', 'sync'),
    ('m', 'api', 'app', 'webhook: đã thanh toán', 'async'),
    ('m', 'app', 'db', 'cập nhật đơn', 'sync'),
    ('m', 'app', 'kh', 'trang xác nhận', 'ret'),
    ('note', 'app', 'db', ['Hay bị quên: backup DB ra ngoài VPS', 'mỗi ngày + cảnh báo khi app sập.'], 'gap'),
    ('end',),
]


def build():
    body = (EXTRA_CSS +
            '<div class="fig">%s</div>' % arch() +
            '<h2>Danh mục giao tiếp <small>số tím = lúc XÂY · chữ xanh = lúc CHẠY</small></h2>' +
            color_badges(catalog(ARCH_IF, headers=('#', 'Từ → đến', 'Kiểu', 'Nội dung', 'Lúc'))) +
            '<h2>Ba cách dùng công nghệ <small>đổi sức mạnh lấy trách nhiệm</small></h2>' + compare_html() +
            '<p class="note">Những gì nền tảng nocode lo giùm, khi tự chạy hệ riêng sẽ thành việc của bạn. '
            'Tám ô dưới là danh sách đó; góc phải mỗi ô ghi số giao tiếp liên quan trên bản vẽ.</p>'
            '<h2>Những thứ cần care <small>chuyện gì xảy ra nếu bỏ qua → cách chặn trước</small></h2>' + care_html() +
            '<p class="note"><b>Nhớ ba câu:</b> có chìa thì giấu · có dữ liệu thì backup ra chỗ khác · '
            'có chạy tự động thì phải có báo lỗi. Xem luồng theo thứ tự thời gian ở '
            '<a href="seq-01.html">SEQ-01</a>.</p>')
    out = page('ARCH-01 — Bản đồ AI code', 'Kiến trúc hệ thống · sơ đồ thành phần và giao tiếp',
               'AI code chạm tới đâu trong hệ thống của bạn',
               'AI code là thợ xây làm việc trên máy bạn. VPS, Cloudflare, API là căn nhà chạy 24/7 '
               'ngoài internet. Gập laptop: vùng máy bạn nghỉ, phần còn lại vẫn phục vụ khách.',
               body, META + [('Bản vẽ', 'ARCH-01 · v1 · ' + DATE)])
    open(os.path.join(HERE, 'arch-01.html'), 'w', encoding='utf-8').write(out)

    body = (EXTRA_CSS +
            '<h2>Hai luồng: XÂY và CHẠY <small>sequence diagram · đọc từ trên xuống</small></h2>'
            '<div class="fig">%s</div>' % seq(PARTS, STEPS, width=1400) +
            '<p class="note">Bản đồ thành phần và danh mục giao tiếp ở <a href="arch-01.html">ARCH-01</a>.</p>')
    out = page('SEQ-01 — Luồng XÂY và CHẠY', 'Kiến trúc hệ thống · sequence diagram',
               'Một yêu cầu đi qua những đâu',
               'Mỗi cột là một bên tham gia. Pha trên là lúc bạn và AI xây; pha dưới là lúc khách dùng app.',
               body, META + [('Bản vẽ', 'SEQ-01 · v1 · ' + DATE)])
    open(os.path.join(HERE, 'seq-01.html'), 'w', encoding='utf-8').write(out)
    print('ok: arch-01.html, seq-01.html')


if __name__ == '__main__':
    build()
