# Dự án: Spotify Clone - Ứng dụng quản lý âm nhạc

Đồ án học phần Python

- Thành viên: **DTH235659 - Nguyễn Phi Hùng**

Mô tả ngắn: Đây là đồ án mô phỏng một ứng dụng quản lý âm nhạc (Spotify clone). Dự án gồm một backend REST API (FastAPI + SQLAlchemy + JWT) để quản lý người dùng, danh mục, chi tiêu (mô phỏng dữ liệu âm nhạc có thể mở rộng), và một frontend desktop viết bằng PySide6 làm giao diện người dùng.

Mục tiêu:
- Thực hành xây dựng API với FastAPI và ORM (SQLAlchemy).
- Thực hành xác thực (JWT), lưu trữ token, và gọi API từ frontend.
- Tạo giao diện desktop bằng PySide6.

Tính năng chính (hiện có / có thể mở rộng):
- Đăng ký tài khoản, đăng nhập (JWT)
- Quản lý danh mục (categories)
- Quản lý bản ghi (expenses) — trong đồ án này được dùng để mô phỏng các mục âm nhạc / giao dịch
- Frontend desktop (PySide6) với form đăng nhập/đăng ký và tích hợp gọi API

Yêu cầu hệ thống
- Python 3.10+ (hoặc 3.8+ tùy môi trường)
- PostgreSQL nếu dùng DB production / cloud (ví dụ Neon). SQLite có thể dùng cho phát triển cục bộ nếu cấu hình lại.

Cài đặt & chạy (người chấm/giáo viên):

1) Backend

```bash
# vào thư mục backend
cd backend

# (tạo và kích hoạt virtualenv - khuyến nghị)
python3 -m venv .venv
source .venv/bin/activate

# cài dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# cấu hình biến môi trường (ví dụ dùng .env hoặc export trực tiếp)
# DATABASE_URL=postgresql://user:pass@host:port/dbname
# SECRET_KEY và các biến khác nếu cần

# đồng bộ mô hình lên cơ sở dữ liệu (nếu muốn tạo bảng tự động)
python sync_db.py

# chạy backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

2) Frontend (PySide6 desktop)

```bash
# vào thư mục frontend_pyside6
cd frontend_pyside6

# tạo virtualenv riêng nếu muốn
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# chạy app (chạy dưới dạng package từ thư mục chứa frontend_pyside6)
cd ..  # quay về root của repo
python -m frontend_pyside6.main

# hoặc chạy trực tiếp (nếu bạn đang ở trong frontend_pyside6 và đã cấu hình đúng PYTHONPATH)
python main.py
```

Lưu ý về cấu hình
- `BACKEND_URL`: frontend sẽ đọc biến môi trường `BACKEND_URL` để biết endpoint của backend. Mặc định là `http://localhost:8000`.
- `DATABASE_URL`: backend đọc chuỗi kết nối cơ sở dữ liệu (Postgres). Nếu dùng Neon/hosted Postgres, đảm bảo schema và quyền đã được thiết lập (có thể cần set `search_path` về `public`).

Cấu trúc dự án (mục tiêu tham khảo):

```
README.md
requirements.txt
backend/
    requirements.txt
    app/
        main.py
        routers/
        models.py
        schemas.py
        crud.py
    sync_db.py
frontend_pyside6/
    requirements.txt
    api_client.py
    main.py
    ui/
        login.py
        register.py
```

Gợi ý debugging nhanh
- Nếu backend không kết nối được DB trên Neon: kiểm tra `DATABASE_URL`, username/password, host, port. Kiểm tra schema (Neon có thể tạo schema không phải `public`).
- Nếu `django-admin` hay lệnh CLI khác báo "command not found": đảm bảo bạn cài gói vào cùng Python/virtualenv mà bạn đang dùng (sử dụng `python -m pip install ...`).

Ghi chú học phần
- Đây là một đồ án học phần; mã nguồn nhằm mục đích học tập. Bạn có thể mở rộng dự án để quản lý playlist, streaming metadata, hoặc tích hợp OAuth.

Liên hệ
- Nguyễn Phi Hùng — Mã SV: DTH235659

Phiên bản & Bản quyền
- Không có bản quyền đặc biệt; mã dành cho mục đích học tập.
