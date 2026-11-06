---
name: tool-diagram
description: "Vẽ BỘ BẢN VẼ KIẾN TRÚC HỆ THỐNG bài bản bằng SVG dựng tay (diagrams as code), không phải infographic thẻ xếp cột. Ba loại bản vẽ: ARCH (sơ đồ thành phần + giao tiếp đánh số kiểu C4 container, kèm bảng danh mục giao tiếp), SEQ (UML sequence diagram), DATA (sơ đồ kiến trúc dữ liệu nguồn → nạp → kho → báo cáo). Có ranh giới hệ thống, màu theo chủ sở hữu, mũi tên phân kiểu đồng bộ / sự kiện / thủ công, đánh dấu đỏ chỗ nguồn chưa đặc tả, khung tên bản vẽ. Trigger khi user gõ /tool-diagram, hoặc nói 'vẽ sơ đồ kiến trúc', 'kiến trúc hệ thống bài bản', 'diagram flow hệ thống', 'dựng sơ đồ hệ thống từ tài liệu này', 'vẽ lại system của X', 'sequence diagram', 'sơ đồ luồng dữ liệu', 'kiến trúc data warehouse', 'C4 diagram', 'render diagram'. KHÁC ARCHITECTURE.md markdown + mermaid để đọc trong repo. KHÔNG bịa kiến trúc — đọc tài liệu/code thật trước, chỗ nguồn không nói thì vẽ ô đỏ nét đứt. Bản infographic 1 màn kiểu cũ chỉ dùng khi user nói rõ 'infographic nhanh' (--quick)."
argument-hint: "<project hoặc tài liệu nguồn> [--views arch,seq,data] [--quick]"
metadata:
  author: dangpm
  version: "2.0.0"
  license: MIT
---

# /tool-diagram — Bộ bản vẽ kiến trúc hệ thống (v2)

Xuất **bộ bản vẽ kiến trúc** (HTML + PNG + script nguồn) đủ chuẩn để đưa cho dev, tech lead hoặc client đọc: có thành phần, ranh giới, **quan hệ có mũi tên**, và bảng danh mục giao tiếp.

> **v2 thay v1.** v1 là 1 infographic thẻ xếp 4 cột Client → Edge → Compute → Data, không có mũi tên. Bị loại khi dùng thật vì *"nhìn không phải kiểu kiến trúc hệ thống bài bản"*. v1 chỉ còn ở `--quick`.

---

## Tên gọi (dùng đúng tên khi nói với dev / client)

| Cái mình làm | Tên chuẩn | Ghi chú |
|---|---|---|
| Cách làm tổng thể | **Architecture views** (bộ góc nhìn kiến trúc) | Mỗi bản vẽ trả lời 1 câu hỏi. Cùng họ với C4 model, 4+1 view, arc42 |
| Cách dựng | **Diagrams as code** | Sơ đồ sinh từ script; sửa sơ đồ = sửa code rồi build lại |
| `ARCH-01` | **Container diagram kiểu C4** (C4 level 2), có mở một phần **Component** (level 3) của hệ lõi và gộp **System Context** (level 1: người dùng, hệ bên ngoài) | Tiếng Việt: sơ đồ thành phần và giao tiếp |
| Bảng dưới ARCH | **Interface catalog** (danh mục giao tiếp) | Bản đầy đủ hơn gọi là ICD — Interface Control Document |
| `SEQ-01` | **UML Sequence diagram**, khung pha là **combined fragment** | Tiếng Việt: sơ đồ tuần tự |
| `DATA-01` | **Data architecture diagram** / DFD mức hệ thống (source → ingestion → storage → consumption) | Tiếng Việt: sơ đồ kiến trúc dữ liệu |
| Khung góc phải | **Title block** (khung tên bản vẽ) | Nguồn · phạm vi · tình trạng · mã bản vẽ, phiên bản, ngày |
| Ô / mũi tên đỏ nét đứt | **Gap marking** | Chỗ nguồn không đặc tả hoặc để ngoài phạm vi |
| "Hiện trạng" / "Trạng thái đích" | **As-is / To-be architecture** | Luôn ghi rõ bản vẽ thuộc loại nào |

---

## Nguyên tắc (đừng quên — đã trả giá để rút ra)

