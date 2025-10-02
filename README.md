# 📊 Đồ án Quản lý Chi tiêu Cá nhân - Môn học Python

Đây là đồ án kết thúc học phần Python tại trường Đại học An Giang.

- **Sinh viên thực hiện:** Nguyễn Phi Hùng
- **Mã số sinh viên:** DTH235659

---

## 📝 Tổng quan

Hệ thống quản lý tài chính cá nhân được xây dựng bằng **FastAPI** (backend REST API) và **PySide6** (desktop frontend), với **SQLAlchemy** (ORM) và PostgreSQL (cơ sở dữ liệu).

Dự án giúp người dùng ghi lại, phân loại và phân tích các khoản chi tiêu của mình.

## 🛠 Công nghệ sử dụng

- **Backend:** FastAPI + SQLAlchemy + Pydantic (Python 3.12)
- **Frontend:** PySide6 (Qt for Python) - Ứng dụng desktop cho Ubuntu
- **Database:** PostgreSQL
- **API Docs:** FastAPI tự động tạo tài liệu tại `/docs`

## 📂 Cấu trúc Dự án

```
DTH235659_NguyenPhiHung_DoAn_Python/
├── README.md
├── requirements.txt
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── database.py
│       ├── models.py
│       ├── schemas.py
│       ├── crud.py
│       ├── deps.py
│       ├── routers/
│       │   ├── categories.py
│       │   └── expenses.py
│       └── services/
│           └── ai_client.py
├── frontend_pyside6/
│   ├── main.py
│   ├── api_client.py
│   └── requirements.txt
└── .env.example
```

## 📌 Tính năng

- Quản lý người dùng (CRUD).
- Quản lý danh mục chi tiêu (CRUD, toàn cục).
- Ghi lại chi tiêu (CRUD + lọc theo người dùng, danh mục, ngày).
- Quản lý ngân sách (CRUD).
- Tài liệu API tự động với Swagger UI.

## 🔧 Hướng dẫn chạy dự án

### Chuẩn bị môi trường

1. Tạo virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # hoặc .venv\Scripts\activate  # Windows
   ```

2. Cài đặt dependencies cho backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Cài đặt dependencies cho frontend:
   ```bash
   cd ../frontend_pyside6
   pip install -r requirements.txt
   ```

### Chạy Backend (FastAPI)

1. Thiết lập biến môi trường:
   - Sao chép `.env.example` thành `.env`
   - Cập nhật `DATABASE_URL` với thông tin PostgreSQL của bạn.

2. Chạy server:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

API sẽ chạy tại `http://localhost:8000`. Tài liệu API tại `http://localhost:8000/docs`.

### Chạy Frontend (PySide6)

1. Chạy ứng dụng:
   ```bash
   cd frontend_pyside6
   python main.py
   ```

## 📡 API Endpoints

- **Categories:**
  - `GET /categories/` - Liệt kê danh mục
  - `POST /categories/` - Tạo danh mục
  - `GET /categories/{id}` - Lấy danh mục
  - `PUT /categories/{id}` - Cập nhật danh mục
  - `DELETE /categories/{id}` - Xóa danh mục

- **Expenses:**
  - `GET /expenses/?user_id={id}&category_id={id}&date_from=2023-01-01&date_to=2023-12-31` - Liệt kê chi tiêu với bộ lọc
  - `POST /expenses/` - Tạo chi tiêu
  - `GET /expenses/{id}` - Lấy chi tiêu
  - `PUT /expenses/{id}` - Cập nhật chi tiêu
  - `DELETE /expenses/{id}` - Xóa chi tiêu

## 🚀 Triển khai Production

- Sử dụng PostgreSQL cho production.
- Chạy `uvicorn app.main:app --host 0.0.0.0 --port 8000` cho production.
- Thêm xác thực nếu cần (JWT, OAuth).
