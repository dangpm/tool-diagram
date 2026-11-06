#!/usr/bin/env python3
"""build_views.py — KHUÔN KHỞI ĐẦU cho bộ bản vẽ kiến trúc (skill /tool-diagram v2).

Cách dùng:
  1. Copy file này + lib/archkit.py + lib/render_png.py vào thư mục bản vẽ của dự án.
  2. Thay toàn bộ nội dung VÍ DỤ bên dưới ("Cửa hàng online") bằng fact THẬT của hệ đang vẽ.
  3. python3 build_views.py  →  ra arch-01.html, seq-01.html, data-01.html
  4. python3 render_png.py arch-01.html arch-01.png   → mở PNG ra SOI trước khi báo xong.

Ba bản vẽ, ba câu hỏi:
  ARCH-01  sơ đồ thành phần + giao tiếp   → có những khối nào, ai sở hữu, khối nào gọi khối nào
  SEQ-01   sequence diagram                → một việc chạy qua những bước nào, ai gọi ai
  DATA-01  sơ đồ kiến trúc dữ liệu         → dữ liệu từ đâu vào, nằm đâu, ra báo cáo gì

Toạ độ đặt tay. Mẹo bố cục nằm trong reference/notation.md của skill.
"""
import os

from archkit import Svg, seq, catalog, page

HERE = os.path.dirname(os.path.abspath(__file__))
META = [('Nguồn', 'VÍ DỤ — thay bằng tài liệu / repo thật'),
        ('Phạm vi', 'Trạng thái đích'),            # hoặc 'Hiện trạng'
        ('Tình trạng', 'Bản nháp, chưa QC', True),  # True = tô đỏ
        ]


# ───────────────────────── ARCH-01 ─────────────────────────
def arch():
    s = Svg(1280, 730)

    # Người dùng (đặt ngay trên thứ họ dùng để mũi tên đi thẳng)
    s.person(410, 24, 140, 58, 'Khách mua')
    s.person(712, 24, 150, 58, 'Quản trị viên')
    s.person(1040, 24, 150, 58, 'Nhân viên CSKH')

    # Tầng giao diện
    s.boundary(320, 140, 620, 110, 'Tầng giao diện')
    s.box(335, 162, 290, 74, 'Web shop', tech='Next.js · đang chạy', desc=['Xem hàng, giỏ hàng, đặt hàng'])
    s.box(637, 162, 290, 74, 'Trang quản trị', tech='đang xây', desc=['Sản phẩm, tồn kho, đơn hàng'])
    s.arrow([(480, 82), (480, 162)], style='use', num=1, npos=(480, 112))
    s.arrow([(787, 82), (787, 162)], style='use', num=2, npos=(787, 112))

    # Hệ lõi tự xây (nhãn ranh giới đặt ở ĐÁY vì mũi tên đi vào từ phía trên)
    s.boundary(320, 300, 620, 310, 'Order service — tự xây · nguồn sự thật cho đơn hàng và tồn kho',
               color='#4338CA', fill='#FAFAFF', bottom=True)
    s.box(335, 322, 592, 44, 'API /v1', tech='REST · quyền chặn ở tầng API')
    s.arrow([(480, 236), (480, 322)], label=['giỏ hàng, đặt hàng'], lpos=(494, 284), lanchor='start',
            num=4, npos=(480, 284))
    s.arrow([(787, 236), (787, 322)], label=['đọc / ghi theo vai trò'], lpos=(801, 284), lanchor='start',
            num=5, npos=(787, 284))
    mods = [('Thông báo', ['email, SMS']), ('Giỏ hàng', ['giữ giá 30 phút']), ('Đơn hàng', ['trạng thái, hoàn']),
            ('Tồn kho', ['trừ lúc đặt']), ('Sự kiện ra', ['mỗi sự kiện 1 id'])]
    for i, (t, d) in enumerate(mods):
        s.box(335 + i * 120, 384, 112, 66, t, desc=d, kind='module', tsize=11.5, dsize=9.8, pad=8)
    s.cyl(335, 474, 592, 96, 'PostgreSQL', tech='đơn hàng · tồn kho · sổ cái',
          desc=['Sổ cái tồn kho chỉ ghi thêm, không sửa.'])
    s.arrow([(631, 450), (631, 476)])

    # Mua / SaaS
    s.boundary(1000, 140, 250, 470, 'Mua / SaaS', color='#047857', bottom=True)
    s.box(1015, 162, 220, 110, 'CRM', tech='SaaS · chưa triển khai', kind='saas',
          desc=['khách, hội thoại, ticket', 'Chỉ giữ mã đơn, không giữ giá.'])
    s.box(1015, 384, 220, 80, 'Kho phân tích', tech='công cụ chưa chọn', kind='saas',
          desc=['Chỉ để báo cáo.'])
    s.box(1015, 520, 220, 50, 'BI', tech='báo cáo doanh thu', kind='saas')
    s.arrow([(1115, 82), (1115, 162)], style='use', num=3, npos=(1115, 112))
    s.arrow([(927, 400), (968, 400), (968, 230), (1015, 230)], style='async', num=6, npos=(968, 315))
    s.arrow([(927, 432), (1015, 432)], style='async', num=7, npos=(971, 432))
    s.arrow([(1125, 272), (1125, 384)], style='async', label=['khách,', 'ticket'], lpos=(1137, 326),
            lanchor='start', num=8, npos=(1125, 330))
    s.arrow([(1125, 464), (1125, 520)], num=9, npos=(1125, 492))

    # Bên thứ ba (đặt sát hệ nó nói chuyện cùng để mũi tên không cắt nhau)
    s.boundary(30, 290, 240, 320, 'Bên thứ ba', bottom=True)
    s.box(45, 316, 210, 58, 'Cổng thanh toán', tech='thẻ · chuyển khoản', kind='ext')
    s.box(45, 400, 210, 50, 'Email / SMS', tech='nhà cung cấp gửi tin', kind='ext')
    s.box(45, 500, 210, 50, 'Hãng vận chuyển', tech='CHƯA đặc tả', kind='gap')
    # Mũi tên ngắn (dưới ~120px): chỉ đánh số, nội dung để ở bảng danh mục giao tiếp
    s.arrow([(335, 334), (255, 334)], num=10, npos=(295, 334))
    s.arrow([(255, 358), (335, 358)], style='async', num=11, npos=(295, 358))
    s.arrow([(335, 425), (255, 425)], style='async', num=12, npos=(295, 425))
    s.arrow([(320, 525), (255, 525)], style='gap', label='?', lpos=(288, 517), lsize=12)

    s.legend(320, 632, 930)
    return s.render()


