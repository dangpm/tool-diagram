# tool-diagram — Render & lỗi hay gặp

## 1. Bản v2 (mặc định): `lib/render_png.py`

```bash
python3 render_png.py <file.html> <out.png> [width=1850] [scale=2]
```

- Tự tìm Chrome (macOS / Windows / Linux), tự đo chiều cao trang, chụp toàn trang.
- `width` = bề rộng SVG + ~60. Sơ đồ rộng 1790 → 1850. Sơ đồ rộng 1280 → 1340.
- `scale=2` cho ảnh nét để đưa vào tài liệu; `1.1–1.4` khi chỉ cần soi nhanh (file nhẹ, đọc nhanh hơn).
- Dùng `--user-data-dir` riêng trong thư mục tạm, không đụng Chrome đang mở của bạn.

**Luôn Read PNG sau khi render.** Trang cao (sequence dài) thì render scale thấp để soi tổng thể, cần đọc chữ nhỏ thì cắt vùng:
```bash
sips -c <cao> <rộng> --cropOffset <y> <x> in.png --out crop.png
```

## 2. Lỗi hay gặp

| Triệu chứng | Nguyên nhân | Sửa |
|---|---|---|
| Lệnh Chrome treo tới hết timeout (macOS) | Chrome headless chụp xong không tự thoát | Dùng `render_png.py` (đã bọc timeout). Đừng gọi Chrome trần. Lỡ treo thì dừng bằng TaskStop, **không `pkill` theo tên** |
| Chữ ra font serif | Google Fonts chưa tải kịp | Tăng `--virtual-time-budget` trong `render_png.py` (5000 → 8000) |
| Ảnh có khoảng trắng lớn phía dưới | Đo chiều cao sai | Kiểm `data-h` trong `render_png.py`; trang phải reset `margin` của `body` |
| Dòng trống trong ô bị dính lại | tspan rỗng không chiếm chiều cao | Đã xử lý trong `archkit` (dòng `''` → khoảng trắng cứng) |
| Nhãn bị mũi tên cắt | Nhãn ranh giới ở trên trong khi mũi tên đi vào từ trên | `bottom=True`, hoặc dời `lpos` |
| Chữ tràn ô | Ước lượng bề rộng sai | Nới ô hoặc ngắt dòng tay; ~6px / ký tự ở cỡ 10.5 |
| Bản online vẫn hiện ảnh cũ sau khi đẩy lại | host / CDN giữ cache file `.png/.css/.js` | Đổi tên file ảnh mỗi lần cập nhật (`arch-01-v2.png`) |

## 3. Bản `--quick` (v1, infographic 1 màn)

Khổ cố định 1500×858. Trên Windows:
```powershell
$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
& $chrome --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 `
  --window-size=1500,858 --virtual-time-budget=5000 --screenshot="<out>.png" "file:///<abs-path>.html"
```
Trên macOS dùng `render_png.py <file.html> <out.png> 1500 2` cho khỏi treo.

D2 (`d2 --theme 0 --layout elk`) chỉ còn là bước nháp tuỳ chọn của bản `--quick`; không bắt buộc cài.
