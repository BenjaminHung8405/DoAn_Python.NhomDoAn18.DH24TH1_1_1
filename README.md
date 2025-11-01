# 🎵 Amplify - Ứng dụng nghe nhạc Spotify Clone

**Đồ án học phần Python - Nhóm 18**

- **Sinh viên**: DTH235659 - Nguyễn Phi Hùng
- **Lớp**: DH24TH1
- **Học phần**: Lập trình Python

---

## 📋 Mô tả dự án

Amplify là ứng dụng desktop nghe nhạc được xây dựng bằng Python, mô phỏng giao diện và tính năng của Spotify. Dự án sử dụng:

- **Frontend**: Tkinter với custom UI components
- **Database**: PostgreSQL (Neon Cloud)
- **Features**:
  - 🎨 Giao diện đẹp mắt, hiện đại với dark theme
  - 🎵 Quản lý albums, tracks, artists, playlists
  - 🔍 Tìm kiếm và browse nhạc
  - ❤️ Yêu thích bài hát
  - 👤 Quản lý user và authentication
  - 🎼 Phát nhạc với music player controls

---

## 🛠️ Công nghệ sử dụng

### Backend & Database
- **PostgreSQL** - Neon Cloud Database
- **psycopg2** - PostgreSQL adapter
- **Connection pooling** - Tối ưu kết nối database

### Frontend
- **Tkinter** - GUI framework
- **Pillow (PIL)** - Xử lý hình ảnh
- **Pyglet** - Custom fonts
- **Requests** - HTTP client để load ảnh từ URL

### Audio
- **Pygame** - Audio playback
- **Mutagen** - Audio metadata

### Data Processing
- **NumPy** - Numerical computing
- **scikit-image** - Image processing

---

## 📦 Cấu trúc thư mục

```
DoAn_Python.NhomDoAn18.DH24TH1_1_1/
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── test_db.py                # Database test script
├── README.md
│
├── ActivityIndicator/        # Loading animation
│   ├── Activity_Indicator.py
│   └── Activity.gif
│
├── Base/                     # Base UI components
│   ├── top.py               # Top navigation bar
│   ├── bottom.py            # Bottom player bar
│   ├── topLeft.py           # Logo & menu
│   ├── topRight.py          # Page container
│   └── ...
│
├── Database/                 # Database layer
│   ├── config.py            # DB configuration
│   ├── Database.py          # Connection pool & queries
│   └── HomePagedata.py      # Data fetching logic
│
├── Pages/                    # Application pages
│   ├── HomePage/            # Home page
│   │   ├── Home.py
│   │   └── Components/
│   │       └── HorizontalFrame.py
│   ├── SearchPage/          # Search page
│   ├── Browse/              # Browse page
│   ├── AlbumPage/           # Album detail page
│   ├── ArtistPage/          # Artist detail page
│   ├── MusicPage/           # Music player page
│   ├── UserPage/            # User profile
│   └── Resource/            # Shared resources
│       ├── Header.py
│       ├── HorizontalScrollableFrame.py
│       └── VerticalScrollableFrame.py
│
├── fonts/                    # Custom fonts
│   └── Play/
│       ├── Play-Bold.ttf
│       └── Play-Regular.ttf
│
└── images/                   # UI assets
    ├── app_64.png
    ├── play_icon.png
    ├── pause_icon.png
    └── ...
```

---

## 🚀 Hướng dẫn cài đặt & chạy

### 1️⃣ Yêu cầu hệ thống

- **Python**: 3.10+ (khuyến nghị 3.10)
- **OS**: Windows / macOS / Linux
- **RAM**: 4GB+
- **Kết nối Internet**: Để load hình ảnh từ database

### 2️⃣ Clone repository

```bash
git clone https://github.com/your-username/DoAn_Python.NhomDoAn18.DH24TH1_1_1.git
cd DoAn_Python.NhomDoAn18.DH24TH1_1_1
```

### 3️⃣ Tạo môi trường ảo (Virtual Environment)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4️⃣ Cài đặt dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

