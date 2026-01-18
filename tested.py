#!/usr/bin/env python3
"""
Простой тестовый GUI для обфускатора
Калькулятор с кнопками и полем ввода
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, 
                            QVBoxLayout, QHBoxLayout, QLineEdit, 
                            QPushButton, QLabel, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class SimpleCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create By @twix and perplexity ai")
        self.setGeometry(300, 300, 300, 400)
        
        # Центральный виджет
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)
        
        # Дисплей
        self.display = QLineEdit()
        self.display.setFont(QFont("Arial", 16))
        self.display.setAlignment(Qt.AlignRight)
        layout.addWidget(self.display)
        
        # Кнопки цифр
        buttons = [
            ('C', self.clear),
            ('7', self.button_click),
            ('8', self.button_click),
            ('9', self.button_click),
            ('/', self.button_click),
            ('4', self.button_click),
            ('5', self.button_click),
            ('6', self.button_click),
            ('*', self.button_click),
            ('1', self.button_click),
            ('2', self.button_click),
            ('3', self.button_click),
            ('-', self.button_click),
            ('0', self.button_click),
            ('.', self.button_click),
            ('=', self.calculate),
            ('+', self.button_click)
        ]
        
        # Создание сетки кнопок
        for i, (text, func) in enumerate(buttons):
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, f=func, t=text: f(t))
            btn.setFont(QFont("Arial", 14))
            layout.addWidget(btn)
        
        # Заголовок
        title = QLabel("Калькулятор")
        title.setFont(QFont("Arial", 12))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
    
    def button_click(self, text):
        """Обработка клика по кнопке"""
        current = self.display.text()
        self.display.setText(current + text)
    
    def clear(self, text):
        """Очистка дисплея"""
        self.display.clear()
    
    def calculate(self, text):
        """Вычисление результата"""
        try:
            result = eval(self.display.text())
            self.display.setText(str(result))
        except Exception:
            QMessageBox.warning(self, "Ошибка", "Неверное выражение!")
    
    def keyPressEvent(self, event):
        """Поддержка клавиатуры"""
        key = event.text()
        if key.isdigit() or key in '+-*/.':
            self.button_click(key)
        elif key == 'Enter' or key == '=':
            self.calculate('')
        elif key == 'C' or key == 'c':
            self.clear('')

def main():
    app = QApplication(sys.argv)
    calc = SimpleCalculator()
    calc.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

