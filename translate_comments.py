#!/usr/bin/env python3
"""
Script để chuyển đổi tất cả các chú thích tiếng Anh sang tiếng Việt
"""

import os
import re

# Dictionary ánh xạ các chú thích phổ biến
TRANSLATIONS = {
    # Database comments
    "Load environment variables from .env file": "Tải các biến môi trường từ file .env",
    "PostgreSQL connection string from .env (Neon)": "Chuỗi kết nối PostgreSQL từ .env (Neon)",
    "Create connection pool to manage DB connections": "Tạo connection pool để quản lý các kết nối DB",
    "Add SSL mode if not present in DATABASE_URL": "Thêm chế độ SSL nếu không có trong DATABASE_URL",
    "minimum connections": "số kết nối tối thiểu",
    "maximum connections": "số kết nối tối đa",
    "Add timeout to avoid hanging": "Thêm timeout để tránh treo",
    "Provide a Firestore-like `db` object backed by PostgreSQL via a lightweight emulator.": "Cung cấp đối tượng `db` giống Firestore được hỗ trợ bởi PostgreSQL qua emulator nhẹ.",
    "Keep the `db` symbol for compatibility with existing code that uses db.collection(...).": "Giữ ký hiệu `db` để tương thích với code hiện có sử dụng db.collection(...).",
    "import here to avoid circular imports": "import ở đây để tránh circular imports",
    "For backwards compatibility with code that does `from Database.config import db`": "Để tương thích ngược với code sử dụng `from Database.config import db`",
    "we provide a module-level `db` property via __getattr__": "chúng ta cung cấp thuộc tính `db` cấp module qua __getattr__",
    
    # Emulator comments
    "use title as identifier": "sử dụng title làm định danh",
    "doc id supposed to be uid string; convert if numeric": "doc id phải là chuỗi uid; chuyển đổi nếu là số",
    "insert or update by user_id or by email": "chèn hoặc cập nhật theo user_id hoặc email",
    "try insert by email": "thử chèn theo email",
    "albums and subcollection handled simply": "albums và subcollection được xử lý đơn giản",
    "unsupported collection -> no-op": "collection không được hỗ trợ -> không làm gì",
    "Return a snapshot-like object": "Trả về đối tượng giống snapshot",
    "Support nested paths like 'artist/<name>/tracks' and 'albums/<name>/tracks'": "Hỗ trợ đường dẫn lồng như 'artist/<name>/tracks' và 'albums/<name>/tracks'",
    "convenience aliases": "các bí danh tiện lợi",
    
    # Firebase admin comments
    "row: (user_id, display_name, email, password, phone_number, created_at)": "hàng: (user_id, display_name, email, password, phone_number, created_at)",
    "PostgreSQL doesn't store this, default to False": "PostgreSQL không lưu trữ điều này, mặc định là False",
    "check email": "kiểm tra email",
    "check phone": "kiểm tra số điện thoại",
    "re-raise known exceptions": "tái phát các ngoại lệ đã biết",
    
    # Database package
    "Database package": "Gói Database",
    "ensure we can import Database package": "đảm bảo chúng ta có thể import gói Database",
    
    # Authentication comments
    "-----Base for Authentication-----": "-----Cơ sở cho Xác thực-----",
    "#Layout of Base": "#Bố cục của Cơ sở",
    "Use attributes for cross-platform fullscreen/maximize": "Sử dụng attributes cho fullscreen/maximize đa nền tảng",
    "Windows": "Windows",
    "Linux/macOS: maximize using geometry or -fullscreen": "Linux/macOS: phóng to bằng geometry hoặc -fullscreen",
    "Some Linux DEs": "Một số môi trường desktop Linux",
    "Fallback: normal window": "Dự phòng: cửa sổ bình thường",
    "#Frame of Base": "#Khung của Cơ sở",
    "#Canvas for Background Image": "#Canvas cho Hình nền",
    "#Frames": "#Các Khung",
    "#Close Button": "#Nút Đóng",
    "#Frame grid and configurations": "#Lưới khung và cấu hình",
    "#Function for displaying frames": "#Hàm hiển thị các khung",
    "#Function for entering Homepage": "#Hàm vào Trang chủ",
    
    # Frame1 comments
    "#-----Signup/Register Page": "#-----Trang Đăng ký",
    "data for registration and passing them": "dữ liệu đăng ký và truyền chúng",
    "data3 for email passing": "data3 để truyền email",
    "Class for input field: contact number": "Lớp cho trường nhập: số liên lạc",
    "Class for input fields: username, password, email": "Lớp cho các trường nhập: tên người dùng, mật khẩu, email",
    "#placeholder function": "#hàm placeholder",
    "#font size, style": "#kích thước font, kiểu",
    "#font color": "#màu font",
    "#properties of Entry widget": "#thuộc tính của widget Entry",
    "#function called on focusing": "#hàm được gọi khi focus",
    "#function called when not focusing": "#hàm được gọi khi không focus",
    "#Frame of Signup/Register Page": "#Khung của Trang Đăng ký",
    "#Frame": "#Khung",
    "#Signup/Register head": "#Tiêu đề Đăng ký",
    "#For Back button": "#Cho nút Quay lại",
    "#Font style, size": "#Kiểu font, kích thước",
    "#Bck button": "#Nút Quay lại",
    "#Username Entry": "#Nhập Tên người dùng",
    "#Password Entry": "#Nhập Mật khẩu",
    "#Contact Number Entry": "#Nhập Số liên lạc",
    "#Email Entry": "#Nhập Email",
    "#Result/Stataus Display": "#Hiển thị Kết quả/Trạng thái",
    "#Result/Status Display": "#Hiển thị Kết quả/Trạng thái",
    "#Signup/Register Button": "#Nút Đăng ký",
    "#Validaiton funtion for contact number": "#Hàm xác thực cho số liên lạc",
    "#Validation function for email": "#Hàm xác thực cho email",
    "#Validation function for password": "#Hàm xác thực cho mật khẩu",
    "#Validation for signup/register": "#Xác thực cho đăng ký",
    "#placeholders": "#các placeholder",
    "Register user directly without email verification": "Đăng ký người dùng trực tiếp không cần xác thực email",
    "Save user_id to file for auto-login": "Lưu user_id vào file để tự động đăng nhập",
    "Show login frame": "Hiển thị khung đăng nhập",
    
    # Frame3 comments
    "#-----Login Page-----": "#-----Trang Đăng nhập-----",
    "data2 for checking credentials and passing them": "data2 để kiểm tra thông tin đăng nhập và truyền chúng",
    "#passing user credentials to Homepage": "#truyền thông tin đăng nhập người dùng vào Trang chủ",
    "#Class for Entry widget": "#Lớp cho widget Entry",
    "#Frame of Login Page": "#Khung của Trang Đăng nhập",
    "#Login head": "#Tiêu đề Đăng nhập",
    "#For Back buttton": "#Cho nút Quay lại",
    "#Back button": "#Nút Quay lại",
    "#Email entry": "#Nhập Email",
    "#Login Button": "#Nút Đăng nhập",
    "#Validation for login": "#Xác thực cho đăng nhập",
    
    # Frame4 comments
    "#-----Email Verification Page-----": "#-----Trang Xác thực Email-----",
    "#Frame of Email Verification Page": "#Khung của Trang Xác thực Email",
    "#Email Verification head": "#Tiêu đề Xác thực Email",
    "#otp Entry": "#Nhập mã OTP",
    "#Verify Button": "#Nút Xác thực",
    "#resend button": "#nút gửi lại",
    "#Resend OTP": "#Gửi lại OTP",
    "#Validation function for otp": "#Hàm xác thực cho OTP",
    
    # Database.py comments
    "Query PostgreSQL languages table": "Truy vấn bảng languages của PostgreSQL",
    "language_name": "tên ngôn ngữ",
    "language_image": "hình ảnh ngôn ngữ",
    "Create user in PostgreSQL via firebase_admin shim": "Tạo người dùng trong PostgreSQL qua firebase_admin shim",
    "Email already exists": "Email đã tồn tại",
    "Phone number already exists": "Số điện thoại đã tồn tại",
    "Query PostgreSQL genres table": "Truy vấn bảng genres của PostgreSQL",
    "genre_name": "tên thể loại",
    "genre_image": "hình ảnh thể loại",
    "[START get_user]": "[BẮT ĐẦU get_user]",
    "Return user object as dict for compatibility": "Trả về đối tượng user dưới dạng dict để tương thích",
    "Include password for UserPage": "Bao gồm password cho UserPage",
    "User not found - delete the user file and return False to show login": "Không tìm thấy người dùng - xóa file user và trả về False để hiển thị đăng nhập",
    "[END get_user]": "[KẾT THÚC get_user]",
    "Return user record directly from PostgreSQL": "Trả về bản ghi user trực tiếp từ PostgreSQL",
    "[END get_user_by_phone]": "[KẾT THÚC get_user_by_phone]",
    "doc is a SimpleNamespace object, use attributes not dict keys": "doc là đối tượng SimpleNamespace, sử dụng attributes không phải dict keys",
    "Takes random choices from": "Lấy các lựa chọn ngẫu nhiên từ",
    "ascii_letters and digits": "chữ cái ascii và số",
    "For PostgreSQL migration: skip email verification, allow all users to login": "Cho migration PostgreSQL: bỏ qua xác thực email, cho phép tất cả người dùng đăng nhập",
    "Always return True to bypass OTP verification": "Luôn trả về True để bỏ qua xác thực OTP",
    "Query user_likes table for this user's liked songs": "Truy vấn bảng user_likes cho các bài hát đã thích của người dùng này",
    "Convert to dict format for compatibility with Firebase structure": "Chuyển đổi sang định dạng dict để tương thích với cấu trúc Firebase",
    "Query PostgreSQL tracks table ordered by like_count": "Truy vấn bảng tracks của PostgreSQL được sắp xếp theo like_count",
    "Convert to dict format for compatibility": "Chuyển đổi sang định dạng dict để tương thích",
    
    # Main.py comments
    "Use attributes for maximized window on Linux": "Sử dụng attributes cho cửa sổ phóng to trên Linux",
    "Maximize window - cross-platform compatible": "Phóng to cửa sổ - tương thích đa nền tảng",
    "Just toggling the boolean": "Chỉ đảo ngược boolean",
    "If user not found, show login screen": "Nếu không tìm thấy người dùng, hiển thị màn hình đăng nhập",
    
    # Components comments
    "font": "font",
    "images": "hình ảnh",
    "frames": "các khung",
    "frame1": "khung1",
    "frame2": "khung2",
    "frame3": "khung3",
    "frame4": "khung4",
    "frame5": "khung5",
    "grid - components": "lưới - các thành phần",
    "grid - frames": "lưới - các khung",
    "grid - row/column": "lưới - hàng/cột",
    
    # TopRightTop comments
    "placeholder function": "hàm placeholder",
    "font size, style": "kích thước font, kiểu",
    "font color": "màu font",
    "properties of Entry widget": "thuộc tính của widget Entry",
    "function called on focusing": "hàm được gọi khi focus",
    "function called when not focusing": "hàm được gọi khi không focus",
    "User_button": "Nút người dùng",
    "user_dropdown": "menu thả xuống người dùng",
    
    # Resource comments
    "Apply theme-specific settings using style.map (cross-platform compatible)": "Áp dụng cài đặt cụ thể cho theme sử dụng style.map (tương thích đa nền tảng)",
    "Instead of theme_settings which is theme-specific": "Thay vì theme_settings là cụ thể cho theme",
    "Apply style mapping (cross-platform compatible)": "Áp dụng ánh xạ style (tương thích đa nền tảng)",
    
    # UserPage comments
    "#Frames": "#Các Khung",
    "#Logo": "#Logo",
    "#Profile": "#Hồ sơ",
    "#Name": "#Tên",
    "#Email": "#Email",
    "#Contact No.": "#Số liên lạc",
    "#Password": "#Mật khẩu",
    "#configure": "#cấu hình",
    
    # HomePage comments
    "Load image from URL using PIL": "Tải hình ảnh từ URL sử dụng PIL",
    
    # SearchPage comments
    
    # Fix frame2
    "Read the file": "Đọc file",
    "Find registerNow function and fix indentation": "Tìm hàm registerNow và sửa lỗi thụt lề",
    "End of registerNow function": "Kết thúc hàm registerNow",
    "Inside registerNow - ensure proper indentation": "Bên trong registerNow - đảm bảo thụt lề đúng",
    "Empty line": "Dòng trống",
    "Comment should have 2 tabs": "Comment nên có 2 tabs",
    "Statement at function body level - 2 tabs": "Câu lệnh ở cấp thân hàm - 2 tabs",
    "Inside if block - 3 tabs": "Bên trong khối if - 3 tabs",
    "Variable assignments - 2 tabs": "Gán biến - 2 tabs",
    "Keep original indentation if unsure": "Giữ nguyên thụt lề nếu không chắc",
    "Write back": "Ghi lại",
}