**Nội dung `requirements.txt`:**
```txt
pyglet==2.0.10
Pillow==10.1.0
numpy==1.26.2
scikit-image==0.22.0
mutagen==1.47.0
requests==2.31.0
pygame==2.5.2
psycopg2-binary==2.9.9
```

### 5️⃣ Cấu hình Database

Dự án sử dụng PostgreSQL trên Neon Cloud. Connection string đã được cấu hình sẵn trong `Database/config.py`:

```python
DATABASE_CONFIG = {
    'connection_string': "postgresql://neondb_owner:npg_0xVDJL7dfsSI@ep-polished-water-a1gwnvhw-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
}
```

> **Lưu ý**: Để bảo mật, trong production nên đặt connection string vào biến môi trường.

### 6️⃣ Test kết nối Database

```bash
python test_db.py
```

**Kết quả mong đợi:**
```
==================================================
DATABASE CONNECTION TEST
==================================================

[1] Testing database connection...
   ✓ Connected! Total artists: 15

[2] Checking tables...
   ✓ artists: 15 records
   ✓ albums: 20 records
   ✓ tracks: 50 records
   ✓ genres: 10 records
   ✓ languages: 5 records
   ✓ users: 3 records

[3] Testing HomePage data...
   ✓ Got 4 sections
      - Popular Albums: 10 items
      - Trending Now: 10 items
      - Top Artists: 10 items
      - Recently Added: 10 items

==================================================
TEST COMPLETED
==================================================
```

### 7️⃣ Chạy ứng dụng

```bash
python main.py
```

**Ứng dụng sẽ:**
1. Hiển thị splash screen trong 3 giây
2. Load dữ liệu từ PostgreSQL
3. Hiển thị giao diện chính với:
   - Home page với albums, tracks, artists
   - Navigation menu (Home, Browse, Search)
   - Music player controls (bottom bar)

---

## 🎯 Tính năng chính

### ✅ Đã hoàn thành

#### 1. **Home Page**
- Hiển thị Popular Albums
- Trending Tracks với like count
- Top Artists
- Recently Added Albums
- Lazy loading images từ URL
- Hover effects (zoom, shadow, play button overlay)
- Scrolling text cho tên bài hát dài

#### 2. **Database Integration**
- Connection pooling với PostgreSQL
- Real-time data fetching
- Error handling và fallback
- Mock data khi database trống

#### 3. **UI Components**
- Custom scrollable frames (vertical & horizontal)
- Music cards với hover animations
- Header component tái sử dụng
- Responsive layout với grid/pack managers

#### 4. **Image Handling**
- Load ảnh từ HTTP/HTTPS
- Placeholder cho ảnh lỗi
- Cache ảnh đã load
- User-Agent spoofing cho Wikipedia

### 🚧 Đang phát triển

- [ ] Search functionality
- [ ] Browse by genre/language
- [ ] Album detail page
- [ ] Artist detail page
- [ ] Music player với audio playback
- [ ] Playlist management
- [ ] User authentication & profiles
- [ ] Like/Unlike tracks
- [ ] Add to playlist
- [ ] Audio visualization

---

## 🗄️ Database Schema

### **Bảng chính:**

```sql
-- Artists
CREATE TABLE artists (
    artist_id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    image_url TEXT
);

-- Albums
CREATE TABLE albums (
    album_id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    release_date DATE,
    cover_image_url TEXT,
    artist_id INTEGER REFERENCES artists(artist_id)
);

-- Tracks
CREATE TABLE tracks (
    track_id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    duration_seconds INTEGER,
    location_url TEXT,
    like_count INTEGER DEFAULT 0,
    album_id INTEGER REFERENCES albums(album_id),
    genre_id INTEGER REFERENCES genres(genre_id),
    language_id INTEGER REFERENCES languages(language_id)
);

-- Users
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    password_hash TEXT,
    display_name VARCHAR
);

-- Playlists
CREATE TABLE playlists (
    playlist_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    is_public BOOLEAN DEFAULT false,
    user_id INTEGER REFERENCES users(user_id)
);
```

