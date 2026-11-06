# Bản đồ AI code — bộ bản vẽ cho người không code

Mô hình tham chiếu chung (không vẽ từ 1 hệ cụ thể): AI code trên máy bạn nối với GitHub, VPS, Cloudflare và các API bên ngoài thế nào, khác nocode ở đâu, và những chỗ cần care.

| Bản vẽ | Trả lời câu hỏi |
|---|---|
| `arch-01.html` / `.png` | Hệ gồm những gì, ai giữ gì, cái nào nối cái nào. Kèm danh mục giao tiếp, bảng so sánh nocode · chat AI · AI code, và 8 chỗ cần care |
| `seq-01.html` / `.png` | Lúc XÂY và lúc CHẠY: ai gọi ai, theo thứ tự |

## Cách đọc
- Màu ô = ai sở hữu: vàng người dùng · tím tự xây (code của bạn) · xanh lá thuê / SaaS bạn vận hành · xám bên thứ ba (API) · đỏ nét đứt = hay bị quên, phải tự thêm.
- Badge số tím (1–7) = lúc XÂY · badge chữ xanh (A–G) = lúc CHẠY. Mỗi số có 1 dòng trong danh mục giao tiếp.
- Nét liền = gọi API đồng bộ · nét đứt = webhook báo về · xám mảnh = người dùng sử dụng · đỏ đứt = hay bị quên.

## Build lại
```bash
python3 build_views.py
python3 ../../lib/render_png.py arch-01.html arch-01.png 1460 2
python3 ../../lib/render_png.py seq-01.html seq-01.png 1460 2
```
Sửa nội dung = sửa `build_views.py` (toạ độ đặt tay, xem `../../reference/notation.md`).
