from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

numPadList = [
    '1', '2', '3',
    '4', '5', '6',
    '7', '8', '9',
]


class Button(QPushButton):
    def setNumButton(self, x, y, callback):
        self.move(x, y)
        self.resize(150, 150)
        self.setFont(QFont('Times', 80))
        self.clicked.connect(callback)

    def setButton(self, x, y, a, b, s, callback):
        self.move(x, y)
        self.resize(a, b)
        self.setFont(QFont("Times", s))
        self.clicked.connect(callback)


def space(Widget, x, y, a, b, s):
    Widget.move(x, y)
    Widget.resize(a, b)
    Widget.setFont(QFont("Times", s))
