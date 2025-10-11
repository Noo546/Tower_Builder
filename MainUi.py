from PySide6 import QtCore, QtGui, QtWidgets
from shiboken6 import wrapInstance
import maya.OpenMayaUI as omui
from . import util

ROOT_RESOURCE_DIR = "C:/Users/NAC/Documents/maya/2026/scripts"

# ---------------- SETTINGS DIALOG ----------------
class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, current_mode="EASY"):
        super().__init__(parent)
        self.setWindowTitle("Game Settings")
        self.resize(200, 150)
        self.setStyleSheet("""
            background-color: #FCF9EA;
            color: black;
            font-family: Georgia;
        """)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.label = QtWidgets.QLabel("Select Difficulty Mode:")
        self.mainLayout.addWidget(self.label)

        # Radio buttons for modes
        self.easyRadio = QtWidgets.QRadioButton("Easy")
        self.normalRadio = QtWidgets.QRadioButton("Normal")
        self.hardRadio = QtWidgets.QRadioButton("Hard")

        if current_mode == "EASY":
            self.easyRadio.setChecked(True)
        elif current_mode == "NORMAL":
            self.normalRadio.setChecked(True)
        else:
            self.hardRadio.setChecked(True)

        self.mainLayout.addWidget(self.easyRadio)
        self.mainLayout.addWidget(self.normalRadio)
        self.mainLayout.addWidget(self.hardRadio)

        # Apply / Cancel buttons
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.applyBtn = QtWidgets.QPushButton("Apply")
        self.cancelBtn = QtWidgets.QPushButton("Cancel")

        for btn in [self.applyBtn, self.cancelBtn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #EE7B30;
                    color: black;
                    border-radius: 8px;
                    font-size: 14px;
                    padding: 6px;
                    font-family: Georgia;
                }
                QPushButton:hover {
                    background-color: #F9B872;
                    color: black;
                }
            """)
            self.buttonLayout.addWidget(btn)

        self.mainLayout.addLayout(self.buttonLayout)

        self.applyBtn.clicked.connect(self.accept)
        self.cancelBtn.clicked.connect(self.reject)

    def selectedMode(self):
        if self.easyRadio.isChecked():
            return "EASY"
        elif self.normalRadio.isChecked():
            return "NORMAL"
        else:
            return "HARD"


# ---------------- MAIN TOWER BUILDER UI ----------------
class TowerBuilderDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('🏢 Tower Builder')
        self.resize(300, 250)
        self.setStyleSheet('background-color: #FCF9EA; color: black; font-family: Georgia;')

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        # ---------- HEADER IMAGE ----------
        self.imageLabel = QtWidgets.QLabel()
        self.imagePixmap = QtGui.QPixmap(f"{ROOT_RESOURCE_DIR}/TowerBuilder/Image/001.png")
        scaled_pixmap = self.imagePixmap.scaled(
            QtCore.QSize(300, 180),
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        self.imageLabel.setPixmap(scaled_pixmap)
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(self.imageLabel)

        # ---------- INFO ----------
        self.infoLayout = QtWidgets.QHBoxLayout()
        self.scoreLabel = QtWidgets.QLabel("Score: 0")
        self.blockLabel = QtWidgets.QLabel("Blocks: 0")
        self.modeLabel = QtWidgets.QLabel("Mode: EASY")
        self.infoLayout.addWidget(self.scoreLabel)
        self.infoLayout.addWidget(self.blockLabel)
        self.infoLayout.addWidget(self.modeLabel)
        self.mainLayout.addLayout(self.infoLayout)

        # ---------- BUTTONS ----------
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.startBtn = QtWidgets.QPushButton("Start Game")
        self.dropBtn = QtWidgets.QPushButton("Drop Block")
        self.resetBtn = QtWidgets.QPushButton("Reset")
        self.settingBtn = QtWidgets.QPushButton("Settings")

        for btn in [self.startBtn, self.dropBtn, self.resetBtn, self.settingBtn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #EE7B30;
                    color: black;
                    border-radius: 8px;
                    font-size: 14px;
                    padding: 6px;
                    font-family: Georgia;
                }
                QPushButton:hover {
                    background-color: #F9B872;
                    color: black;
                }
            """)
            self.buttonLayout.addWidget(btn)

        self.mainLayout.addLayout(self.buttonLayout)

        # ---------- LOG BOX ----------
        self.logBox = QtWidgets.QTextEdit()
        self.logBox.setReadOnly(True)
        self.logBox.setStyleSheet("color: black; background-color: #FFFBEA;")
        self.mainLayout.addWidget(self.logBox)

        # ---------- SIGNALS ----------
        self.startBtn.clicked.connect(self.startGame)
        self.dropBtn.clicked.connect(self.dropBlock)
        self.resetBtn.clicked.connect(self.resetGame)
        self.settingBtn.clicked.connect(self.openSettings)

        # ---------- STATE ----------
        self.score = 0
        self.blockCount = 0
        self.gameActive = False
        self.currentMode = "EASY"

    # ---------- GAME FUNCTIONS ----------
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
        result = util.dropBlock(self.blockCount)
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

    def openSettings(self):
        dialog = SettingsDialog(self, self.currentMode)
        if dialog.exec():
            self.currentMode = dialog.selectedMode()
            self.modeLabel.setText(f"Mode: {self.currentMode}")
            self.log(f"Changed mode to {self.currentMode}")

    # ---------- UI HELPERS ----------
    def updateLabels(self):
        self.scoreLabel.setText(f"Score: {self.score}")
        self.blockLabel.setText(f"Blocks: {self.blockCount}")

    def log(self, message):
        self.logBox.append(message)


# ---------------- RUN DIALOG ----------------
def run():
    global ui
    try:
        ui.close()
    except:
        pass

    ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    ui = TowerBuilderDialog(parent=ptr)
    ui.show()
