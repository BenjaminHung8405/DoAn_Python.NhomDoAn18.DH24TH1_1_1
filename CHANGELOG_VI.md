# Nhật Ký Thay Đổi (Changelog)

Tất cả các thay đổi quan trọng của dự án sẽ được ghi lại trong file này.

## [2.1.0] - 2025-01-06

### ✨ Tính Năng Mới
- Chuyển đổi toàn bộ chú thích code sang tiếng Việt
- Thêm script `translate_comments.py` để tự động chuyển đổi chú thích
- Cập nhật README.md sang tiếng Việt đầy đủ
- Thêm tài liệu `MIGRATION_FIREBASE_TO_POSTGRESQL.md`

### 🔧 Sửa Lỗi
- Sửa lỗi `get_user()` không trả về password cho UserPage
- Sửa lỗi window maximization trên Linux (`state('zoomed')`)
- Sửa lỗi Pillow 10+ (`Image.ANTIALIAS` → `Image.LANCZOS`)
- Sửa lỗi theme compatibility (thay `theme_settings` bằng `style.map`)

### 📝 Tài Liệu
- Cập nhật README với hướng dẫn cài đặt PostgreSQL
- Thêm schema database PostgreSQL chi tiết
- Cập nhật thông tin nhóm và liên hệ
- Thêm roadmap phát triển tương lai

## [2.0.0] - 2025-01-05

### 🚀 Thay Đổi Lớn
- **Migration từ Firebase sang PostgreSQL (Neon)**
  - Chuyển từ Firestore sang PostgreSQL serverless
  - Tạo connection pool để quản lý kết nối
  - Thêm SSL mode và timeout cho PostgreSQL
  - Tạo Firebase admin shim để tương thích với code cũ

### ✨ Tính Năng Mới
- Thêm Firestore emulator cho PostgreSQL
- Script `reset_schema.py` để reset database
- Thêm messagebox thông báo đăng ký thành công
- Hỗ trợ đa nền tảng (Windows/Linux/macOS)

### 🔧 Database
- Tạo 8 bảng chính: users, tracks, artists, genres, languages, albums, albums_tracks, user_likes
- Thêm connection pooling với psycopg2
- Tối ưu truy vấn với indexes
- SSL/TLS encryption cho kết nối database

### 📦 Dependencies
- Thêm `psycopg2-binary` cho PostgreSQL
- Thêm `python-dotenv` cho quản lý biến môi trường
- Cập nhật `Pillow` lên phiên bản 12.0.0
- Loại bỏ `firebase-admin`, `scipy`, `scikit-image`

### 🐛 Sửa Lỗi
- Sửa lỗi email verification bypass
- Sửa lỗi password authentication
- Sửa lỗi cross-platform paths (Windows backslash)
- Sửa nhiều lỗi TypeError và NameError

## [1.0.0] - 2024-04-27

### ✨ Tính Năng Ban Đầu
- Phát nhạc trực tuyến
- Đăng ký/Đăng nhập với Firebase
- Like/Unlike bài hát
- Tìm kiếm bài hát
- Hiển thị nghệ sĩ và thể loại
- Giao diện Tkinter

### 🛠️ Công Nghệ
- Python 3.x
- Firebase Firestore
- Tkinter GUI
- Pygame audio player

---

## Quy Ước Ghi Chú

- ✨ `Tính Năng Mới` - Tính năng mới được thêm vào
- 🔧 `Sửa Lỗi` - Sửa lỗi bug
- 🚀 `Thay Đổi Lớn` - Thay đổi breaking changes
- 📝 `Tài Liệu` - Cập nhật tài liệu
- 📦 `Dependencies` - Thay đổi dependencies
- 🐛 `Bug Fixes` - Sửa lỗi nhỏ
- 🎨 `Style` - Thay đổi style/formatting
- ⚡ `Performance` - Cải thiện hiệu suất
- 🔒 `Security` - Bảo mật

## Đóng Góp

Mọi đóng góp đều được chào đón! Vui lòng đọc [CONTRIBUTING.md](CONTRIBUTING.md) để biết thêm chi tiết.

## Liên Hệ

- GitHub: [BenjaminHung8405](https://github.com/BenjaminHung8405)
- Email: amplifyteam1234@gmail.com