def translate_comment(line):
    """Chuyển đổi một dòng chú thích sang tiếng Việt"""
    # Tìm vị trí bắt đầu của comment
    comment_start = line.find('#')
    if comment_start == -1:
        return line
    
    # Lấy phần trước và sau comment
    before_comment = line[:comment_start]
    comment_part = line[comment_start:]
    
    # Xử lý comment
    for eng, vie in TRANSLATIONS.items():
        if eng.lower() in comment_part.lower():
            # Giữ nguyên định dạng comment (dấu #, khoảng trắng)
            comment_part = comment_part.replace(eng, vie)
            comment_part = comment_part.replace(eng.lower(), vie)
            comment_part = comment_part.replace(eng.upper(), vie.upper())
    
    return before_comment + comment_part

def process_file(filepath):
    """Xử lý một file Python"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        modified = False
        new_lines = []
        
        for line in lines:
            if '#' in line:
                new_line = translate_comment(line)
                if new_line != line:
                    modified = True
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"✓ Đã chuyển đổi: {filepath}")
            return True
        return False
        
    except Exception as e:
        print(f"✗ Lỗi khi xử lý {filepath}: {e}")
        return False

def main():
    """Hàm chính"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Danh sách các thư mục cần xử lý
    directories = [
        'Database',
        'firebase_admin',
        'Pages',
        'Base',
        'Music',
    ]
    
    total_files = 0
    modified_files = 0
    
    # Xử lý các file Python trong thư mục gốc
    for filename in ['main.py', 'utils.py', 'setup.py', 'test_db.py', 'build.py']:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            total_files += 1
            if process_file(filepath):
                modified_files += 1
    
    # Xử lý các thư mục
    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        if not os.path.exists(dir_path):
            continue
            
        for root, dirs, files in os.walk(dir_path):
            for filename in files:
                if filename.endswith('.py'):
                    filepath = os.path.join(root, filename)
                    total_files += 1
                    if process_file(filepath):
                        modified_files += 1
    
    print(f"\n{'='*60}")
    print(f"Hoàn tất! Đã xử lý {total_files} file, chuyển đổi {modified_files} file.")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
