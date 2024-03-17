from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QGridLayout, QFileDialog
import numpy as np
import matplotlib.pyplot as plt
from canvas import MplCanvas

class Workspace(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):
        self.addRedButton = QPushButton("Add Red")
        self.addRedButtonx10 = QPushButton("x10")
        self.addRedButtonx25 = QPushButton("x25")
        self.addRedButtonx50 = QPushButton("x50")
        self.addRedButtonReverse = QPushButton("Reverse")
        self.addRedButtonReverse.setCheckable(True)
        addRedLayout = QGridLayout()
        addRedLayout.addWidget(self.addRedButton, 0, 0, 1, 4)
        addRedLayout.addWidget(self.addRedButtonx10, 1, 0)
        addRedLayout.addWidget(self.addRedButtonx25, 1, 1)
        addRedLayout.addWidget(self.addRedButtonx50, 1, 2)
        addRedLayout.addWidget(self.addRedButtonReverse, 1, 3)

        self.addGreenButton = QPushButton("Add Green")
        self.addGreenButtonx10 = QPushButton("x10")
        self.addGreenButtonx25 = QPushButton("x25")
        self.addGreenButtonx50 = QPushButton("x50")
        self.addGreenButtonReverse = QPushButton("Reverse")
        self.addGreenButtonReverse.setCheckable(True)
        addGreenLayout = QGridLayout()
        addGreenLayout.addWidget(self.addGreenButton, 0, 0, 1, 4)
        addGreenLayout.addWidget(self.addGreenButtonx10, 1, 0)
        addGreenLayout.addWidget(self.addGreenButtonx25, 1, 1)
        addGreenLayout.addWidget(self.addGreenButtonx50, 1, 2)
        addGreenLayout.addWidget(self.addGreenButtonReverse, 1, 3)

        self.addBlueButton = QPushButton("Add Blue")
        self.addBlueButtonx10 = QPushButton("x10")
        self.addBlueButtonx25 = QPushButton("x25")
        self.addBlueButtonx50 = QPushButton("x50")
        self.addBlueButtonReverse = QPushButton("Reverse")
        self.addBlueButtonReverse.setCheckable(True)
        addBlueLayout = QGridLayout()
        addBlueLayout.addWidget(self.addBlueButton, 0, 0, 1, 4)
        addBlueLayout.addWidget(self.addBlueButtonx10, 1, 0)
        addBlueLayout.addWidget(self.addBlueButtonx25, 1, 1)
        addBlueLayout.addWidget(self.addBlueButtonx50, 1, 2)
        addBlueLayout.addWidget(self.addBlueButtonReverse, 1, 3)

        # we iterate through all the layouts' widgets to set stylesheets on them
        # all layouts have the same count of widgets
        index = addRedLayout.count()-1
        while(index >= 0):
            widget = addRedLayout.itemAt(index).widget()
            widget.setStyleSheet("margin-left: 10px; margin-right: 10px; padding-top: 10px; padding-bottom: 10px;")
            widget = addGreenLayout.itemAt(index).widget()
            widget.setStyleSheet("margin-left: 10px; margin-right: 10px; padding-top: 10px; padding-bottom: 10px;")
            widget = addBlueLayout.itemAt(index).widget()
            widget.setStyleSheet("margin-left: 10px; margin-right: 10px; padding-top: 10px; padding-bottom: 10px;")
            index -= 1

        placeholderbut3 = QPushButton("Placeholder")
        placeholderbut4 = QPushButton("Placeholder")
        self.setStyleSheet("QPushButton {margin-left: 60px; margin-right: 60px; padding-top: 15px; padding-bottom: 15px;}")

        self.openFileButton = QPushButton("Open an image")
        self.openFileButton.setStyleSheet("margin-left: 300px; margin-right: 300px; padding-top: 10px; padding-bottom: 10px;")

        vLayoutLeft = QVBoxLayout()
        vLayoutRight = QVBoxLayout()
        self.mainLayout = QGridLayout()

        vLayoutLeft.addLayout(addRedLayout)
        vLayoutLeft.addLayout(addGreenLayout)
        vLayoutLeft.addLayout(addBlueLayout)
        vLayoutRight.addWidget(placeholderbut3)
        vLayoutRight.addWidget(placeholderbut4)

        self.mainLayout.addLayout(vLayoutLeft, 0, 0, 5, 1)
        self.mainLayout.addWidget(self.openFileButton, 0, 2, 5, 3)
        self.mainLayout.addLayout(vLayoutRight, 0, 5, 5, 1)

        self.setLayout(self.mainLayout)

        self.openFileButton.clicked.connect(self.openFile)

    def initFunc(self):
        self.addRedButton.clicked.connect(lambda: self.canvas.addColor("r", 1))
        self.addRedButtonx10.clicked.connect(lambda: self.canvas.addColor("r", 10))
        self.addRedButtonx25.clicked.connect(lambda: self.canvas.addColor("r", 25))
        self.addRedButtonx50.clicked.connect(lambda: self.canvas.addColor("r", 50))
        self.addRedButtonReverse.clicked.connect(lambda: self.canvas.reverseAddColor("r"))

        self.addGreenButton.clicked.connect(lambda: self.canvas.addColor("g", 1))
        self.addGreenButtonx10.clicked.connect(lambda: self.canvas.addColor("g", 10))
        self.addGreenButtonx25.clicked.connect(lambda: self.canvas.addColor("g", 25))
        self.addGreenButtonx50.clicked.connect(lambda: self.canvas.addColor("g", 50))
        self.addGreenButtonReverse.clicked.connect(lambda: self.canvas.reverseAddColor("g"))

        self.addBlueButton.clicked.connect(lambda: self.canvas.addColor("b", 1))
        self.addBlueButtonx10.clicked.connect(lambda: self.canvas.addColor("b", 10))
        self.addBlueButtonx25.clicked.connect(lambda: self.canvas.addColor("b", 25))
        self.addBlueButtonx50.clicked.connect(lambda: self.canvas.addColor("b", 50))
        self.addBlueButtonReverse.clicked.connect(lambda: self.canvas.reverseAddColor("b"))

    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(self)
        
        if filename.lower().endswith((".jpg", ".jpeg", ".webp", ".png")):
            self.openFileButton.deleteLater()
            self.canvas = MplCanvas(file=filename)
            self.mainLayout.addWidget(self.canvas, 0, 2, 5, 3)
            self.initFunc()
        else:
            ...