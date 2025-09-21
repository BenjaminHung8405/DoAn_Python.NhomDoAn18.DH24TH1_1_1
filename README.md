# 📊 Đồ án Quản lý Chi tiêu Cá nhân - Môn học Python

Đây là đồ án kết thúc học phần Python tại trường Đại học An Giang.

- **Sinh viên thực hiện:** Nguyễn Phi Hùng
- **Mã số sinh viên:** DTH235659

---

## 📝 Tổng quan

Hệ thống quản lý tài chính cá nhân được xây dựng bằng Django (backend) và PostgreSQL (cơ sở dữ liệu trên cloud).
Dự án giúp người dùng ghi lại, phân loại và phân tích các khoản chi tiêu của mình.
Trong tương lai, dự án sẽ được tích hợp với AI (Gemini API) và Telegram Bot để cung cấp các tính năng thông minh và tương tác qua chat.

## 🛠 Công nghệ sử dụng

- **Backend:** Django 5 (Python 3.12)
- **Cơ sở dữ liệu:** PostgreSQL (lưu trữ trên Neon cloud)
- **Frontend:** Django templates (giao diện cơ bản), có thể mở rộng với React/Vue trong tương lai.
- **Tích hợp AI:** Gemini API (phân tích văn bản, đưa ra gợi ý)
- **Tích hợp Bot:** Telegram Bot API
- **Trực quan hóa dữ liệu:** Matplotlib / Plotly (Biểu đồ tròn & cột)

## 📂 Cấu trúc Dự án

- `expenses/models.py`: Định nghĩa các model chính (User, Category, Expense).
- `expenses/views.py`: Xử lý logic cho các chức năng CRUD (Thêm, Sửa, Xóa, Xem) và trang tổng quan.
- `expenses/templates/`: Chứa các file HTML cho giao diện.
- `config/settings.py`: Cấu hình Django, kết nối PostgreSQL và quản lý biến môi trường.

## 📌 Tính năng

- Quản lý người dùng (đăng nhập cơ bản, liên kết với `chat_id` trên Telegram).
- Quản lý danh mục chi tiêu (mỗi người dùng có danh mục riêng).
- Ghi lại chi tiêu (số tiền, ngày tháng, ghi chú, danh mục).
- Trang tổng quan (Dashboard) hiển thị tổng chi tiêu và số lượng giao dịch.
- **Trực quan hóa dữ liệu:**
  - Biểu đồ tròn: Tỷ lệ chi tiêu theo từng danh mục.
  - Biểu đồ cột: Thống kê chi tiêu theo ngày/tuần/tháng.
- Xuất dữ liệu chi tiêu ra file CSV/Excel.
- **Tính năng AI (Sprint 3):**
  - Tự động phân loại chi tiêu dựa trên mô tả.
  - Gợi ý tiết kiệm thông minh dựa trên lịch sử chi tiêu.
- **Telegram Bot (Sprint 4):**
  - Lệnh `/add`: Thêm một khoản chi tiêu mới.
  - Lệnh `/report`: Nhận báo cáo tóm tắt chi tiêu.

## 🔧 Hướng dẫn chạy dự án khi clone về máy (local setup)

Phần này mô tả các bước cần thiết để chạy project `Expense Tracker` trên máy local sau khi bạn clone repository.

### Yêu cầu trước
- Python 3.12 (khuyến nghị) đã cài đặt và có thể gọi bằng `python` hoặc `python3`.
- Git
- **PostgreSQL (Neon) — project được cấu hình để dùng PostgreSQL trên cloud thông qua biến môi trường `DATABASE_URL`.**
  - Trong môi trường production / staging, bạn nên cung cấp `DATABASE_URL` (ví dụ Neon). Project sẽ sử dụng PostgreSQL khi `DATABASE_URL` được thiết lập.
  - Nếu bạn không cung cấp `DATABASE_URL` (ví dụ khi thử nhanh trên máy dev), project sẽ tự động fallback sang SQLite (`db.sqlite3`) cho mục đích phát triển.

### 1) Clone repository
```bash
git clone https://github.com/BenjaminHung8405/DTH235659_NguyenPhiHung_DoAn_Python.git
cd expense_tracker
```

### 2) Tạo và kích hoạt virtual environment
Chạy trong bash (Windows Git Bash / WSL / macOS / Linux):
```bash
python -m venv .venv
# Unix-like
source .venv/bin/activate
# Hoặc trên Windows (Git Bash / Powershell):
source .venv/Scripts/activate
```

