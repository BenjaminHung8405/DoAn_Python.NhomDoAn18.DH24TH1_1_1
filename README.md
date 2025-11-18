[![Contributors][contributors-shield]][contributors-url]
[![Language][Language-shield]][Language-url]
[![Activity][activity-shield]][activity-url]
[![Version][version-shield]][version-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]




<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/app_64.png" alt="Logo" width="80" height="80">
  </a>

  <h2 align="center">Amplify</h2>

  <p align="center">
    An awesome Platform for listening songs.
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://drive.google.com/file/d/1TG90kIOGDsKfBk17zwHMx9bT8tkDvgGx/view?usp=sharing">View Demo</a>
    ·
    <a href="https://github.com/Srajan1122/TK-Player/issues">Report Bug</a>
    ·
    <a href="https://github.com/Srajan1122/TK-Player/issues">Request Feature</a>
  </p>
</p>


<p align="center">
  <img width="640" height="331" src="https://user-images.githubusercontent.com/49261633/80869362-ab5e1a00-8cbd-11ea-989a-f1df198f49c9.gif">
</p>

<!-- TABLE OF CONTENTS -->


## Table of Contents

* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)



<!-- BẮT ĐẦU -->
## Bắt Đầu

### 📋 Yêu Cầu Hệ Thống

* **Python 3.13 trở lên**
* **PostgreSQL database** (hoặc sử dụng Neon serverless)
* **Internet connection** để stream nhạc

### ⚙️ Cấu Trúc Database PostgreSQL

```sql
-- Bảng users (người dùng)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    display_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng tracks (bài hát)
CREATE TABLE tracks (
    track_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    language VARCHAR(50),
    location TEXT NOT NULL,
    like_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng artists (nghệ sĩ)
CREATE TABLE artists (
    artist_id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    image_url TEXT
);

-- Bảng genres (thể loại)
CREATE TABLE genres (
    genre_id SERIAL PRIMARY KEY,
    genre_name VARCHAR(100) UNIQUE NOT NULL,
    genre_image TEXT
);

-- Bảng languages (ngôn ngữ)
CREATE TABLE languages (
    language_id SERIAL PRIMARY KEY,
    language_name VARCHAR(50) UNIQUE NOT NULL,
    language_image TEXT
);

-- Bảng user_likes (bài hát yêu thích)
CREATE TABLE user_likes (
    like_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    track_id INTEGER REFERENCES tracks(track_id),
    liked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, track_id)
);
```

### 🔧 Cài Đặt

1. **Clone repository**
```bash
git clone https://github.com/BenjaminHung8405/DoAn_Python.NhomDoAn18.DH24TH1_1_1.git
cd DoAn_Python.NhomDoAn18.DH24TH1_1_1
```

2. **Tạo virtual environment**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. **Cài đặt dependencies**
```bash
pip install -r requirements.txt
```

4. **Tạo file .env với DATABASE_URL**
```bash
# File .env
DATABASE_URL=postgresql://username:password@host:5432/database?sslmode=require
```

5. **Chạy ứng dụng**
```bash
python main.py
```

### 🎉 Hoàn Tất!

Giờ bạn có thể đăng ký tài khoản mới và bắt đầu nghe nhạc!

---

## 🔒 Migration Lock System (Mới!)

**Vấn đề:** Team migration đồng thời có thể làm mất dữ liệu

**Giải pháp:** Hệ thống lock tự động với backup

### Quick Start

```bash
# Kiểm tra lock trước khi migration
python -m Database.migration_lock status

# Chạy migration an toàn (auto lock + backup)
python -m Database.protected_migration run

# Seed dữ liệu mẫu
python -m Database.seed_data seed
```

### Tài Liệu Chi Tiết

- 📖 [Team Migration Guide - BẮT BUỘC ĐỌC](Database/TEAM_MIGRATION_GUIDE.md)
- 📖 [Migration Lock System - Chi tiết](Database/MIGRATION_LOCK_GUIDE.md)

---

<!-- LỘ TRÌNH PHÁT TRIỂN -->
## Lộ Trình Phát Triển

### ✅ Đã Hoàn Thành

- [x] Migration từ Firebase sang PostgreSQL
- [x] **Migration Lock System - Bảo vệ database** 🔒
- [x] **Auto Backup trước migration** 💾
- [x] **Seed data system** 🌱
- [x] Chuyển đổi chú thích sang tiếng Việt
- [x] Hỗ trợ đa nền tảng (Windows/Linux/macOS)
- [x] Connection pooling cho PostgreSQL
- [x] User authentication với PostgreSQL
- [x] Like/Unlike bài hát
- [x] Tìm kiếm theo thể loại và ngôn ngữ

### 🚀 Sắp Tới

- [ ] Tạo playlist cá nhân
- [ ] Follow nghệ sĩ yêu thích
- [ ] Lịch sử nghe nhạc
- [ ] Gợi ý bài hát dựa trên sở thích
- [ ] Chia sẻ bài hát qua email
- [ ] Thêm lyrics hiển thị
- [ ] Dark/Light theme toggle

Xem thêm tại [open issues](https://github.com/BenjaminHung8405/DoAn_Python.NhomDoAn18.DH24TH1_1_1/issues)



<!-- ĐÓNG GÓP -->
## Đóng Góp

Mọi đóng góp đều được **đánh giá cao**! Đây là cách bạn có thể đóng góp:

1. Fork dự án
2. Tạo Feature Branch (`git checkout -b feature/TinhNangMoi`)
3. Commit thay đổi (`git commit -m 'Thêm tính năng mới'`)
4. Push lên Branch (`git push origin feature/TinhNangMoi`)
5. Mở Pull Request

### 📝 Quy Tắc Đóng Góp

- Code phải có chú thích bằng **tiếng Việt**
- Tuân thủ PEP 8 style guide
- Test kỹ trước khi commit
- Viết commit message rõ ràng

<!-- GIẤY PHÉP -->
## Giấy Phép

Phân phối theo giấy phép MIT License. Xem `LICENSE` để biết thêm thông tin.

---

<div align="center">
  <p>⭐ Nếu bạn thích dự án này, hãy cho chúng tôi một star nhé! ⭐</p>
  <p>Made with ❤️ by Nhóm 18 - DH24TH1</p>
</div>






<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Srajan1122/TK-Player
[contributors-url]: https://github.com/Srajan1122/TK-Player/graphs/contributors
[activity-shield]: https://img.shields.io/github/commit-activity/m/Srajan1122/Tk-Player
[activity-url]: https://github.com/Srajan1122/TK-Player/commits/master
[version-shield]: https://img.shields.io/github/v/tag/Srajan1122/Tk-Player
[version-url]: https://github.com/Srajan1122/TK-Player/releases
[language-shield]: https://img.shields.io/github/languages/top/Srajan1122/TK-Player
[language-url]: https://www.python.org/
[forks-shield]: https://img.shields.io/github/forks/Srajan1122/TK-Player
[forks-url]:https://github.com/Srajan1122/TK-Player/network/members
[stars-shield]: 	https://img.shields.io/github/stars/Srajan1122/TK-Player
[stars-url]: https://github.com/Srajan1122/TK-Player/stargazers
[issues-shield]: https://img.shields.io/github/issues/Srajan1122/TK-Player
[issues-url]: hhttps://github.com/Srajan1122/TK-Player/issues
[license-shield]: https://img.shields.io/github/license/Srajan1122/TK-Player
[license-url]: https://github.com/Srajan1122/TK-Player/blob/master/LICENSE