1. **Bắt đầu từ câu hỏi người đọc cần trả lời, không từ khuôn.** Chọn loại bản vẽ theo câu hỏi (bảng dưới). Khuôn trong `templates/` chỉ là điểm khởi đầu về kỹ thuật vẽ, không phải hình dạng bắt buộc.
2. **Sơ đồ kiến trúc = thành phần + ranh giới + QUAN HỆ.** Không có mũi tên thì không phải sơ đồ kiến trúc.
3. **Màu = ai sở hữu** (tự xây / mua / bên thứ ba), không phải tầng kỹ thuật, không phải brand.
4. **Chi tiết nằm ở bảng danh mục, không nhồi vào hình.** Mũi tên mang số + nhãn tối đa 4–5 từ.
5. **Đúng tầng chi tiết.** ARCH: tên thành phần + 1–2 dòng việc nó làm. Không liệt kê tên bảng, tên trường (đó là việc của DATA hoặc ERD).
6. **KHÔNG bịa.** Nguồn không nói → ô / mũi tên đỏ nét đứt, ghi "chưa đặc tả". Hiện trạng (đang chạy / đang xây / chưa có) chỉ ghi khi nguồn có nêu.
7. **Nguồn chưa QC thì ghi "chưa QC" ngay trên khung tên bản vẽ.**

| Người đọc hỏi | Vẽ |
|---|---|
| Hệ thống gồm những gì, ai giữ dữ liệu gì, cái nào nối cái nào? | `ARCH` |
| Một việc (đặt hàng, tạo booking…) chạy qua những bước nào? | `SEQ` |
| Dữ liệu từ đâu vào, nằm đâu, ra báo cáo gì? | `DATA` |
| Chỉ cần 1 hình đẹp cho slide, không cần đúng chuẩn | `--quick` (bản cũ) |

Mặc định vẽ đủ `ARCH` + `SEQ`; thêm `DATA` khi có kho dữ liệu / báo cáo.

---

## Workflow

### Bước 0 — Scope
Hệ nào, nguồn nào (tài liệu, repo, transcript), bản vẽ là hiện trạng hay trạng thái đích. Không rõ → hỏi 1 câu gọn.

⚠️ **Client isolation:** folder client thì chỉ vẽ khi đang làm trong đó. Không đưa secret vào sơ đồ. **Không tự publish** (host web, gửi link) — chỉ làm khi user bảo.

### Bước 1 — Gather fact THẬT rồi viết INVENTORY
Đọc tài liệu / code. Hệ lớn hoặc lạ → spawn agent gather, bắt cite nguồn từng dòng. Viết ra (trong đầu hoặc nháp) trước khi đặt toạ độ:

- **Người dùng**: ai, dùng cái gì.
- **Thành phần**: tên · ai sở hữu (tự xây / mua / bên thứ ba) · công nghệ · hiện trạng nếu nguồn nêu.
- **Kho dữ liệu**: cái gì là nguồn sự thật cho dữ liệu nào.
- **Giao tiếp**: từ → đến · kiểu (đồng bộ / sự kiện / webhook / thủ công / trích xuất) · nội dung · tham chiếu mục trong nguồn.
- **Khoảng trống**: nguồn không nói gì về cái gì. Đây là thứ có giá trị nhất với người đọc, đừng bỏ.

### Bước 2 — Lấy bộ đồ nghề
Copy 3 file vào thư mục bản vẽ của dự án (vd `<project>/arch-diagram/` hoặc theo cấu trúc thư mục của dự án):

```
lib/archkit.py            # khung vẽ SVG: box, person, cyl, boundary, arrow, badge, legend, seq(), catalog(), page()
lib/render_png.py         # chụp toàn trang bằng Chrome headless (macOS / Windows / Linux)
templates/build_views.py  # khuôn khởi đầu có ví dụ đủ 3 bản vẽ — THAY HẾT nội dung ví dụ
```

Copy vào dự án (không import từ thư mục skill) để thư mục bản vẽ tự chạy được về sau.

### Bước 3 — Dựng
Sửa `build_views.py` theo inventory. Toạ độ đặt tay. Luật bố cục + API của `archkit` ở `reference/notation.md`. Tóm tắt:

- Xếp cột sao cho hai hệ nói chuyện với nhau **nằm cạnh nhau** → mũi tên thẳng, không cắt nhau.
- Người dùng đặt **ngay trên** thứ họ dùng.
- Mỗi giao tiếp một số; số đó có 1 dòng trong bảng danh mục.
- Mũi tên ngắn hơn ~120px: chỉ đánh số, không ghi nhãn.
- Nhãn ranh giới đặt **ở đáy** (`bottom=True`) khi có mũi tên đi vào từ phía trên.

