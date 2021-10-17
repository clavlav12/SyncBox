# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'getIP.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from functools import reduce
import warnings
import copy
import re


class IpLines:
    def __init__(self, parent):
        self.parent = parent
        IPLineEdit.reset(parent)
        for i in range(4):
            IPLineEdit(parent.frame_2, parent.horizontalLayout, i)
            if not i == 3:
                label = QtWidgets.QLabel(parent.frame_2)
                label.setMaximumSize(QtCore.QSize(16777215, 20))
                parent.horizontalLayout.addWidget(label)
                label.setText('.')
        IPLineEdit.lines[0].setFocus()
        IPLineEdit.setTabOrder_(parent)

    def getIP(self):
        return IPLineEdit.getIP()


class IPLineEdit(QtWidgets.QLineEdit):
    lines = []
    dialog = None
    paste = QtCore.pyqtSignal()
    reg_ex = QtCore.QRegExp('^(0{0,2}[0-9]|0?[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$')
    input_validator = QtGui.QRegExpValidator(reg_ex)
    ip_regex = re.compile(r'(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}'
                          r'([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])')

    def __init__(self, parent, layout, index):
        super(IPLineEdit, self).__init__(parent)
        self.setMaximumSize(QtCore.QSize(16777215, 20))
        self.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        layout.addWidget(self)
        self.setValidator(self.input_validator)
        self.index = index
        self.textChanged.connect(self.checkFinished)
        self.paste.connect(self.linePaste)
        self.lines.append(self)

    def finished(self, text):
        length = len(text)
        if length == 3:
            return True
        elif length == 2:
            if int(text[0]) > 2:  # 34
                return True
            elif int(text[0]) == 2 and int(text[1]) > 5: # 19
                return True
        return False  # only 1 number

    def checkFinished(self, text):
        if self.finished(text):
            self.moveFocus()

    def linePaste(self):
        text = self.dialog.clipboard.text().replace(' ', '').replace('\n', '')

        bytes_ = text.split('.')
        if not all(IPLineEdit.reg_ex.exactMatch(i.strip()) for i in bytes_):  # if it is not exactly ip,
            # try to get something
            match = IPLineEdit.ip_regex.search(text)
            if match:
                bytes_ = match.group(0)
            else:
                return
        for extra_idx, byt in enumerate(bytes_):
            if self.index + extra_idx > 3:
                break
            self.lines[self.index + extra_idx].setText(byt)
        self.moveFocus()

    def keyPressEvent(self, e):
        if e.type() == QtCore.QEvent.KeyPress:
            key = e.key()
            modifiers = e.modifiers()
            if modifiers & QtCore.Qt.ControlModifier:
                key += QtCore.Qt.CTRL
            if key == QtCore.Qt.Key_V + QtCore.Qt.CTRL:
                self.paste.emit()
        super(IPLineEdit, self).keyPressEvent(e)

    @classmethod
    def getIP(cls):
        string = ''
        for line in cls.lines:
            string += f"{line.text().lstrip('0') or '0'}."
        string = string[:-1]
        return string

    @classmethod
    def reset(cls, dialog):
        cls.lines.clear()
        cls.dialog = dialog

    @classmethod
    def setTabOrder_(cls, parent):
        parent.setTabOrder(cls.lines[0], cls.lines[1])
        parent.setTabOrder(cls.lines[1], cls.lines[2])
        parent.setTabOrder(cls.lines[2], cls.lines[3])

    @classmethod
    def moveFocus(cls):
        for line in cls.lines:
            if not line.reg_ex.exactMatch(line.text()):
                line.setFocus()
                break
        else:  # everything match
            cls.dialog.buttonBox.buttons()[0].click()


class IPDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(IPDialog, self).__init__(parent)
        self.clipboard = QtWidgets.QApplication.instance().clipboard()
        self.setObjectName("Dialog")
        self.resize(200, 108)
        self.setMinimumSize(QtCore.QSize(200, 0))
        self.setFocusPolicy(QtCore.Qt.TabFocus)
        self.setSizeGripEnabled(False)
        self.setModal(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.frame_2 = QtWidgets.QFrame(self)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setDirection(QtWidgets.QBoxLayout.LeftToRight)
        self.verticalLayout.addWidget(self.frame_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.buttonBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.lines = IpLines(self)

    def getIP(self):
        return self.lines.getIP()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_4.setText(_translate("Dialog", "Insert Server IPv4 Address:"))


def getIP(parent=None):
    dialog = IPDialog(parent)
    val = dialog.exec_()
    return dialog.getIP(), val


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    print(getIP())
