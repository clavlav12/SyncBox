from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setGeometry(0, 0, 1920, 1080)
        self.initUI()
        self.show()

    def initUI(self):
        pass

    # def event(self, event: QEvent) -> bool:
    #     print(event)
    #     return super().event(event)
    #
    def keyPressEvent(self, a0: QKeyEvent) -> None:
        print(a0)


if __name__ == '__main__':
        app = QApplication(sys.argv)
        main = Main()
        sys.exit(app.exec_())