(Chú ý: nếu `source .venv/Scripts/activate` không hoạt động trong terminal của bạn, mở PowerShell và dùng `\.venv\Scripts\Activate.ps1` hoặc `\.venv\Scripts\activate`.)

### 3) Cài dependency
Nếu repository có file `requirements.txt` (nếu không, cài các gói sau):
```bash
# Nếu có requirements.txt
pip install -r requirements.txt
# Nếu không có, cài tối thiểu:
pip install "Django>=5.0" psycopg2-binary python-dotenv
```

> Lưu ý: `psycopg2-binary` là driver PostgreSQL phổ biến. Nếu bạn gặp lỗi khi cài, thử cài bản phù hợp với hệ điều hành hoặc cài các build tools cần thiết.

### 4) Cấu hình biến môi trường (BẮT BUỘC cho cloud PostgreSQL)
Project được cấu hình để dùng biến môi trường `DATABASE_URL` để kết nối tới PostgreSQL (ví dụ Neon). Hãy export các biến sau trước khi chạy ứng dụng trong môi trường muốn dùng PostgreSQL:

- `DATABASE_URL` — chuỗi kết nối tới Postgres, ví dụ:
```
postgres://USER:PASSWORD@HOST:PORT/DBNAME
```
- `SECRET_KEY` — secret key Django (production)
- `DEBUG` — 0 hoặc 1

Ví dụ (Unix / WSL / macOS / Git Bash):
```bash
export DATABASE_URL="postgres://db_user:secret@ep-somehost.neon.tech:5432/dbname"
export SECRET_KEY="a-very-secret-key"
export DEBUG=1
```
Trên PowerShell (Windows):
```powershell
$env:DATABASE_URL = "postgres://db_user:secret@ep-somehost.neon.tech:5432/dbname"
$env:SECRET_KEY = "a-very-secret-key"
$env:DEBUG = "1"
```

> Nếu bạn không thiết lập `DATABASE_URL`, project sẽ sử dụng SQLite (`db.sqlite3`) như một fallback cho phát triển local. Tuy nhiên vì repository được triển khai với PostgreSQL (Neon) trong môi trường cloud, **nên** cung cấp `DATABASE_URL` khi mô phỏng môi trường thực tế.

**Gợi ý:** tạo file `.env` chứa các biến trên và dùng `python-dotenv` (project đã có logic load `.env` nếu tồn tại) để nạp tự động.

### 5) Chạy migrations (tạo schema trên DB)
```bash
python manage.py makemigrations
python manage.py migrate
```
- `makemigrations` tạo file migrations khi bạn thay model.
- `migrate` áp dụng migrations lên DB.

### 6) Tạo superuser (tùy chọn, để vào /admin/)
```bash
python manage.py createsuperuser
# điền username, email (nếu cần) và password
```

### 7) Chạy server phát triển
```bash
python manage.py runserver
```
Mở trình duyệt tới `http://127.0.0.1:8000/`.

### 8) Kiểm tra nhanh (debug)
- Kiểm tra cấu hình dự án:
```bash
python manage.py check
```
- Vào Django shell để kiểm tra model / dữ liệu:
```bash
python manage.py shell
>>> from expenses.models import User, Expense, Category
>>> User.objects.all()
```

### Ghi chú & troubleshooting
- Project mặc định dùng PostgreSQL khi `DATABASE_URL` được set (phù hợp với Neon cloud setup). SQLite chỉ là fallback cho trường hợp bạn muốn chạy nhanh trên máy dev.
- Nếu bạn dùng PostgreSQL và gặp lỗi khi cài `psycopg2-binary`, hãy cài gói build tools tương ứng cho hệ điều hành hoặc dùng phiên bản `psycopg2-binary` tương thích.
- Nếu thay đổi `AUTH_USER_MODEL` sau khi đã migrate thì sẽ rất phức tạp; tránh thay đổi nếu DB production đã dùng.
- Đảm bảo `SECRET_KEY` không được commit vào git khi deploy (dùng biến môi trường cho production).
- Trong quá trình phát triển, bạn có thể tạm dùng SQLite để thử nhanh, nhưng môi trường staging/production nên sử dụng PostgreSQL (Neon) giống môi trường thật.

---
Mình đã cập nhật README để phản ánh rõ ràng rằng project được cấu hình dùng cloud PostgreSQL (Neon) qua `DATABASE_URL`, với SQLite chỉ là fallback cho local dev. Muốn mình thêm file `.env.example` và/hoặc `requirements.txt` tự động không?
