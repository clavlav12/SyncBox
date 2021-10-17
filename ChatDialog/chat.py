# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chat.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(320, 294)
        Dialog.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setMinimumSize(QtCore.QSize(0, 40))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame.setStyleSheet("background: white;\n"
"border-top: 2px solid rgb(201, 203, 208);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setMaximumSize(QtCore.QSize(20, 16777215))
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("border:none;\n"
"background: Transparent")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = ExtendedComboBox(self.frame)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 0))
        self.comboBox.setMaximumSize(QtCore.QSize(75, 16777215))
        self.comboBox.setStyleSheet("QComboBox {\n"
"    border: none;\n"
"    border-radius: 5px;\n"
"    padding: 3px 3px 3px 8px;\n"
"    background: rgb(242, 242, 247);\n"
"    font-size: large\n"
"}\n"
"QComboBox:hover {\n"
"    background-color: rgb(231, 241, 253);\n"
"    color: rgb(5, 96, 150);\n"
"}\n"
"\n"
"\n"
"QComboBox::drop-down:button{\n"
"    background: transparent;\n"
"    border: none;\n"
"    padding-top: 7px;\n"
"    padding-right: 3px;\n"
"    image: url(:/Icons/Images/icons image/10X10 Dropdown.png);\n"
"}\n"
"\n"
"QListView {\n"
"        width: 200;\n"
"    }\n"
"QComboBox QAbstractItemView {\n"
"        min-width: 200;\n"
"}\n"
"QScrollBar:vertical {\n"
"  width: 5px;\n"
"  background: #f1f1f1;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"  background: #888;\n"
"  border-radius: 2px;\n"
"}\n"
"QScrollBar::add-line:vertical {\n"
"  border: 2px solid gray;\n"
"  background: #f1f1f1;\n"
"}\n"
"\n"
"QScrollBar::handle:hover:vertical {\n"
"  background: #555;\n"
"}\n"
"\n"
"\n"
"")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.widget = QtWidgets.QWidget(self.frame)
        self.widget.setStyleSheet("background: transparent;\n"
"border: none")
        self.widget.setObjectName("widget")
        self.horizontalLayout.addWidget(self.widget)
        self.toolButton = QtWidgets.QToolButton(self.frame)
        self.toolButton.setStyleSheet("    border: 1px solid rgb(229, 229, 238);\n"
"    border-radius: 5px;\n"
"    padding: 3px 3px 3px 3px;\n"
"    background: transparent\n"
"")
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout.addWidget(self.toolButton)
        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 50))
        self.lineEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit.setStyleSheet("/*border-top: 2px solid rgb(235, 238, 244)*/\n"
"border: none;\n"
"padding-top: -35px;\n"
"padding-left: 10px;")
        self.lineEdit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit.setDragEnabled(True)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 3, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setStyleSheet("QScrollBar:vertical {\n"
"  width: 5px;\n"
"  background: #f1f1f1;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"  background: #888;\n"
"  border-radius: 2px;\n"
"}\n"
"QScrollBar::add-line:vertical {\n"
"  border: 2px solid gray;\n"
"  background: #f1f1f1;\n"
"}\n"
"\n"
"QScrollBar::handle:hover:vertical {\n"
"  background: #555;\n"
"}\n"
"\n"
"QTextBrowser{\n"
"    border: none;\n"
"}")
        self.textBrowser.setOpenExternalLinks(False)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Chat"))
        self.label.setText(_translate("Dialog", "To:"))
        self.comboBox.setItemText(0, _translate("Dialog", "Everyone"))
        self.toolButton.setText(_translate("Dialog", "..."))
        self.lineEdit.setPlaceholderText(_translate("Dialog", "Type message here..."))
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p></body></html>"))
from widgets.extendedcombobox import ExtendedComboBox

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