### **Bảng quan hệ:**

```sql
-- Track - Artist (Many-to-Many)
CREATE TABLE track_artists (
    track_id INTEGER REFERENCES tracks(track_id),
    artist_id INTEGER REFERENCES artists(artist_id),
    PRIMARY KEY (track_id, artist_id)
);

-- User - Liked Songs (Many-to-Many)
CREATE TABLE user_liked_songs (
    user_id INTEGER REFERENCES users(user_id),
    track_id INTEGER REFERENCES tracks(track_id),
    PRIMARY KEY (user_id, track_id)
);

-- Playlist - Tracks (Many-to-Many)
CREATE TABLE playlist_tracks (
    playlist_id INTEGER REFERENCES playlists(playlist_id),
    track_id INTEGER REFERENCES tracks(track_id),
    track_order INTEGER,
    PRIMARY KEY (playlist_id, track_id)
);
```

---

## 🐛 Troubleshooting

### ❌ Lỗi: `ModuleNotFoundError: No module named 'pyglet'`

**Giải pháp:**
```bash
pip install pyglet
```

### ❌ Lỗi: `cannot use geometry manager grid inside ... which already has slaves managed by pack`

**Nguyên nhân**: Mixing pack() và grid() trong cùng container

**Giải pháp**: Chỉ dùng một loại geometry manager. Xem file `Pages/HomePage/Home.py` - đã sửa dùng grid() cho tất cả.

### ❌ Lỗi: `cannot identify image file`

**Nguyên nhân**: Wikipedia trả về HTML thay vì ảnh

**Giải pháp**: Đã implement User-Agent header và fallback placeholder trong `HorizontalFrame.py`

### ❌ Lỗi: Database connection failed

**Kiểm tra:**
1. Kết nối internet
2. Connection string trong `Database/config.py`
3. Firewall/antivirus blocking port 5432

**Test:**
```bash
python test_db.py
```

### ❌ Ứng dụng chạy chậm khi load ảnh

**Nguyên nhân**: Đang download ảnh từ internet

**Giải pháp tương lai**:
- Implement image caching
- Lazy loading với threading
- Thumbnail generation
- CDN cho ảnh

---

## 📚 Tài liệu tham khảo

### Tkinter
- [Official Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [Tkinter Tutorial - Real Python](https://realpython.com/python-gui-tkinter/)

### PostgreSQL
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [Neon Postgres](https://neon.tech/docs/introduction)

### PIL/Pillow
- [Pillow Documentation](https://pillow.readthedocs.io/)

### Audio
- [Pygame Mixer](https://www.pygame.org/docs/ref/mixer.html)
- [Mutagen](https://mutagen.readthedocs.io/)

---

## 🤝 Đóng góp

Dự án này là đồ án học phần, không nhận PR từ bên ngoài. Tuy nhiên, bạn có thể fork và phát triển phiên bản của riêng mình.

---

## 📄 License

MIT License - Dành cho mục đích học tập

---

## 👨‍💻 Thông tin liên hệ

- **Sinh viên**: Nguyễn Phi Hùng
- **MSSV**: DTH235659
- **Email**: hungnp@example.com
- **GitHub**: [@hungdev](https://github.com/hungdev)

---

## 🎓 Lời cảm ơn

- Giảng viên hướng dẫn: Nguyễn Ngọc Minh
- Nhóm học tập: Nhóm 1 - DH24TH1
- Nguồn cảm hứng: Spotify
- Base project: [Amplify by Srajan Gupta](https://github.com/srajangarg/Amplify)

---

## 📝 Changelog

### v1.0.0 (01/11/2025)
- ✅ Initial release
- ✅ PostgreSQL integration
- ✅ Home page với dynamic data
- ✅ Music card với hover effects
- ✅ Scrolling text cho tên dài
- ✅ Image loading từ URLs
- ✅ Database connection pooling

### v0.1.0 (25/10/2025)
- 🎨 Base UI layout
- 📁 Project structure setup
- 🗄️ Database schema design

---

**⭐ Nếu dự án hữu ích, hãy cho một star!**
