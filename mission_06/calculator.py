import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, 
    QVBoxLayout, QGridLayout, QPushButton, QLabel)
from PyQt6.QtCore import Qt

class IPhoneCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('iPhone Calculator')
        self.setFixedSize(320, 550)
        self.setStyleSheet('background-color: black;')
        
        self.current_value = '0'
        self.reset_display = False # 결과 출력 후 새 숫자 입력 시 초기화용
        self.initUI()

    def initUI(self):
        central_widget = QWidget() # 중앙에 넣을 위젯 생성
        self.setCentralWidget(central_widget) # central_widget을 QMainWindow의 중앙 위젯으로 설정(중앙 위젯에는 한 번에 한 위젯만 설정 가능)
        main_layout = QVBoxLayout(central_widget) # 수직 박스 레이아웃으로 여러 위젯 배치할 수 있음
        main_layout.setContentsMargins(10, 10, 10, 20)
        main_layout.setSpacing(10)

        # 1. 출력창
        self.display = QLabel(self.current_value)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.display.setStyleSheet('color: white; font-size: 70px; padding: 10px;')
        main_layout.addWidget(self.display)

        # 2. 버튼 데이터
        buttons = [
            ('AC', 0, 0, '#A5A5A5', 'black'), ('+/-', 0, 1, '#A5A5A5', 'black'), ('%', 0, 2, '#A5A5A5', 'black'), ('÷', 0, 3, '#FF9F0A', 'white'),
            ('7', 1, 0, '#333333', 'white'), ('8', 1, 1, '#333333', 'white'), ('9', 1, 2, '#333333', 'white'), ('×', 1, 3, '#FF9F0A', 'white'),
            ('4', 2, 0, '#333333', 'white'), ('5', 2, 1, '#333333', 'white'), ('6', 2, 2, '#333333', 'white'), ('－', 2, 3, '#FF9F0A', 'white'),
            ('1', 3, 0, '#333333', 'white'), ('2', 3, 1, '#333333', 'white'), ('3', 3, 2, '#333333', 'white'), ('＋', 3, 3, '#FF9F0A', 'white'),
            ('0', 4, 0, '#333333', 'white', 2), ('.', 4, 2, '#333333', 'white'), ('＝', 4, 3, '#FF9F0A', 'white')
        ]

        grid_layout = QGridLayout()
        grid_layout.setSpacing(12)
        
        for btn_info in buttons:
            text, row, col, bg, color = btn_info[:5] # 앞에서 5개 데이터를 각각 변수에 한 번에 담기
            # Python 삼항 연산자 : 참 if 조건 else 거짓
            colspan = btn_info[5] if len(btn_info) > 5 else 1 # 6번 데이터(5번 인덱스)가 존재하는 경우 colspan 변수에 저장
            
            button = QPushButton(text)
            # 0번 버튼을 위해 가변 크기 대응
            button.setFixedSize(70 * colspan + (12 if colspan > 1 else 0), 70)
            
            style = f"""
                QPushButton {{
                    background-color: {bg};
                    color: {color};
                    border-radius: 35px;
                    font-size: 28px;
                    font-weight: 500;
                }}
                QPushButton:pressed {{
                    background-color: #777777;
                }}
            """
            button.setStyleSheet(style)
            button.clicked.connect(self.on_click)
            grid_layout.addWidget(button, row, col, 1, colspan)

        main_layout.addLayout(grid_layout)

    def on_click(self):
        button = self.sender() # 이벤트 발생지 추적
        key = button.text()

        if key == 'AC':
            self.current_value = '0'
        elif key == '+/-':
            if self.current_value.startswith('-'):
                self.current_value = self.current_value[1:]
            elif self.current_value != '0':
                self.current_value = '-' + self.current_value
        elif key == '%':
            try:
                self.current_value = str(float(self.current_value) / 100)
            except:
                self.current_value = "Error"
        elif key == '=':
            try:
                # 결과 계산 시 보안을 위해 정해진 기호만 허용 (간단한 eval)
                result = eval(self.current_value) # eval() : 문자열을 파이썬 코드로 변환하여 실행
                # 정수면 소수점 제거 (.0 방지)
                if result == int(result):
                    self.current_value = str(int(result))
                else:
                    self.current_value = str(round(result, 8))
                self.reset_display = True # 계산 직후 숫자를 누르면 새로 시작하도록 설정
            except:
                self.current_value = "Error"
        elif key in ['+', '-', '*', '/']:
            # 연산자가 마지막에 있을 때 또 연산자를 누르면 교체
            if self.current_value[-1] in ['+', '-', '*', '/']:
                self.current_value = self.current_value[:-1] + key
            else:
                self.current_value += key
            self.reset_display = False
        else: # 숫자 및 소수점
            if self.reset_display or self.current_value == "0":
                if key == '.':
                    self.current_value = "0."
                else:
                    self.current_value = key
                self.reset_display = False
            else:
                # 소수점 중복 입력 방지
                if key == '.' and self.current_value.split()[-1].count('.'):
                    pass
                else:
                    self.current_value += key

        # 글자 수에 따른 폰트 크기 조절 (아이폰 특유의 반응형 텍스트)
        length = len(self.current_value)
        if length > 6:
            self.display.setStyleSheet("color: white; font-size: 40px; padding: 10px;")
        else:
            self.display.setStyleSheet("color: white; font-size: 70px; padding: 10px;")

        self.display.setText(self.current_value)

if __name__ == "__main__":
    app = QApplication(sys.argv) # QT 프로그램 엔진 켜기 # sys.argv는 프로그램을 실행할 때 전달하는 인자값들을 Qt 엔진에 넘겨주는 역할
    calc = IPhoneCalculator()
    calc.show()
    sys.exit(app.exec())