### Bước 4 — Build, render, SOI
```bash
python3 build_views.py
```
```bash
python3 render_png.py arch-01.html arch-01.png
```
**Bắt buộc Read PNG** trước khi báo xong. Checklist:

- [ ] Không chữ nào tràn ô, không ô nào đè ô.
- [ ] Không mũi tên nào cắt qua nhãn hoặc qua ô không liên quan.
- [ ] Mọi số trên hình có dòng trong bảng danh mục, và ngược lại.
- [ ] Chú giải khớp với màu và kiểu mũi tên thật sự dùng.
- [ ] Khung tên bản vẽ đủ: nguồn, phạm vi (hiện trạng / đích), tình trạng, mã · phiên bản · ngày.
- [ ] Chỗ nguồn không nói đã được tô đỏ, không bị lấp bằng suy đoán.
- [ ] Không còn nội dung ví dụ của khuôn ("Cửa hàng online").

Sai thì sửa toạ độ, build lại, soi lại. Thường mất 2–3 vòng.

### Bước 5 — Output
Trong thư mục bản vẽ: `*.html` · `*.png` · `build_views.py` · `archkit.py` · `render_png.py` · `README.md` (bản vẽ nào trả lời câu hỏi gì, cách đọc ký pháp, cách build lại). Trả link file. Không tự publish.

---

## Ký pháp

| Ô (`kind`) | Nghĩa | Hình |
|---|---|---|
| `person` | Người dùng | Vàng, bo tròn, có icon người |
| `build` | Tự xây | Tím nhạt, viền tím |
| `module` | Thành phần bên trong hệ tự xây | Trắng, viền tím |
| `saas` | Mua / SaaS do mình vận hành | Xanh lá nhạt |
| `ext` | Bên thứ ba | Xám |
| `gap` | Chưa đặc tả / ngoài phạm vi | Đỏ nhạt, viền đỏ nét đứt |
| `cyl()` | Kho dữ liệu | Hình trụ |
| `boundary()` | Ranh giới hệ thống / nhóm | Khung nét đứt, nhãn chữ hoa |

| Mũi tên (`style`) | Nghĩa |
|---|---|
| `sync` | Gọi đồng bộ (API) — nét liền |
| `async` | Sự kiện / webhook — nét đứt |
| `manual` | Thủ công (người chuyển tay) — nét chấm |
| `use` | Người dùng sử dụng — xám mảnh |
| `ret` | Kết quả trả về (sequence) — đứt, đầu hở |
| `gap` | Chưa đặc tả — đỏ nét đứt |

Dòng trong ngoặc vuông dưới tên ô (`tech=`) = công nghệ và hiện trạng, vd `[Laravel · đang xây]`, `[SaaS · CHƯA triển khai]`.

---

## `--quick` — infographic 1 màn (bản v1)
Chỉ khi user nói rõ cần "infographic nhanh" / "1 hình cho slide". Fork `templates/architecture-landscape.html` (4 cột + 1 dải key-flow, khổ 1500×858). Không gọi nó là sơ đồ kiến trúc. Không dùng làm mặc định.

## Máy & công cụ
- Python 3 (không cần thư viện ngoài) + Chrome. `render_png.py` tự tìm Chrome trên macOS / Windows / Linux.
- macOS: Chrome headless chụp xong không tự thoát → `render_png.py` đã bọc timeout, đừng gọi Chrome trần.
- `d2` không bắt buộc ở v2.
- Chi tiết render + lỗi hay gặp: `reference/render.md`.

## Khi nào dùng skill nào
- `/tool-diagram` → bộ bản vẽ kiến trúc để đọc hiểu, review, bàn với dev / client.
- `ARCHITECTURE.md` (markdown + mermaid) nằm trong repo cho dev onboard → viết mermaid, không cần skill này.
- Trang HTML trình bày nội dung thường (không phải sơ đồ) → không cần skill này.

## Ví dụ đầy đủ
`examples/ai-code-system-map/` — bản đồ AI code + VPS + Cloudflare + API cho người không code: ARCH-01 (14 giao tiếp, badge tách 2 luồng XÂY / CHẠY, ô "hay bị quên"), SEQ-01 (2 pha), kèm bảng so sánh và checklist trên cùng trang. Xem để tham khảo mức chi tiết và cách mở rộng trang (thêm section HTML dưới sơ đồ), không copy nội dung.
