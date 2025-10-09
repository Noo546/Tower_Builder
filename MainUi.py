from PySide6 import QtCore, QtGui, QtWidgets
from shiboken6 import wrapInstance

import maya.OpenMayaUI as omui
from . import util 

ROOT_RESOURCE_DIR = "C:/Users/NAC/Documents/maya/2026/scripts"

class TowerBuilderDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('🏢 Tower Builder')
        self.resize(300, 200)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.setStyleSheet('background-color: #FCF9EA')

        self.imageLabel = QtWidgets.QLabel()
        self.imagePixmap = QtGui.QPixmap(f"{ROOT_RESOURCE_DIR}/TowerBuilder/Image/001")
        scaled_pixmap = self.imagePixmap.scaled(
            QtCore.QSize(300,250),
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
            )
        self.imageLabel.setPixmap(scaled_pixmap)
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(self.imageLabel)

        self.infoLayout = QtWidgets.QHBoxLayout()
        self.scoreLabel = QtWidgets.QLabel("Score: 0")
        self.blockLabel = QtWidgets.QLabel("Blocks: 0")
        self.modeLabel = QtWidgets.QLabel("Mode: EASY")
        self.infoLayout.addWidget(self.scoreLabel)
        self.infoLayout.addWidget(self.blockLabel)
        self.infoLayout.addWidget(self.modeLabel)
        self.mainLayout.addLayout(self.infoLayout)

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.startBtn = QtWidgets.QPushButton("Start Game")
        self.startBtn.setStyleSheet(
            '''
                QPushButton{
                    background-color: #EE7B30;
                    color: white;
                    border-radius: 10px;
                    font-size: 16 px;
                    padding: 8px;
                    font-family: Georgia;
                    font-weighr: bold; 
                }
                QPushButton:hover{
                    background-color: white:
                )
                QPushButton:pressed{
                    background-color: #D1B490:
                }
                }

            '''
        )
        self.dropBtn = QtWidgets.QPushButton("Drop Block")
        self.dropBtn.setStyleSheet(
            '''
                QPushButton{
                    background-color: #EE7B30;
                    color: white;
                    border-radius: 10px;
                    font-size: 16 px;
                    padding: 8px;
                    font-family: Georgia;
                    font-weighr: bold; 
                }
                QPushButton:hover{
                    background-color: white:
                )
                QPushButton:pressed{
                    background-color: #D1B490:
                }
                }

            '''
        )
        self.resetBtn = QtWidgets.QPushButton("Reset")
        self.resetBtn.setStyleSheet(
            '''
                QPushButton{
                    background-color: #EE7B30;
                    color: white;
                    border-radius: 10px;
                    font-size: 16 px;
                    padding: 8px;
                    font-family: Georgia;
                    font-weighr: bold; 
                }
                QPushButton:hover{
                    background-color: white:
                )
                QPushButton:pressed{
                    background-color: #D1B490:
                }
                }

            '''
        )
        self.exitBtn = QtWidgets.QPushButton("Exit")
        self.exitBtn.setStyleSheet(
            '''
                QPushButton{
                    background-color: #EE7B30;
                    color: white;
                    border-radius: 10px;
                    font-size: 16 px;
                    padding: 8px;
                    font-family: Georgia;
                    font-weighr: bold; 
                }
                QPushButton:hover{
                    background-color: white:
                )
                QPushButton:pressed{
                    background-color: #D1B490:
                }
                }

            '''
        )

        self.buttonLayout.addWidget(self.startBtn)
        self.buttonLayout.addWidget(self.dropBtn)
        self.buttonLayout.addWidget(self.resetBtn)
        self.buttonLayout.addWidget(self.exitBtn)
        self.mainLayout.addLayout(self.buttonLayout)

        self.logBox = QtWidgets.QTextEdit()
        self.logBox.setReadOnly(True)
        self.mainLayout.addWidget(self.logBox)

        self.startBtn.clicked.connect(self.startGame)
        self.dropBtn.clicked.connect(self.dropBlock)
        self.resetBtn.clicked.connect(self.resetGame)
        self.exitBtn.clicked.connect(self.close)

        self.score = 0
        self.blockCount = 0
        self.gameActive = False

    def startGame(self):
        self.log("Game started.")
        util.reset_scene()
        util.create_base()
        self.score = 0
        self.blockCount = 0
        self.updateLabels()
        self.gameActive = True

    def dropBlock(self):
        if not self.gameActive:
            self.log("Please start the game first!")
            return
        result = util.drop_new_block(self.blockCount)
        if result:
            self.score += 1
            self.blockCount += 1
            self.log(f"✅ Block {self.blockCount} placed successfully.")
        else:
            self.log("💥 Game Over! Tower collapsed!")
            self.gameActive = False
        self.updateLabels()

    def resetGame(self):
        util.reset_scene()
        self.log("Scene cleared. Ready to restart.")
        self.score = 0
        self.blockCount = 0
        self.updateLabels()
        self.gameActive = False

    def updateLabels(self):
        self.scoreLabel.setText(f"Score: {self.score}")
        self.blockLabel.setText(f"Blocks: {self.blockCount}")

    def log(self, message):
        self.logBox.append(message)

def run():
    global ui
    try:
        ui.close()
    except:
        pass

    ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    ui = TowerBuilderDialog(parent=ptr)
    ui.show()
