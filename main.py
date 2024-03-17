from PySide6.QtWidgets import QApplication, QMainWindow
from workspace import Workspace

class PhotoEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photo Editor")
        self.setGeometry(500, 500, 800, 800)
        
        self.setCentralWidget(Workspace())
        self.showMaximized()

if __name__ == "__main__":
    app = QApplication()
    ex = PhotoEditor()
    app.exec()