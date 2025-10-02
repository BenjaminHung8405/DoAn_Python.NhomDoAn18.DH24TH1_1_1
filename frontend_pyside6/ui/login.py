from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox,
    QPushButton, QFrame, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap, QIcon
from frontend_pyside6.api_client import APIClient
import os

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Đăng nhập - Expense Tracker")
        self.setFixedSize(400, 500)
        self.setStyleSheet("background-color: #f3f4f6;")  # Light gray background like bg-gray-100
        self.setFont(QFont("Roboto", 10))  # Set Roboto font for Vietnamese text
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        # Icon/Logo
        icon_label = QLabel()
        # You can set an icon here, for now placeholder
        icon_label.setText("💰")  # Placeholder icon
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 48px;")
        main_layout.addWidget(icon_label)

        # Title
        title_label = QLabel("Đăng nhập tài khoản")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333333;")
        main_layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel("Chào mừng bạn quay trở lại!")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 14px; color: #6b7280;")
        main_layout.addWidget(subtitle_label)

        # Spacer
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Username input
        username_label = QLabel("Tên đăng nhập")
        username_label.setStyleSheet("font-weight: bold; color: #333333;")
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
        password_label.setStyleSheet("font-weight: bold; color: #333333;")
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

        # Remember me and forgot password
        options_layout = QHBoxLayout()
        self.remember_checkbox = QCheckBox("Ghi nhớ đăng nhập")
        self.remember_checkbox.setStyleSheet("color: #333333;")
        options_layout.addWidget(self.remember_checkbox)

        options_layout.addStretch()

        forgot_button = QPushButton("Quên mật khẩu?")
        forgot_button.setFlat(True)
        forgot_button.setStyleSheet("color: #3b82f6; text-decoration: underline;")
        options_layout.addWidget(forgot_button)

        main_layout.addLayout(options_layout)

        # Spacer
        main_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Login button
        self.login_button = QPushButton("Đăng nhập")
        self.login_button.setStyleSheet("""
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
        main_layout.addWidget(self.login_button)

        # Spacer
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Sign up link
        signup_label = QLabel("Chưa có tài khoản? <a href='#'>Đăng ký ngay</a>")
        signup_label.setAlignment(Qt.AlignCenter)
        signup_label.setOpenExternalLinks(False)
        signup_label.setStyleSheet("color: #6b7280; font-size: 14px;")
        signup_label.linkActivated.connect(self.on_signup_clicked)
        main_layout.addWidget(signup_label)

        self.setLayout(main_layout)

        # Connect signals
        self.login_button.clicked.connect(self.on_login_clicked)
        forgot_button.clicked.connect(self.on_forgot_password_clicked)

    def on_login_clicked(self):
        username = self.username_input.text()
        password = self.password_input.text()
        remember = self.remember_checkbox.isChecked()
        backend = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
        client = APIClient(base_url=backend)
        try:
            resp = client.__class__().__init__ if False else None
            # Use requests directly via APIClient endpoints: call token endpoint
            import requests
            r = requests.post(f"{backend}/token", data={"username": username, "password": password})
            if r.status_code == 200:
                data = r.json()
                client.set_tokens(access_token=data.get("access_token"), refresh_token=data.get("refresh_token"))
                print("Login successful, token stored via APIClient")
            else:
                print("Login failed:", r.text)
        except Exception as e:
            print("Error contacting backend:", e)

    def on_forgot_password_clicked(self):
        # TODO: Implement forgot password
        print("Forgot password clicked")

    def on_signup_clicked(self):
        # TODO: Implement signup
        print("Signup clicked")