from PyQt5.QtCore import Qt, QTimer, QEventLoop
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QTextEdit, QComboBox, QStackedWidget
from score_db import *
from button import *
import random


class Start(QWidget):

    def __init__(self):
        super().__init__()
        self.startUI()
        self.setGeometry(500, 100, 875, 900)
        self.setWindowTitle("game")
        self.nameText = ""

    def startUI(self):
        # startUI -> gameUI 버튼
        self.startButton = Button("START", self)
        self.startButton.setButton(100, 600, 675, 200, 100, self.start_game)

        # 이름 입력 창
        self.nameEdit = QLineEdit(self)
        self.nameEdit.setAlignment(Qt.AlignCenter) # 글자 가운데 정렬
        self.nameEdit.setMaxLength(8) # 글자수 8 제한
        space(self.nameEdit, 250, 380, 540, 140, 30)

        # 이름 라벨
        self.name = QLabel("이름: ", self)
        space(self.name, 90, 420, 200, 50, 30)

        # 난이도 라벨
        self.key = QLabel("난이도:", self)
        space(self.key, 360, 210, 200, 100, 30)

        # 난이도 선택 박스
        self.keys = ["Easy", "Normal", "Hard"]
        self.keyBox = QComboBox(self)
        self.keyBox.addItems(self.keys)
        space(self.keyBox, 575, 210, 200, 100, 25)

        # 난이도에 점수 배수
        self.bonusDic = {"Easy": 1, "Normal": 2, "Hard": 3}

    # start버튼 누르면 호출되는 함수, startUI -> gameUI
    def start_game(self):
        if self.nameEdit.text().strip() == "": # 이름 입력 안했을 때 "익명" 이름 부여
            self.nameEdit.setText("익명")
            self.nameText = self.nameEdit.text()
            self.keyText = self.keyBox.currentText()
            self.bonus = self.bonusDic[self.keyText]
            game.game_setup() # 게임 준비 상태로 만드는 함수
            widget.setCurrentIndex(widget.currentIndex() + 1) # gameUI로 넘어감
        else:
            self.nameText = self.nameEdit.text()
            self.keyText = self.keyBox.currentText()
            self.bonus = self.bonusDic[self.keyText]
            game.game_setup()
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def getBonus(self):
        return self.bonus

    def getNameText(self):
        return self.nameText


