# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'titleWidget.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class PanelTitle(QtWidgets.QWidget):
    def __init__(self, parent=None, title=''):
        super(PanelTitle, self).__init__(parent)
        self.setupUi(self, title)

    def setupUi(self, Form, title):
        Form.setObjectName("Form")
        Form.resize(167, 38)
        Form.setStyleSheet("background-color: white;")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setMinimumSize(QtCore.QSize(20, 20))
        self.comboBox.setMaximumSize(QtCore.QSize(17, 20))
        self.comboBox.setStyleSheet("QComboBox {\n"
                                    "    border: none;\n"
                                    "    border-radius: 5px;\n"
                                    "    padding: 3px 3px 3px 8px;\n"
                                    "    background: transparent;\n"
                                    "    font-size: large;\n"
                                    "    margin-right: 3px;\n"
                                    "}\n"
                                    "QComboBox:hover {\n"
                                    "    background-color: rgb(240, 240, 240);\n"
                                    "    color: rgb(5, 96, 150);\n"
                                    "}\n"
                                    "\n"
                                    "QComboBox:pressed {\n"
                                    "    background-color: rgb(221, 221, 221);\n"
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
                                    "        width: 80;\n"
                                    "    }\n"
                                    "QComboBox QAbstractItemView {\n"
                                    "        min-width: 80;\n"
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
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Icons/Images/icons image/x.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.comboBox.addItem(icon, "")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Icons/Images/icons image/popout.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.comboBox.addItem(icon1, "")
        self.horizontalLayout.addWidget(self.comboBox)
        self.label = QtWidgets.QLabel(Form)
        self.label.setMaximumSize(QtCore.QSize(140, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.label.setStyleSheet("background-color: transparent;"
                                 "border: none;\n"
                                 "\n"
                                 "")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # self.setStyleSheet('''
        #     border-top: 2px solid lightgray;
        #     border-bottom: none;
        # ''')

        self.comboBox.setView(QtWidgets.QListView())
        self.comboBox.setStyleSheet(self.comboBox.styleSheet() + '\n' + "QListView::item {height:30px;}")
        self.comboBox.setCurrentIndex(0)

        self.label.setText(title)

    def changeParticipantsNumber(self, n):
        self.label.setText(f"Participants ({n})")

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.comboBox.setItemText(0, _translate("Form", "Close"))
        self.comboBox.setItemText(1, _translate("Form", "Pop out"))

    def paintEvent(self, pe):
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        p = QtGui.QPainter(self)
        s = self.style()
        s.drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, p, self)


class Participant(QtWidgets.QWidget):
    myNameStyleSheet = 'font: bold 12px; color: green'
    otherNameStyleSheet = 'font: bold 12px; color: blue'

    def __init__(self, name, accepted, parent=None, myName=False):
        super(Participant, self).__init__(parent)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.horizontalLayout)
        self.acceptedLabel = QtWidgets.QLabel(self)
        self.nameLabel = QtWidgets.QLabel(self)

        self.horizontalLayout.setAlignment(QtCore.Qt.AlignLeft)
        self.horizontalLayout.addWidget(self.acceptedLabel)
        self.horizontalLayout.addWidget(self.nameLabel)
        self.nameLabel.setAlignment(QtCore.Qt.AlignVCenter)

        if myName:
            self.nameLabel.setStyleSheet(self.myNameStyleSheet)
        else:
            self.nameLabel.setStyleSheet(self.otherNameStyleSheet)

        self.x = QtGui.QPixmap(r":/Icons/Images/icons image/redx.png")
        self.v = QtGui.QPixmap(r":/Icons/Images/icons image/greenV.png")
        self.clapperboard = QtGui.QPixmap(r":/Icons/Images/icons image/Clapperboard.png"). \
            scaled(16, 16, transformMode=QtCore.Qt.SmoothTransformation)

        self.nameLabel.setText(name)
        self.acceptedLabel.setScaledContents(False)
        self.acceptedLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.setAcceptedIcon(accepted)

    def setAcceptedIcon(self, accepted):
        if accepted:
            self.acceptedLabel.setPixmap(self.v)
        else:
            self.acceptedLabel.setPixmap(self.x)

    def setFinishIcon(self):
        self.acceptedLabel.setPixmap(self.clapperboard)


class ParticipantsPanel(QtWidgets.QDockWidget):
    def __init__(self, parent):
        super(ParticipantsPanel, self).__init__(parent)
        self.wasShown = False
        self.started = False
        self.specialDockTitleBar = PanelTitle(self, 'Participants (1)')

        self.specialDockTitleBar.comboBox.textActivated.connect(self.changeParticipantPanelMode)
        self.setWindowTitle(self.specialDockTitleBar.label.text())
        self.DockDefaultTitleBar = self.titleBarWidget()
        self.setTitleBarWidget(self.specialDockTitleBar)
        self.topLevelChanged.connect(self.ParticipantPanelModeChanged)

        self.hide()
        self.setStyleSheet('QDockWidget{background: white;}')

        self.parent().name_changed.connect(self.name_changed)
        self.participants = []
        self.layoutCreated = False
        parent.users_updated.connect(self.users_updated)
        parent.video_started_signal.connect(self.video_started)

    def name_changed(self, name):
        first = True
        for widget in self.participants:
            label = widget.nameLabel
            if label.text() == name:
                if not first:  # own name is not first, need to change order
                    self.verticalLayout.removeWidget(widget)
                    self.verticalLayout.insertWidget(0, widget)
                label.setStyleSheet(Participant.myNameStyleSheet)
                break

            first = False

        if not first:  # re order participants
            self.participants.remove(widget)
            self.participants.insert(0, widget)

    def video_started(self):
        self.started = True
        for widget in self.participants:
            widget.setFinishIcon()

    def users_updated(self, users):  # {name: accepted}
        self.setWindowTitle(f'Participants ({len(users)})')
        self.specialDockTitleBar.changeParticipantsNumber(len(users))

        if not self.layoutCreated:
            self.createLayout()

        self.clearLayout()
        self.participants.clear()

        myName = self.parent().getName()

        # first add own label, then add others alphabetically

        if myName is not None:
            participant = Participant(myName, users[myName], self, True)
            self.verticalLayout.addWidget(participant)
            self.participants.append(participant)
            users.pop(myName)
        for user in users:
            participant = Participant(user, users[user], self, False)
            self.verticalLayout.addWidget(participant)
            self.participants.append(participant)

        if self.started:
            self.video_started()

    def createLayout(self):
        self.verticalLayout = self.parent().ParticipantsLayout
        self.verticalLayout.setAlignment(QtCore.Qt.AlignTop)
        self.layoutCreated = True

    def clearLayout(self):
        while self.verticalLayout.count():
            child = self.verticalLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.hide()
        self.setFloating(False)

    def changeParticipantPanelMode(self, mode):
        command = mode.lower()
        if command == 'pop out':
            self.setFloating(True)
        elif command == 'close':
            self.hide()
        elif command == 'open':
            self.show()

    def ParticipantPanelModeChanged(self, floating):
        if floating:
            self.setTitleBarWidget(self.DockDefaultTitleBar)
        else:
            self.setTitleBarWidget(self.specialDockTitleBar)

    def updateWasShown(self):
        self.wasShown = not self.isHidden()

    def toggleShow(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()
