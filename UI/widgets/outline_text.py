from PyQt5 import QtGui, QtCore, QtWidgets


class LabelWithOutline(QtWidgets.QLabel):
    def paintEvent(self, QPaintEvent):
        off = 3
        font_size = 15
        shadow_size = 5
        shadow_color = QtGui.QColor("#141414")
        text_color = QtGui.QColor("#cacac8")

        path = QtGui.QPainterPath()
        painter = QtGui.QPainter(self)
        drawFont = QtGui.QFont('Arial Black', font_size)
        path.addText(off, drawFont.pointSize() + off, drawFont, self.text())
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.strokePath(path, QtGui.QPen(shadow_color, shadow_size))
        painter.fillPath(path, QtGui.QBrush(text_color))
        self.resize(path.boundingRect().size().toSize().width() + off * 2,
                    path.boundingRect().size().toSize().height() + off * 2)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication([sys.argv])
    volume = LabelWithOutline()
    volume.show()
    app.exec_()