class Game(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 100, 875, 900)
        self.setWindowTitle("game")

        # 다용도 텍스트창
        self.display = QLineEdit(self)
        self.display.setReadOnly(True) # 읽기 전용
        self.display.setAlignment(Qt.AlignCenter) # 글자 가운데 정렬
        self.display.setMaxLength(18) # 글자수 18 제한
        space(self.display, 50, 50, 550, 100, 25)

        # 정답 입력창
        self.answer = QLineEdit(self)
        self.answer.setReadOnly(True)
        self.answer.setAlignment(Qt.AlignCenter)
        self.answer.setMaxLength(16)
        space(self.answer, 50, 750, 550, 100, 30)

        # 숫자 버튼 생성 및 숫자 배치
        self.buttons = {}
        num_count = 1
        for y in range(3):
            for x in range(3):
                button = Button(str(num_count), self)
                button.setNumButton(60 + x * 190, 185 + y * 190, self.buttonClicked)
                self.buttons[num_count] = button
                num_count += 1

        # 홈 버튼
        self.home_button = Button("HOME", self)
        self.home_button.setButton(625, 50, 200, 100, 25, self.buttonClicked)

        # 입력완료 버튼
        self.finish_button = Button("FINISH", self)
        self.finish_button.setButton(625, 750, 200, 100, 25, self.buttonClicked)

        # 순위
        self.rank = QLabel("RANK", self)
        space(self.rank, 690, 155, 200, 50, 15)

        # 순위표
        self.rank_display = QTextEdit(self)
        self.rank_display.setReadOnly(True)
        space(self.rank_display, 625, 200, 200, 270, 10)

        # 현재 점수
        self.scoreLabel = QLabel("SCORE", self)
        space(self.scoreLabel, 675, 475, 200, 50, 15)

        # 현재 점수판
        self.score_display = QLineEdit(self)
        self.score_display.setReadOnly(True)
        self.score_display.setAlignment(Qt.AlignCenter)
        space(self.score_display, 625, 525, 200, 200, 70)

    # 버튼 눌렀을 때 호출되는 함수
    def buttonClicked(self):
        button = self.sender()
        key = button.text()

        if key in numPadList: # 숫자 버튼 눌렀을 때
            self.answer.setText(self.answer.text() + key)

        elif key == "HOME": # 홈 버튼 눌렀을 때
            if self.game_status == True: # 게임중이면 게임을 끝냄
                self.game_out()
            widget.setCurrentIndex(widget.currentIndex() - 1) # gameUI ->

        elif key == "FINISH":
            if self.round == 0: # 게임 준비 상태면 게임 시작
                self.game_status = True
                self.round += 1
                self.round_start(self.round) # 1라운드 시작
            else:
                if self.answer.text() == self.round_answer: # 정답이 맞으면 다음 라운드, 마지막 라운드: 16라운드
                    if self.round >= 16: # 16라운드 깨면 게임 클리어
                        self.game_clear()
                    else:
                        self.round += 1 # 다음 라운드 시작
                        self.round_start(self.round)
                else: # 틀렸으면 게임 종료
                    self.game_out()

    # n 라운드 시작 함수
    def round_start(self, n):
        self.count = 10 - int((start.getBonus() - 1) * 2.5) # 시간 제한
        self.score = self.round * start.getBonus() - start.getBonus() # 점수

        self.display.setText("순서를 기억하세요")
        self.answer.setText("")
        self.score_display.setText(str(self.score))

        # 버튼 비활성화 및 버튼 검은색 설정
        for i in range(1, 10):
            self.buttons[i].setDisabled(True)
            self.change_color(i, "black")
        self.sleep(1000) # 1초 대기

        # 이번 라운드 정답 생성 및 버튼 깜빡임
        self.round_answer = ""
        for i in range(n):
            if (self.count >= 1) and (self.game_status == True):
                random_number = random.randint(1, 9)
                self.round_answer += str(random_number)
                self.change_color(random_number, "blue")
                self.sleep(800 - (start.getBonus() - 1) *200 ) # 버튼 켜지는 시간
                self.change_color(random_number, "black")
                self.sleep(200) # 버튼 꺼지는 시간

        # 버튼 활성화
        for i in range(1, 10):
            self.buttons[i].setEnabled(True)

        # 남은 시간 표시
        while (self.count >= 1) and (self.game_status == True):
            self.display.setText(str(self.count))
            self.sleep(1000)
            self.count -= 1
            if self.game_status == False:
                break
            if self.count == 0:
                self.game_out()

    # 버튼 색 변경 함수
    def change_color(self, n, color):
        if color == "blue":
            self.buttons[n].setStyleSheet("background-color: blue")
        elif color == "black":
            self.buttons[n].setStyleSheet("background-color: black")

    # 시간 지연 함수
    def sleep(self, n):
        loop = QEventLoop()
        QTimer.singleShot(n, loop.quit)
        loop.exec_()

    # 게임 종료 함수
    def game_out(self):
        self.game_status = False
        self.display.setText("실패!")
        self.finish_button.setDisabled(True)
        self.display.setDisabled(True)
        for i in range(1, 10):
            self.buttons[i].setDisabled(True)
            self.change_color(i, "black")
        scoredb.addScore(start.getNameText(), self.score)
        self.rank_display.setText(scoredb.rankDB())

    # 게임 클리어 함수
    def game_clear(self):
        self.game_status = False
        self.display.setText("☆GAME CLEAR!☆")
        self.finish_button.setDisabled(True)
        self.display.setDisabled(True)
        for i in range(1, 10):
            self.buttons[i].setDisabled(True)
        scoredb.addScore(start.getNameText(), self.score + start.getBonus())
        self.score_display.setText(str(self.score + start.getBonus()))
        self.rank_display.setText(scoredb.rankDB())

    # 게임 준비 함수
    def game_setup(self):
        self.display.setText("FINISH를 눌러 시작")
        self.answer.setText("누른 버튼 표시")
        for i in range(1, 10):
            self.buttons[i].setDisabled(True)
        self.rank_display.setText(scoredb.rankDB())
        self.round = 0
        self.score = 0
        self.score_display.setText(str(self.score))
        self.finish_button.setEnabled(True)
        self.game_status = False


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    widget = QStackedWidget()

    scoredb = ScoreDB()
    start = Start()
    game = Game()

    widget.addWidget(start)
    widget.addWidget(game)

    widget.setWindowTitle("game")

    widget.setGeometry(500, 100, 875, 900)
    widget.setFixedSize(875, 900)
    widget.show()

    sys.exit(app.exec_())
