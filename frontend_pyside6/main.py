import sys
from PySide6.QtWidgets import QApplication
from ui.login import LoginWindow
from ui.register import RegisterWindow

def main():
    app = QApplication(sys.argv)
    register_window = RegisterWindow()
    login_window = LoginWindow(on_signup=lambda: (login_window.hide(), register_window.show()))
    register_window = RegisterWindow(on_login=lambda: (register_window.hide(), login_window.show()))
    login_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()