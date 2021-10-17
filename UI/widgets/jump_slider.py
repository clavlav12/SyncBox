from PyQt5 import QtGui, QtCore, QtWidgets


class JumpSlider(QtWidgets.QSlider):
    def __init__(self, parent=None):
        super(JumpSlider, self).__init__(parent)
        self.pressed = False
        self.valToChange = None

    def mousePressEvent(self, event):
        super(JumpSlider, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            val = self.pixelPosToRangeValue(event.pos())
            self.setValue(val)
            self.pressed = True

    def mouseReleaseEvent(self, QMouseEvent):
        super(JumpSlider, self).mouseReleaseEvent(QMouseEvent)
        self.pressed = False
        if self.valToChange is not None:
            self.setValue(self.valToChange)
        self.valToChange = None

    def pixelPosToRangeValue(self, pos):
        opt = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(opt)
        gr = self.style().subControlRect(QtWidgets.QStyle.CC_Slider, opt, QtWidgets.QStyle.SC_SliderGroove, self)
        sr = self.style().subControlRect(QtWidgets.QStyle.CC_Slider, opt, QtWidgets.QStyle.SC_SliderHandle, self)

        if self.orientation() == QtCore.Qt.Horizontal:
            sliderLength = sr.width()
            sliderMin = gr.x()
            sliderMax = gr.right() - sliderLength + 1
        else:
            sliderLength = sr.height()
            sliderMin = gr.y()
            sliderMax = gr.bottom() - sliderLength + 1;
        pr = pos - sr.center() + sr.topLeft()
        p = pr.x() if self.orientation() == QtCore.Qt.Horizontal else pr.y()
        return QtWidgets.QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), p - sliderMin,
                                               sliderMax - sliderMin, opt.upsideDown)

    def signalBLockedValueChange(self, val):
        self.blockSignals(True)
        self.setValue(val)
        self.blockSignals(False)

    def hold(self):
        return self.pressed

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication([sys.argv])
    volume = JumpSlider()
    volume.show()
    app.exec_()
