import os
import json
import hashlib
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
                           QVBoxLayout, QComboBox, QMessageBox)
from PyQt5.QtCore import Qt

class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Стражник - Авторизация")
        self.setFixedSize(400, 350)
        self.setup_ui()
        self.ensure_data_directory()
        self.load_or_create_config()

    def ensure_data_directory(self):
        if not os.path.exists('data'):
            os.makedirs('data')

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Сервис контроля доступа «Стражник»")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")

        self.user_type = QComboBox()
        self.user_type.addItems(["Администратор доступа", "Сотрудник службы безопасности"])
        self.user_type.setStyleSheet("padding: 8px; border: 1px solid #bdc3c7; border-radius: 4px;")

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите логин")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.secret_input = QLineEdit()
        self.secret_input.setPlaceholderText("Введите секретное слово")
        self.secret_input.setEchoMode(QLineEdit.Password)

        for input_field in [self.login_input, self.password_input, self.secret_input]:
            input_field.setStyleSheet("padding: 8px; border: 1px solid #bdc3c7; border-radius: 4px;")

        login_btn = QPushButton("Войти в систему")
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        login_btn.clicked.connect(self.authenticate)

        layout.addWidget(title)
        layout.addWidget(self.user_type)
        layout.addWidget(QLabel("Логин:"))
        layout.addWidget(self.login_input)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel("Секретное слово:"))
        layout.addWidget(self.secret_input)
        layout.addWidget(login_btn)

        self.setLayout(layout)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def load_or_create_config(self):
        config_path = "data/config.json"
        if not os.path.exists(config_path):
            default_config = {
                "users": [
                    {
                        "role": "Администратор доступа",
                        "login": "guardianskk",
                        "password": self.hash_password("Admin123!"),
                        "secret": self.hash_password("security"),
                        "name": "Иванов И.И."
                    },
                    {
                        "role": "Сотрудник службы безопасности",
                        "login": "defendservice",
                        "password": self.hash_password("Security123!"),
                        "secret": self.hash_password("guard"),
                        "name": "Петров П.П."
                    }
                ]
            }
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=4)

    def authenticate(self):
        role = self.user_type.currentText()
        login = self.login_input.text()
        password = self.password_input.text()
        secret = self.secret_input.text()

        if not all([login, password, secret]):
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
            return

        try:
            with open('data/config.json') as f:
                config = json.load(f)

            user = None
            for u in config['users']:
                if u['role'] == role and u['login'] == login:
                    user = u
                    break

            if not user:
                QMessageBox.warning(self, "Ошибка", "Пользователь не найден!")
                return

            if (self.hash_password(password) == user["password"] and 
                self.hash_password(secret) == user["secret"]):
                
                self.hide()
                
                if role == "Администратор доступа":
                    QMessageBox.information(self, "Успех", "Добро пожаловать, администратор!")
                else:
                    from security import SecurityWindow
                    self.security_window = SecurityWindow(user["name"])
                    self.security_window.show()
            else:
                QMessageBox.warning(self, "Ошибка", "Неверные учетные данные!")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка авторизации: {str(e)}")
