from PyQt5 import QtCore, QtWidgets
from widgets.outline_text import LabelWithOutline


class TimeVolumeDisplay(QtWidgets.QMainWindow):
    SHOW_TIME = 3  # in sec

    def __init__(self, parent=None):
        super(TimeVolumeDisplay, self).__init__(parent)
        self.setObjectName("TimeVolumeDisplay")
        self.resize(190, 71)

        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        transparent = '160'
        self.mainWidget = QtWidgets.QWidget(self)
        self.mainWidget.setObjectName("mainWidget")
        self.setStyleSheet("QWidget#TimeVolumeDisplay{background: transparent}")
        self.mainWidget.setStyleSheet("""
            QWidget#mainWidget{{
                    background-color: rgba(114, 114, 112, {transparent});
                    border: 1px solid rgba(178, 178, 178, {transparent});
                    outline: 1px solid rgba(89, 89, 89, {transparent});
                }}

            QLabel{{
                    background-color: transparent;
                    color: rgba(255, 255, 0, {transparent});
                    font-size: 25px;
                }}
                """.format(transparent=transparent))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.mainWidget)
        self.verticalLayout.setContentsMargins(3, 8, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.timeLable = LabelWithOutline(self.mainWidget)
        self.timeLable.setObjectName("timeLable")
        self.verticalLayout.addWidget(self.timeLable)
        self.volumeLable = LabelWithOutline(self.mainWidget)
        self.volumeLable.setObjectName("volumeLable")
        self.verticalLayout.addWidget(self.volumeLable)

        self.hideVolumeTimer = self.createTimer(self.hideVolume)
        self.hideTimeTimer = self.createTimer(self.hideTime)

        self.setCentralWidget(self.mainWidget)
        self.volumeLable.hide()
        self.timeLable.hide()
        self.mainWidget.hide()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.setTime(0, 1)
        self.setVolume(150)

    @staticmethod
    def createTimer(slot):
        timer = QtCore.QTimer()
        timer.timeout.connect(slot)
        timer.setSingleShot(True)
        return timer

    def showTime(self, *, time=SHOW_TIME):
        self.mainWidget.show()
        self.timeLable.show()
        if self.hideTimeTimer.isActive():
            self.hideTimeTimer.stop()
            self.hideTimeTimer = self.createTimer(self.hideTime)

        self.hideTimeTimer.start(time * 1000)

    def showVolume(self, *, time=SHOW_TIME):
        self.mainWidget.show()
        self.volumeLable.show()
        if self.hideVolumeTimer.isActive():
            self.hideVolumeTimer.stop()
            self.hideVolumeTimer = QtCore.QTimer()
            self.hideVolumeTimer = self.createTimer(self.hideVolume)
        self.hideVolumeTimer.start(time * 1000)

    def hideVolume(self):
        self.volumeLable.hide()
        if self.timeLable.isHidden():
            self.mainWidget.hide()

    def hideTime(self):
        self.timeLable.hide()
        if self.volumeLable.isHidden():
            self.mainWidget.hide()

    def setVolume(self, volume):
        self.volumeLable.setText("Volume: {}%".format(volume))

    def setTime(self, ms, movie_length):
        try:
            self.timeLable.setText(self.MStoDate(ms) + " ({}%)".format(int(100*(ms/movie_length))))
        except ZeroDivisionError:
            pass

    @staticmethod
    def MStoDate(ms):
        seconds = ms / 1000
        minutes = seconds // 60
        hours = minutes // 60
        minutes_left = minutes - hours * 60
        seconds_left = seconds - (hours * 3600 + minutes_left * 60)
        return "{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes_left), int(seconds_left))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = TimeVolumeDisplay()
    form.setTime(61 * 1000, 61 * 1000)
    form.setVolume(150)
    form.showTime()
    QtCore.QTimer.singleShot(2000, form.showVolume)
    form.show()
    sys.exit(app.exec_())