ARCH_IF = [
    (1, 'Khách mua → Web shop', 'Sử dụng', 'Xem hàng, đặt hàng, thanh toán.', 'PRD §2'),
    (2, 'Quản trị viên → Trang quản trị', 'Sử dụng', 'Nhập sản phẩm, chỉnh tồn kho, xử lý đơn.', 'PRD §5'),
    (3, 'CSKH → CRM', 'Sử dụng', 'Trả lời khách, mở ticket.', '—'),
    (4, 'Web shop → API', 'Đồng bộ', 'GET sản phẩm · POST giỏ hàng · POST đơn hàng.', 'API §1'),
    (5, 'Trang quản trị → API', 'Đồng bộ', 'Đọc / ghi theo vai trò.', 'API §3'),
    (6, 'Order service → CRM', 'Sự kiện', 'order.created · order.paid · order.refunded.', 'API §6'),
    (7, 'Order service → Kho phân tích', 'Sự kiện', 'order.paid · order.refunded.', 'API §6'),
    (8, 'CRM → Kho phân tích', 'Trích xuất', 'Khách, ticket. Cách nạp: chưa đặc tả.', '—'),
    (9, 'Kho phân tích → BI', 'Đồng bộ', 'Doanh thu, tỷ lệ hoàn.', '—'),
    (10, 'Order service → Cổng thanh toán', 'Đồng bộ', 'Tạo phiên thanh toán.', 'API §4'),
    (11, 'Cổng thanh toán → Order service', 'Webhook', 'Kết quả thanh toán, có mã giao dịch chống ghi trùng.', 'API §4'),
    (12, 'Order service → Email / SMS', 'Sự kiện', 'Xác nhận đơn, nhắc thanh toán.', 'API §7'),
]

# ───────────────────────── SEQ-01 ─────────────────────────
# (khoá, tên, [công nghệ], kind, toạ độ x của lifeline)
PARTS = [
    ('kh', 'Khách mua', None, 'person', 120),
    ('web', 'Web shop', 'Next.js', 'build', 370),
    ('api', 'Order service', 'API /v1', 'build', 640),
    ('pay', 'Cổng thanh toán', 'bên thứ ba', 'ext', 910),
    ('crm', 'CRM', 'chưa triển khai', 'saas', 1150),
]
STEPS = [
    ('frame', 'A · ĐẶT HÀNG', '#4338CA'),
    ('m', 'kh', 'web', 'bấm “Đặt hàng”', 'sync'),
    ('m', 'web', 'api', 'POST /v1/orders', 'sync'),
    ('self', 'api', ['trừ tồn kho, ghi sổ cái', '(hết hàng: trả 409)']),
    ('m', 'api', 'web', 'mã đơn + link thanh toán', 'ret'),
    ('end',),
    ('frame', 'B · THANH TOÁN', '#B45309'),
    ('m', 'kh', 'pay', 'trả tiền', 'sync'),
    ('m', 'pay', 'api', 'webhook: đã thanh toán (mã giao dịch)', 'async'),
    ('m', 'api', 'crm', 'order.paid', 'async'),
    ('note', 'kh', 'api', ['Hoàn tiền: tài liệu chưa đặc tả luồng này.'], 'gap'),
    ('end',),
]


