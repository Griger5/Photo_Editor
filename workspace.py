from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QGridLayout, QFileDialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('QtAgg')

class Workspace(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):
        placeholderbut1 = QPushButton("Placeholder")
        placeholderbut2 = QPushButton("Placeholder")
        placeholderbut3 = QPushButton("Placeholder")
        placeholderbut4 = QPushButton("Placeholder")
        self.setStyleSheet("QPushButton {margin-left: 60px; margin-right: 60px; padding-top: 15px; padding-bottom: 15px;}")

        self.openFileButton = QPushButton("Open an image")
        self.openFileButton.setStyleSheet("margin-left: 300px; margin-right: 300px; padding-top: 10px; padding-bottom: 10px;")

        vLayoutLeft = QVBoxLayout()
        vLayoutRight = QVBoxLayout()
        self.mainLayout = QGridLayout()

        vLayoutLeft.addWidget(placeholderbut1)
        vLayoutLeft.addWidget(placeholderbut2)
        vLayoutRight.addWidget(placeholderbut3)
        vLayoutRight.addWidget(placeholderbut4)

        self.mainLayout.addLayout(vLayoutLeft, 0, 0, 5, 1)
        self.mainLayout.addWidget(self.openFileButton, 0, 2, 5, 3)
        self.mainLayout.addLayout(vLayoutRight, 0, 5, 5, 1)

        self.setLayout(self.mainLayout)

        self.openFileButton.clicked.connect(self.openFile)

    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(self)
        
        if filename:
            self.show_image(filename)

    def show_image(self, file):
        self.openFileButton.deleteLater()
        self.sc = MplCanvas(self)
        img = plt.imread(file)
        img = np.asarray(img)
        if file.lower().endswith(".png"):
            img = (img[:,:,[0,1,2]]*255).astype(int)
            self.sc.axes.imshow(img)
            self.mainLayout.addWidget(self.sc, 0, 2, 5, 3)
        elif file.lower().endswith((".jpg", ".jpeg", ".webp")):
            self.sc.axes.imshow(img)
            self.mainLayout.addWidget(self.sc, 0, 2, 5, 3)
        else:
            ...


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=1, height=1, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.axis("off")
        self.axes.margins(x=0, y=0)
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        super(MplCanvas, self).__init__(fig)