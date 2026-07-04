# 🧋 NLP Hub — Dự án Phân phối Nguyên liệu Pha chế (Xuân Lộc – Đồng Nai)

Gói dự án hoàn chỉnh: **website tổng hợp** + **agent nghiên cứu có bộ nhớ** + **script thu thập tin thời gian thực**, đóng gói từ toàn bộ quá trình nghiên cứu (07/2026).

## 📁 Cấu trúc

```
du-an-nguyen-lieu/
├── index.html              ← WEBSITE dashboard (1 FILE DUY NHẤT — ảnh đã nhúng sẵn bên trong,
│                              mở ở đâu cũng hiển thị, kể cả gửi qua Zalo/copy sang máy khác)
├── images/                 ← 10 ảnh gốc chất lượng cao (dùng riêng để in ấn, đăng bài, chào hàng)
├── README.md               ← File này
├── agent/
│   ├── system-prompt.md    ← "Bộ não" agent — dán vào Arena.ai/ChatGPT/Claude
│   ├── memory.json         ← "Bộ nhớ" agent — toàn bộ tri thức dự án, cập nhật dần
│   └── collector.py        ← Script Python kéo tin Google News theo từ khóa ngành
└── data/
    ├── bao-cao-do-uong-nguyen-lieu.md            ← Nghiên cứu xu hướng + nguồn nguyên liệu
    ├── phan-tich-mo-hinh-phan-phoi-nguyen-lieu.md ← Phân tích khả thi mô hình NPP
    ├── danh-muc-nguyen-lieu-chi-tiet.md          ← Danh mục hàng: nội địa vs nhập khẩu + giá
    ├── danh-ba-nha-cung-cap.md                   ← Danh bạ liên hệ nhà cung cấp đã xác minh
    └── news-YYYY-MM-DD.md                        ← (tự sinh khi chạy collector.py)
```

## 🌐 1. Dùng website

- **Xem ngay:** mở `index.html` bằng trình duyệt (đúp chuột). Có 6 tab: Tổng quan · Xu hướng · **Nguyên liệu (10 ảnh trực quan ngay đầu tab — bấm phóng to, lọc theo 🇻🇳/🌏/🔥 + bảng chi tiết)** · Nhà cung cấp (lọc tìm được) · Kế hoạch 90 ngày · Agent.
- **Đưa lên mạng miễn phí:**
  - Cách 1 (dễ nhất): vào **netlify.com/drop** → kéo-thả cả thư mục `du-an-nguyen-lieu` → nhận link công khai sau 30 giây.
  - Cách 2: tạo repo **GitHub** → upload thư mục → Settings → Pages → chọn nhánh `main` → link dạng `tenban.github.io/du-an`.

## 🤖 2. Dùng Agent có bộ nhớ (không cần code)

1. Mở phiên chat mới trên **Arena.ai** (hoặc AI nào có tìm kiếm web).
2. Dán toàn bộ `agent/system-prompt.md`, rồi dán tiếp `agent/memory.json`.
3. Ra lệnh, ví dụ:
   - `/tuan` — quét tin 7 ngày + biến động giá + 3 việc cần làm
   - `/gia bột kem béo Frima` — tra giá mới nhất, so với bộ nhớ
   - `/ncc Gia Thịnh Phát` — thẩm định nhà cung cấp
   - `/trend` — 5 món viral + nguyên liệu cần trữ để đón trend
4. Cuối phiên gõ `/memory` → agent xuất `memory.json` bản mới → **copy lưu đè file cũ**. Phiên sau dán bản mới này, agent "nhớ" mọi thứ đã làm.

> 💡 Bộ nhớ chính là file `memory.json` — nó lưu: quyết định đã chốt, danh mục hàng + giá, danh bạ NCC (kèm trạng thái đã liên hệ chưa), xu hướng, nhật ký hành động, câu hỏi tồn đọng.

## ⚙️ 3. Thu thập tin tự động theo thời gian thực

Yêu cầu: Python 3.8+ (miễn phí tại python.org).

```bash
pip install requests          # cài 1 lần
python agent/collector.py     # chạy — kết quả lưu vào data/news-YYYY-MM-DD.md
```

Tự động mỗi sáng 7h:
- **Windows:** Task Scheduler → Create Basic Task → Daily 07:00 → Start a program: `python` + arguments `agent\collector.py` + start in: thư mục dự án.
- **Linux/Mac:** `crontab -e` thêm dòng: `0 7 * * * cd /duong/dan/du-an-nguyen-lieu && python agent/collector.py`

Sau đó dán file `news-...md` vào phiên agent để tóm tắt & cập nhật bộ nhớ.

*(Từ khóa theo dõi chỉnh trong biến `KEYWORDS` đầu file collector.py — thêm bớt tùy nhu cầu.)*

## ✅ Việc cần làm ngay (theo memory.json)

1. Gọi hẹn 3 nhà cung cấp: **Gia Thịnh Phát** 1900 299 948 · **P-Taste** 0789 838 858 · **Linh Đan** 0902 499 377
2. Lên lịch 1 chuyến TP.HCM (lộ trình chi tiết trong tab "Nhà cung cấp" của website)
3. Trước khi ký bất kỳ hợp đồng nào: tra giấy phép ATTP tại **nghidinh15.vfa.gov.vn**

---
*⚠️ Giá cả & địa chỉ trong dữ liệu là thông tin công khai tại thời điểm nghiên cứu (07/2026) — luôn gọi xác nhận trước khi giao dịch.*
