# tool-diagram v2 — API của archkit + luật bố cục

## 1. API nhanh (`lib/archkit.py`)

```python
from archkit import Svg, seq, catalog, page

s = Svg(1790, 898)                      # khung vẽ, đơn vị px theo viewBox; trang HTML tự co giãn
s.person(x, y, w, h, 'Khách hàng', sub='dòng phụ')            # người dùng
s.box(x, y, w, h, 'Tên', tech='công nghệ · hiện trạng',       # thành phần
      desc=['dòng 1', 'dòng 2'], kind='build')                # kind: build|module|saas|ext|gap
s.cyl(x, y, w, h, 'MariaDB', tech='…', desc=[…])              # kho dữ liệu
s.boundary(x, y, w, h, 'Nhãn', color='#4338CA', fill='#FAFAFF', bottom=True)   # ranh giới
s.arrow([(x1, y1), (x2, y2), …], style='sync',                # đường gấp khúc qua các điểm
        label='nhãn' hoặc ['dòng 1', 'dòng 2'], lpos=(x, y), lanchor='middle',
        num=7, npos=(x, y))                                   # số giao tiếp + vị trí vòng tròn
s.badge(x, y, 7) · s.dot(x, y) · s.line(x1, y1, x2, y2) · s.text(x, y, 'chữ' | [dòng…], size=11, …)
s.legend(x, y, w)                       # khung chú giải cao 84px
svg = s.render()

seq(PARTS, STEPS, width=1790, pw=160)   # → chuỗi SVG sequence diagram
#   PARTS: [(khoá, tên, công nghệ|None, kind, x_lifeline)]
#   STEPS: ('frame', 'NHÃN PHA', màu) · ('end',)
#          ('m', từ, đến, 'nhãn', 'sync'|'async'|'ret')   — tự đánh số, tự ngắt 2 dòng
#          ('self', ai, ['dòng 1', 'dòng 2'])             — tự gọi chính mình
#          ('note', từ, đến, ['dòng'], 'gap'|'module')    — ghi chú; 'gap' = đỏ nét đứt

catalog(rows)                           # rows: [(số, 'A → B', kiểu, nội dung, tham chiếu)] → HTML <table>
page(title, kicker, h1, sub, body, meta)   # meta: [(nhãn, giá trị[, True = tô đỏ])]
```

Kích thước tham chiếu: ô thành phần 160–290 × 66–96 · ô người dùng 110–170 × 58–64 · khoảng hở giữa hai ranh giới 40–60 · chữ tiêu đề ô 11.5–12.5 · chữ mô tả 9.8–10.5 · nhãn mũi tên 9.3–10.

## 2. Luật bố cục (rút từ dự án thật, mỗi dòng là một lần vẽ lại)

**Xếp chỗ**
- Chọn thứ tự cột theo quan hệ: hai hệ nói chuyện với nhau phải nằm cạnh nhau. Bên thứ ba chỉ nói chuyện với hệ lõi thì đặt sát hệ lõi, đừng để cách một cột.
- Người dùng đặt ngay trên thứ họ dùng. Một người dùng hai hệ ở xa nhau → cho một đường đi **vòng phía trên** hàng người dùng thay vì cắt ngang.
- Hệ lõi tự xây nằm giữa, to nhất. Bên trong: thanh API ở trên → lưới thành phần → kho dữ liệu ở đáy.
- Một ô lớn cho hệ ngoài quan trọng (vd CRM) kéo dài theo chiều dọc để mọi mũi tên nối vào nó đều đi ngang.

**Mũi tên**
- Chỉ đi ngang hoặc dọc (gấp khúc vuông góc). Không đi chéo.
- Nhiều mũi tên cùng vào một cạnh: cách nhau ít nhất 22px.
- Đường dài dùng chung một trục (bus) rồi tách nhánh, đừng vẽ nhiều đường song song.
- Hai đường buộc phải cắt nhau → đổi chỗ ô trước; chỉ chấp nhận cắt khi đã thử đổi thứ tự cột.
- Mũi tên ngắn hơn ~120px: chỉ đánh số, không nhãn. Nội dung để ở bảng danh mục.
- Nhãn đặt trên đoạn dài nhất, cách đường 6–8px, có viền trắng (đã bật sẵn).

**Chữ**
- Nhãn ranh giới ở đáy (`bottom=True`) khi có mũi tên đi vào từ trên, nếu không mũi tên sẽ cắt nhãn.
- Chữ trong ô: ước lượng 6px mỗi ký tự ở cỡ 10.5. Dài quá thì ngắt dòng tay.
- Dòng trống trong `desc` viết `''` (archkit tự giữ chiều cao).
- Một ô tối đa: tên + 1 dòng công nghệ + 2–3 dòng mô tả. Riêng ô "nguồn sự thật" lớn thì được liệt kê nó giữ gì.

**Sequence**
- Tối đa 8 cột. Cột ít tham gia đặt ngoài cùng bên phải.
- Chia pha bằng `('frame', …)` mỗi 4–8 bước; mỗi pha một màu.
- Vòng lặp / nhánh rẽ / chỗ nguồn không nói: dùng `('note', …)`, đừng vẽ thêm mũi tên.
- Một luồng dài quá 25 bước → tách thành 2 sơ đồ.

**Dữ liệu**
- Trái → phải: hệ nguồn → nạp → kho → báo cáo → người đọc. Vòng phản hồi (dữ liệu quay lại hệ nguồn) vẽ thành dải riêng ở dưới.
- Trong ô kho ghi **tập dữ liệu** và ràng buộc (khoá ghép, chỉ ghi thêm…), không ghi schema chi tiết.
- Cơ chế nạp, công cụ, lịch làm mới mà nguồn không nói → ô `gap`.

## 3. Trang HTML
- Mỗi bản vẽ một file, có khung tên bản vẽ (`meta`), sơ đồ trong `<div class="fig">`, bên dưới là bảng danh mục / ghi chú đọc sơ đồ.
- SVG dùng `viewBox` + `width:100%` nên tự co theo màn hình; PNG chụp ở bề rộng 1850 (hoặc bề rộng SVG + 60).
- Mã bản vẽ: `ARCH-01`, `SEQ-01`, `DATA-01`; đổi nội dung thì tăng `v1 → v2` và ghi ngày.
