# Amplify Music Player - PostgreSQL Version

Phiên bản mirror của Amplify Music Player sử dụng PostgreSQL (Neon) thay vì Firebase.

## Tính năng chính

- 🎵 Phát nhạc với giao diện đẹp mắt
- 👤 Đăng ký/Đăng nhập người dùng (không cần email verification)
- 🎨 Duyệt nhạc theo: Nghệ sĩ, Thể loại, Ngôn ngữ
- ❤️ Like/Unlike bài hát
- 🔍 Tìm kiếm bài hát
- 📊 Trending songs

## Yêu cầu hệ thống

- Python 3.8+
- PostgreSQL database (khuyến nghị: Neon)
- Tkinter (thường đã cài sẵn với Python)

## Cài đặt

### 1. Clone repository

```bash
git clone <repository-url>
cd DTH235659_NguyenPhiHung_DoAn_Python
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Thiết lập database

#### Tạo database trên Neon:
1. Truy cập https://neon.tech
2. Tạo project mới
3. Copy connection string

#### Tạo schema:

```bash
# Kết nối với database và chạy schema
psql "postgresql://user:password@host/database" < sql/schema.sql
```

### 4. Cấu hình

Tạo file `.env` từ `.env.example`:

```bash
cp .env.example .env
```

Sửa file `.env` và điền connection string của bạn:

```
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

### 5. Chuẩn bị assets

Copy các file images từ Amplify-master:

```bash
cp -r ../Amplify-master/images/* images/
cp -r ../Amplify-master/fonts/* fonts/
```

## Chạy ứng dụng

```bash
python main.py
```

## Cấu trúc database

### Users
- user_id (PK)
- display_name
- email (unique)
- password_hash (SHA256)
- phone_number
- created_at

### Tracks
- track_id (PK)
- title
- artist
- genre
- location (file path/URL)
- language
- like_count
- created_at

### Artists
- artist_id (PK)
- name (unique)
- image_url

### Genres
- genre_id (PK)
- genre_name (unique)
- genre_image

### Languages
- language_id (PK)
- language_name (unique)
- language_image

## Sự khác biệt với Amplify-master

1. **Database**: PostgreSQL (Neon) thay vì Firebase Firestore
2. **Authentication**: Đơn giản hóa - không cần email verification và OTP
3. **Password**: Sử dụng SHA256 hash
4. **Connection**: Sử dụng connection string thay vì service key JSON

## Troubleshooting

### Lỗi kết nối database
- Kiểm tra connection string trong `.env`
- Đảm bảo database đã được tạo và schema đã được import
- Kiểm tra firewall/network access trên Neon

### Lỗi import images
- Đảm bảo đã copy tất cả images từ Amplify-master
- Kiểm tra đường dẫn trong code (Windows: `\`, Linux/Mac: `/`)

### Lỗi dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## License

MIT License (same as Amplify-master)

## Credits

Based on [Amplify Music Player](https://github.com/original-repo)
Modified by: Nguyễn Phi Hùng
