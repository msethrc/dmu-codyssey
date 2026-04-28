import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, 
    QVBoxLayout, QGridLayout, QPushButton, QLabel)
from PyQt6.QtCore import Qt

# Calculator 클래스 MVC 패턴 적용
# --- MODEL ---
class CalculatorModel:
    # 사칙 연산 담당 메소드
    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b
    def divide(self, a, b): 
        return a / b if b != 0 else 'Error'

    def percent(self, value):
        try: return float(value) / 100
        except: return "Error"

    def negate(self, value):
        if value == '0': return '0'
        return str(-float(value))

# --- VIEW ---
class CalculatorView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('iPhone Calculator')
        self.setFixedSize(320, 600)
        self.setStyleSheet('background-color: black;')
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 20, 15, 25)
        main_layout.setSpacing(12)

        # 디스플레이 설정
        self.display = QLabel('0')
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.display.setStyleSheet('color: white; font-size: 70px; padding-bottom: 20px;')
        main_layout.addWidget(self.display)

        # 버튼 구성 (텍스트, 행, 열, 타입, 열 확장)
        buttons = [
            ('AC', 0, 0, 'func'), ('+/-', 0, 1, 'func'), ('%', 0, 2, 'func'), ('÷', 0, 3, 'oper'),
            ('7', 1, 0, 'digit'), ('8', 1, 1, 'digit'), ('9', 1, 2, 'digit'), ('×', 1, 3, 'oper'),
            ('4', 2, 0, 'digit'), ('5', 2, 1, 'digit'), ('6', 2, 2, 'digit'), ('-', 2, 3, 'oper'),
            ('1', 3, 0, 'digit'), ('2', 3, 1, 'digit'), ('3', 3, 2, 'digit'), ('+', 3, 3, 'oper'),
            ('0', 4, 0, 'digit', 2), ('.', 4, 2, 'digit'), ('=', 4, 3, 'oper')
        ]

        grid_layout = QGridLayout()
        grid_layout.setSpacing(12)
        
        self.btns = {} # 버튼 객체 저장용

        for btn_info in buttons:
            text = btn_info[0]
            row, col = btn_info[1], btn_info[2]
            b_type = btn_info[3]
            colspan = btn_info[4] if len(btn_info) > 4 else 1
            
            btn = QPushButton(text)
            self.btns[text] = btn
            
            # 스타일 지정
            bg_color = {'func': '#A5A5A5', 'oper': '#FF9F0A', 'digit': '#333333'}[b_type]
            text_color = 'black' if b_type == 'func' else 'white'
            
            btn.setFixedSize(70 * colspan + (12 if colspan > 1 else 0), 70)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {bg_color};
                    color: {text_color};
                    border-radius: 35px;
                    font-size: 26px;
                    font-weight: bold;
                }}
                QPushButton:pressed {{ background-color: #CCCCCC; }}
            """)
            grid_layout.addWidget(btn, row, col, 1, colspan)

        main_layout.addLayout(grid_layout)

    # 보너스 : 글자 수에 따른 폰트 크기 조절
    def update_display(self, text):
        length = len(str(text))
        if length > 12: font_size = 30
        elif length > 8: font_size = 45
        elif length > 5: font_size = 60
        else: font_size = 70
        
        self.display.setStyleSheet(f"color: white; font-size: {font_size}px; padding-bottom: 20px;")
        self.display.setText(str(text))

# --- CONTROLLER ---
class CalculatorController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # 계산 상태 변수
        self.display_text = '0'
        self.first_operand = None
        self.operator = None
        self.reset_display = False
        
        self.connect_signals()

    def connect_signals(self):
        for text, btn in self.view.btns.items():
            btn.clicked.connect(lambda ch, t=text: self.on_button_click(t))

    def on_button_click(self, key):
        if key.isdigit():
            self.append_digit(key)
        elif key == '.':
            self.append_dot()
        elif key in ['+', '-', '×', '÷']:
            self.set_operator(key)
        elif key == '=':
            self.equal()
        elif key == 'AC':
            self.reset()
        elif key == '+/-':
            self.negative_positive()
        elif key == '%':
            self.percent()

    # 숫자 입력
    def append_digit(self, digit):
        if self.reset_display or self.display_text == '0':
            self.display_text = digit
            self.reset_display = False
        else:
            self.display_text += digit
        self.view.update_display(self.display_text)

    # 소수점 입력
    def append_dot(self):
        if self.reset_display: # 연산자가 입력 직후 소수점 입력 시 0.으로 시작
            self.display_text = '0.'
            self.reset_display = False
        elif '.' not in self.display_text: # 이미 소수점이 입력되어 있는 상태에서는 추가로 입력되지 않음
            self.display_text += '.'
        self.view.update_display(self.display_text)

    # 연산자 입력: 
    def set_operator(self, op):
        self.first_operand = float(self.display_text)
        self.operator = op
        self.reset_display = True

    # 결과 출력
    def equal(self):
        if self.operator is None:
            return

        second_operand = float(self.display_text)
        result = 0

        if self.operator == '+': result = self.model.add(self.first_operand, second_operand)
        elif self.operator == '-': result = self.model.subtract(self.first_operand, second_operand)
        elif self.operator == '×': result = self.model.multiply(self.first_operand, second_operand)
        elif self.operator == '÷': result = self.model.divide(self.first_operand, second_operand)

        # 보너스 : 결과 처리 (정수면 .0 제거, 소수면 6자리 반올림)
        if isinstance(result, float):
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 6)

        self.display_text = str(result)
        self.view.update_display(self.display_text)
        self.operator = None
        self.reset_display = True

    # 초기화
    def reset(self):
        self.display_text = '0'
        self.first_operand = None
        self.operator = None
        self.reset_display = False
        self.view.update_display(self.display_text)

    # 음수/양수
    def negative_positive(self):
        self.display_text = self.model.negate(self.display_text)
        self.view.update_display(self.display_text)

    # 퍼센트
    def percent(self):
        calc_value = self.model.percent(self.display_text)
        self.display_text = str(round(calc_value, 6)) if isinstance(calc_value, float) else calc_value
        self.view.update_display(self.display_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    model = CalculatorModel()
    view = CalculatorView()
    controller = CalculatorController(model, view)
    
    view.show()
    sys.exit(app.exec())