# ───────────────────────── DATA-01 ─────────────────────────
def data():
    s = Svg(1280, 380)
    s.boundary(30, 20, 290, 340, 'Hệ nguồn')
    s.box(45, 46, 260, 90, 'Order service', tech='tự xây', desc=['đơn hàng, hoàn tiền, tồn kho'])
    s.box(45, 150, 260, 80, 'CRM', tech='chưa triển khai', kind='saas', desc=['khách, ticket'])
    s.box(45, 244, 260, 70, 'Nền tảng quảng cáo', tech='bên thứ ba', kind='ext', desc=['chi phí theo chiến dịch'])

    s.boundary(390, 20, 230, 340, 'Nạp dữ liệu')
    s.box(405, 46, 200, 90, 'Sự kiện', tech='bất đồng bộ', kind='module', desc=['order.paid', 'order.refunded'])
    s.box(405, 150, 200, 164, 'Trích xuất định kỳ', tech='CHƯA đặc tả', kind='gap',
          desc=['công cụ nạp', 'lịch làm mới'])
    s.arrow([(305, 91), (405, 91)], style='async', num=1, npos=(355, 91))
    s.arrow([(305, 190), (405, 190)], style='gap', num=2, npos=(355, 190))
    s.arrow([(305, 279), (405, 279)], style='gap', num=3, npos=(355, 279))

    s.boundary(690, 20, 250, 340, 'Kho phân tích — không là nguồn sự thật', color='#047857')
    s.box(705, 46, 220, 90, 'Đơn hàng', tech='chỉ ghi thêm', kind='saas', desc=['mỗi lần hoàn là 1 bản ghi mới'])
    s.box(705, 150, 220, 70, 'Khách & ticket', kind='saas', desc=['ghép bằng mã khách'])
    s.box(705, 234, 220, 70, 'Chi phí quảng cáo', kind='saas', desc=['theo chiến dịch'])
    s.arrow([(605, 91), (705, 91)], style='async', num=4, npos=(655, 91))
    s.arrow([(605, 232), (690, 232)], style='gap', label='?', lpos=(648, 224), lsize=12)

    s.boundary(1010, 20, 240, 340, 'BI')
    s.box(1025, 46, 210, 70, 'Doanh thu', kind='module', desc=['theo ngày thanh toán'])
    s.box(1025, 130, 210, 70, 'Tỷ lệ hoàn', kind='module', desc=['theo sản phẩm'])
    s.box(1025, 214, 210, 70, 'ROAS', kind='module', desc=['doanh thu / chi phí ads'])
    s.arrow([(940, 165), (1010, 165)], num=5, npos=(975, 165))
    return s.render()


def build():
    body = ('<div class="fig">%s</div><h2>Danh mục giao tiếp <small>số trong vòng tròn đen trên sơ đồ</small></h2>%s'
            % (arch(), catalog(ARCH_IF)))
    out = page('ARCH-01 — Kiến trúc tổng thể', 'Kiến trúc hệ thống · sơ đồ thành phần và giao tiếp',
               'Cửa hàng online — kiến trúc tổng thể', 'Một câu nói ý chính của bản vẽ: ai giữ sự thật gì.',
               body, META + [('Bản vẽ', 'ARCH-01 · v1 · dd.mm.yyyy')])
    open(os.path.join(HERE, 'arch-01.html'), 'w', encoding='utf-8').write(out)

    body = '<h2>Luồng 1 — Đặt hàng và thanh toán <small>sequence diagram</small></h2><div class="fig">%s</div>' % seq(
        PARTS, STEPS, width=1280)
    out = page('SEQ-01 — Luồng xử lý', 'Kiến trúc hệ thống · sequence diagram',
               'Cửa hàng online — luồng xử lý chính', 'Mỗi cột là một bên tham gia; đọc từ trên xuống.',
               body, META + [('Bản vẽ', 'SEQ-01 · v1 · dd.mm.yyyy')])
    open(os.path.join(HERE, 'seq-01.html'), 'w', encoding='utf-8').write(out)

    body = '<div class="fig">%s</div>' % data()
    out = page('DATA-01 — Kiến trúc dữ liệu', 'Kiến trúc dữ liệu · nguồn → nạp → kho → báo cáo',
               'Cửa hàng online — kiến trúc dữ liệu', 'Ô và mũi tên đỏ nét đứt là phần tài liệu chưa đặc tả.',
               body, META + [('Bản vẽ', 'DATA-01 · v1 · dd.mm.yyyy')])
    open(os.path.join(HERE, 'data-01.html'), 'w', encoding='utf-8').write(out)
    print('ok: arch-01.html, seq-01.html, data-01.html')


if __name__ == '__main__':
    build()
