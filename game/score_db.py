import pickle
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLabel,
    QComboBox, QTextEdit, QLineEdit)
from PyQt5.QtCore import Qt


class ScoreDB(QWidget):
    def __init__(self):
        super().__init__()
        self.dbfilename = 'rankDB.dat'
        self.scoredb = []
        self.readScoreDB()

    def readScoreDB(self):
        try:
            fH = open(self.dbfilename, 'rb')
        except FileNotFoundError as e:
            self.scoredb = []
            return

        try:
            self.scoredb = pickle.load(fH)
        except:
            pass
        else:
            pass
        fH.close()

    def writeScoreDB(self):
        fH = open(self.dbfilename, 'wb')
        pickle.dump(self.scoredb, fH)
        fH.close()

    def rankDB(self):
        try:
            tempText = ""
            rank = 1
            for p in sorted(self.scoredb, key=lambda person: person["Score"], reverse=True):
                tempText += str(p["Score"]) + "." + p["Name"] + "\n"
                rank += 1
                if rank > 10:
                    break
            return tempText
        except:
            pass

    def addScore(self, name, score):
        tempdic = {}
        tempdic["Name"] = name
        tempdic["Score"] = score
        self.scoredb.append(tempdic)
        self.writeScoreDB()