from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox,
    QPushButton, QSpacerItem, QSizePolicy, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from ..api_client import APIClient

class RegisterWindow(QWidget):
    def __init__(self, on_login=None):
        super().__init__()
        self.on_login = on_login
        self.setWindowTitle("Đăng ký - Expense Tracker")
        self.setFixedSize(400, 550)
        self.setStyleSheet("background-color: #f3f4f6;")
        self.setFont(QFont("Roboto", 10))
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        # Icon/Logo
        icon_label = QLabel()
        icon_label.setText("👤")  # User icon placeholder
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 48px;")
        main_layout.addWidget(icon_label)

        # Title
        title_label = QLabel("Tạo tài khoản mới")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #1f2937;")
        main_layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel("Bắt đầu quản lý chi tiêu của bạn ngay hôm nay!")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 14px; color: #6b7280;")
        main_layout.addWidget(subtitle_label)

        # Spacer
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Username input
        username_label = QLabel("Tên đăng nhập")
        username_label.setStyleSheet("font-weight: bold; color: #1f2937;")
        main_layout.addWidget(username_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Tên đăng nhập")
        self.username_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3b82f6;
            }
        """)
        main_layout.addWidget(self.username_input)

        # Password input
        password_label = QLabel("Mật khẩu")
        password_label.setStyleSheet("font-weight: bold; color: #1f2937;")
        main_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Mật khẩu")
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3b82f6;
            }
        """)
        main_layout.addWidget(self.password_input)

        # Confirm password input
        confirm_password_label = QLabel("Xác nhận mật khẩu")
        confirm_password_label.setStyleSheet("font-weight: bold; color: #1f2937;")
        main_layout.addWidget(confirm_password_label)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setPlaceholderText("Xác nhận mật khẩu")
        self.confirm_password_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3b82f6;
            }
        """)
        main_layout.addWidget(self.confirm_password_input)

        # Terms checkbox
        terms_layout = QHBoxLayout()
        self.terms_checkbox = QCheckBox("Tôi đồng ý với Điều khoản Dịch vụ")
        self.terms_checkbox.setStyleSheet("color: #1f2937;")
        terms_layout.addWidget(self.terms_checkbox)
        main_layout.addLayout(terms_layout)

        # Spacer
        main_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Register button
        self.register_button = QPushButton("Tạo tài khoản")
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)
        main_layout.addWidget(self.register_button)

        # Spacer
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Link to login
        login_label = QLabel("Đã có tài khoản? <a href='#'>Đăng nhập tại đây</a>")
        login_label.setAlignment(Qt.AlignCenter)
        login_label.setOpenExternalLinks(False)
        login_label.setStyleSheet("color: #6b7280; font-size: 14px;")
        login_label.linkActivated.connect(self.on_login_clicked)
        main_layout.addWidget(login_label)

        self.setLayout(main_layout)

        # Connect signals
        self.register_button.clicked.connect(self.on_register_clicked)

    def on_register_clicked(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        terms_accepted = self.terms_checkbox.isChecked()

        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin.")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu xác nhận không khớp.")
            return

        if not terms_accepted:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chấp nhận điều khoản dịch vụ.")
            return

        try:
            user = APIClient().create_user({"username": username, "password": password})
            QMessageBox.information(self, "Thành công", "Đăng ký thành công! Vui lòng đăng nhập.")
            if self.on_login:
                self.on_login()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Đăng ký thất bại: {str(e)}")

    def on_login_clicked(self):
        if self.on_login:
            self.on_login()
        else:
            print("Switch to login")