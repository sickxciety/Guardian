from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QTabWidget, QGroupBox, QLineEdit,
                           QDateEdit, QComboBox, QFileDialog, QMessageBox,
                           QTextEdit, QFormLayout)
from PyQt5.QtCore import Qt, QDate, QRegExp
from PyQt5.QtGui import QRegExpValidator
import json
import os
import re
from datetime import datetime, timedelta

class SecurityWindow(QWidget):
    def __init__(self, user_name):
        super().__init__()
        self.user_name = user_name
        self.setWindowTitle(f"Стражник - Служба безопасности ({user_name})")
        self.setMinimumSize(900, 650)
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        header = QLabel(f"Служба безопасности - {self.user_name}")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        
        tabs = QTabWidget()
        
        individual_tab = QWidget()
        self.setup_individual_tab(individual_tab)
        
        group_tab = QWidget()
        self.setup_group_tab(group_tab)
        
        tabs.addTab(individual_tab, "Индивидуальный")
        tabs.addTab(group_tab, "Групповой")
        
        main_layout.addWidget(header)
        main_layout.addWidget(tabs)
        self.setLayout(main_layout)
    
    def setup_individual_tab(self, tab):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        pass_group = QGroupBox("Информация для пропуска")
        pass_layout = QFormLayout()
        
        self.pass_start = QDateEdit()
        self.pass_start.setDate(QDate.currentDate().addDays(1))
        self.pass_start.setMinimumDate(QDate.currentDate().addDays(1))
        self.pass_start.setMaximumDate(QDate.currentDate().addDays(15))
        self.pass_start.setCalendarPopup(True)
        
        self.pass_end = QDateEdit()
        self.pass_end.setDate(QDate.currentDate().addDays(2))
        self.pass_end.setCalendarPopup(True)
        
        self.visit_purpose = QLineEdit()
        
        pass_layout.addRow("Дата начала действия*:", self.pass_start)
        pass_layout.addRow("Дата окончания:", self.pass_end)
        pass_layout.addRow("Цель посещения:", self.visit_purpose)
        pass_group.setLayout(pass_layout)
        
        host_group = QGroupBox("Принимающая сторона")
        host_layout = QFormLayout()
        
        self.department = QComboBox()
        self.department.addItems(["Отдел кадров", "Бухгалтерия", "ИТ-отдел", "Администрация"])
        
        self.host_employee = QComboBox()
        self.host_employee.addItems(["Иванов И.И.", "Петров П.П.", "Сидоров С.С."])
        
        host_layout.addRow("Подразделение*:", self.department)
        host_layout.addRow("ФИО сотрудника*:", self.host_employee)
        host_group.setLayout(host_layout)
        
        visitor_group = QGroupBox("Информация о посетителе")
        visitor_layout = QFormLayout()
        
        self.last_name = QLineEdit()
        self.first_name = QLineEdit()
        self.middle_name = QLineEdit()
        
        self.phone = QLineEdit()
        self.phone.setInputMask("+7 (999) 999-99-99")
        
        self.email = QLineEdit()
        email_regex = QRegExp(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        self.email.setValidator(QRegExpValidator(email_regex))
        
        self.organization = QLineEdit()
        
        self.birth_date = QDateEdit()
        self.birth_date.setMaximumDate(QDate.currentDate().addYears(-14))
        self.birth_date.setCalendarPopup(True)
        
        self.passport_series = QLineEdit()
        self.passport_series.setMaxLength(4)
        self.passport_series.setValidator(QRegExpValidator(QRegExp(r"\d{4}")))
        
        self.passport_number = QLineEdit()
        self.passport_number.setMaxLength(6)
        self.passport_number.setValidator(QRegExpValidator(QRegExp(r"\d{6}")))
        
        visitor_layout.addRow("Фамилия*:", self.last_name)
        visitor_layout.addRow("Имя*:", self.first_name)
        visitor_layout.addRow("Отчество:", self.middle_name)
        visitor_layout.addRow("Телефон:", self.phone)
        visitor_layout.addRow("Email*:", self.email)
        visitor_layout.addRow("Организация:", self.organization)
        visitor_layout.addRow("Дата рождения*:", self.birth_date)
        visitor_layout.addRow("Серия паспорта* (4 цифры):", self.passport_series)
        visitor_layout.addRow("Номер паспорта* (6 цифр):", self.passport_number)
        visitor_group.setLayout(visitor_layout)
        
        docs_group = QGroupBox("Документы")
        docs_layout = QFormLayout()
        
        self.photo_btn = QPushButton("Выбрать фото (3x4, JPG/PNG, до 2MB)")
        self.photo_btn.clicked.connect(lambda: self.upload_file("photo"))
        self.photo_status = QLabel("Не выбрано")
        
        self.passport_scan_btn = QPushButton("Выбрать скан паспорта (JPG, до 4MB)")
        self.passport_scan_btn.clicked.connect(lambda: self.upload_file("passport"))
        self.passport_scan_status = QLabel("Не выбрано")
        
        docs_layout.addRow("Фото посетителя:", self.photo_btn)
        docs_layout.addRow("", self.photo_status)
        docs_layout.addRow("Скан паспорта*:", self.passport_scan_btn)
        docs_layout.addRow("", self.passport_scan_status)
        docs_group.setLayout(docs_layout)
        
        submit_btn = QPushButton("Создать пропуск")
        submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 12px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #2ecc71; }
        """)
        submit_btn.clicked.connect(self.submit_individual_request)
        
        layout.addWidget(pass_group)
        layout.addWidget(host_group)
        layout.addWidget(visitor_group)
        layout.addWidget(docs_group)
        layout.addWidget(submit_btn, alignment=Qt.AlignCenter)
        
        tab.setLayout(layout)
    
    def setup_group_tab(self, tab):
        pass
    
    def upload_file(self, file_type):
        try:
            filters = {
                "photo": "Images (*.jpg *.jpeg *.png)",
                "passport": "Images (*.jpg *.jpeg)"
            }.get(file_type)
            
            max_size = 2 if file_type == "photo" else 4
            
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                f"Выберите {file_type}",
                "",
                filters
            )
            
            if file_path:
                file_size = os.path.getsize(file_path) / (1024 * 1024)
                if file_size > max_size:
                    raise ValueError(f"Максимальный размер файла {max_size}MB")
                
                if file_type == "passport" and not file_path.lower().endswith(('.jpg', '.jpeg')):
                    raise ValueError("Только JPG формат для скана паспорта")
                
                os.makedirs('docs', exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                ext = os.path.splitext(file_path)[1]
                new_filename = f"{file_type}_{timestamp}{ext}"
                new_path = os.path.join('docs', new_filename)
                
                with open(file_path, 'rb') as src, open(new_path, 'wb') as dst:
                    dst.write(src.read())
                
                if file_type == "photo":
                    self.photo_status.setText(os.path.basename(new_path))
                else:
                    self.passport_scan_status.setText(os.path.basename(new_path))
                
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))
    
    def submit_individual_request(self):
        try:
            errors = []
            
            if not self.last_name.text() or not self.first_name.text():
                errors.append("ФИО обязательно")
                
            if not self.email.hasAcceptableInput():
                errors.append("Некорректный email")
                
            if not self.passport_series.hasAcceptableInput():
                errors.append("Серия паспорта - 4 цифры")
                
            if not self.passport_number.hasAcceptableInput():
                errors.append("Номер паспорта - 6 цифр")
                
            if self.passport_scan_status.text() == "Не выбрано":
                errors.append("Скан паспорта обязателен")
                
            if errors:
                raise ValueError("\n".join(errors))
            
            request = {
                "type": "individual",
                "dates": {
                    "start": self.pass_start.date().toString("yyyy-MM-dd"),
                    "end": self.pass_end.date().toString("yyyy-MM-dd")
                },
                "purpose": self.visit_purpose.text(),
                "host": {
                    "department": self.department.currentText(),
                    "employee": self.host_employee.currentText()
                },
                "visitor": {
                    "last_name": self.last_name.text(),
                    "first_name": self.first_name.text(),
                    "middle_name": self.middle_name.text(),
                    "phone": self.phone.text(),
                    "email": self.email.text(),
                    "organization": self.organization.text(),
                    "birth_date": self.birth_date.date().toString("yyyy-MM-dd"),
                    "passport": {
                        "series": self.passport_series.text(),
                        "number": self.passport_number.text()
                    }
                },
                "documents": {
                    "photo": self.photo_status.text(),
                    "passport_scan": self.passport_scan_status.text()
                },
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "created_by": self.user_name
            }
            
            os.makedirs('data/requests', exist_ok=True)
            filename = f"request_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(f'data/requests/{filename}', 'w') as f:
                json.dump(request, f, indent=4, ensure_ascii=False)
            
            QMessageBox.information(self, "Успех", "Пропуск успешно создан!")
            self.clear_form()
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))
    
    def clear_form(self):
        self.pass_start.setDate(QDate.currentDate().addDays(1))
        self.pass_end.setDate(QDate.currentDate().addDays(2))
        self.visit_purpose.clear()
        self.last_name.clear()
        self.first_name.clear()
        self.middle_name.clear()
        self.phone.clear()
        self.email.clear()
        self.organization.clear()
        self.birth_date.setDate(QDate.currentDate().addYears(-30))
        self.passport_series.clear()
        self.passport_number.clear()
        self.photo_status.setText("Не выбрано")
        self.passport_scan_status.setText("Не выбрано")
