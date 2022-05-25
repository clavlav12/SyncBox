# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import Icons_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(844, 623)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Icons/Images/icons image/player.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        MainWindow.setWindowIcon(icon)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setStyleSheet("QMenuBar {\n"
"    /* background-color: rgb(15, 15, 15) ; */\n"
"\n"
"}\n"
"QMenuBar::item {\n"
"    /* background-color: rgb(15, 15, 15) ; */\n"
"    /*background-color: rgb(207, 207, 207); */\n"
"    /* color: rgb(207, 207, 207) */\n"
"    color: rgb(15,15,15)\n"
"}\n"
"QMainWindow#MainWindow{\n"
"    /* background-color: rgb(15, 15, 15) ; \n"
"        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                  stop: 0     rgb(170, 200, 255), \n"
"                  stop: 1  rgb(229, 243, 255)\n"
"            )\n"
"    */\n"
"    background-color:  rgb(170, 200, 255);\n"
"} \n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.mainMenuPage = QtWidgets.QWidget()
        self.mainMenuPage.setObjectName("mainMenuPage")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.mainMenuPage)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.mainMenuFrame = QtWidgets.QFrame(self.mainMenuPage)
        self.mainMenuFrame.setStyleSheet("color: rgb(15, 15, 15)")
        self.mainMenuFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mainMenuFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mainMenuFrame.setObjectName("mainMenuFrame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.mainMenuFrame)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setHorizontalSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.menuButtonsFrame = QtWidgets.QFrame(self.mainMenuFrame)
        self.menuButtonsFrame.setMaximumSize(QtCore.QSize(300, 200))
        self.menuButtonsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.menuButtonsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.menuButtonsFrame.setObjectName("menuButtonsFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.menuButtonsFrame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.browseRoomButton = QtWidgets.QPushButton(self.menuButtonsFrame)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.browseRoomButton.setFont(font)
        self.browseRoomButton.setStyleSheet("QPushButton {\n"
"    border: 2px solid #8f8f91;\n"
"    border-radius: 6px;\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 rgb(250, 205, 59), stop: 1 rgb(255, 200, 150));\n"
"    min-width: 80px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 rgb(250, 205, 150), stop: 1 rgb(250, 205, 59));\n"
"}\n"
"\n"
"QPushButton:flat {\n"
"    border: none; /* no border for a flat push button */\n"
"}\n"
"\n"
"QPushButton:default {\n"
"    border-color: navy; /* make the default button prominent */\n"
"}\n"
"")
        self.browseRoomButton.setCheckable(False)
        self.browseRoomButton.setAutoDefault(False)
        self.browseRoomButton.setDefault(False)
        self.browseRoomButton.setFlat(False)
        self.browseRoomButton.setObjectName("browseRoomButton")
        self.verticalLayout.addWidget(self.browseRoomButton)
        self.createRoomButton = QtWidgets.QPushButton(self.menuButtonsFrame)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.createRoomButton.setFont(font)
        self.createRoomButton.setStyleSheet("QPushButton {\n"
"    border: 2px solid #8f8f91;\n"
"    border-radius: 6px;\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 rgb(250, 205, 59), stop: 1 rgb(250, 205, 150));\n"
"    min-width: 80px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 rgb(250, 205, 150), stop: 1 rgb(250, 205, 59));\n"
"}\n"
"\n"
"QPushButton:flat {\n"
"    border: none; /* no border for a flat push button */\n"
"}\n"
"\n"
"QPushButton:default {\n"
"    border-color: navy; /* make the default button prominent */\n"
"}\n"
"")
        self.createRoomButton.setCheckable(False)
        self.createRoomButton.setAutoDefault(False)
        self.createRoomButton.setDefault(False)
        self.createRoomButton.setFlat(False)
        self.createRoomButton.setObjectName("createRoomButton")
        self.verticalLayout.addWidget(self.createRoomButton)
        self.usernameInput = QtWidgets.QLineEdit(self.menuButtonsFrame)
        self.usernameInput.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.usernameInput.setFont(font)
        self.usernameInput.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.usernameInput.setStyleSheet("/* QLineEdit {\n"
"    border: 2px solid rgb(122, 122, 122);\n"
"    border-radius: 10px;\n"
"    background: transparent;\n"
"    selection-background-color: green;\n"
"    padding: 0 8px;\n"
"     color: blue; \n"
"    color: rgb(20, 6, 43);\n"
"    font-weight: bold\n"
"}\n"
"QLineEdit:focus{\n"
"    border: 2px solid rgb(0, 120, 215);\n"
"}  */\n"
"\n"
"QLineEdit {\n"
"    border-style: solid;\n"
"                                /* top | right | bottom | left */\n"
"    border-color:   transparent transparent rgb(0, 120, 215) transparent;\n"
"    border-width: 2px;\n"
"    background: transparent;\n"
"    selection-background-color: green;\n"
"    padding: 0 2px -13px 2px;\n"
"    color: green;\n"
"    font-weight: bold\n"
"}\n"
"QLineEdit:focus{\n"
"    border-color:  transparent transparent green transparent;\n"
"}\n"
"QLineEdit[text=\"\"]{  /* place holder text */\n"
"    color: blue\n"
"}\n"
"\n"
"\n"
"")
        self.usernameInput.setInputMask("")
        self.usernameInput.setText("")
        self.usernameInput.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.usernameInput.setObjectName("usernameInput")
        self.verticalLayout.addWidget(self.usernameInput)
        self.gridLayout_3.addWidget(self.menuButtonsFrame, 3, 1, 1, 1)
        self.localImageLabel = QtWidgets.QLabel(self.mainMenuFrame)
        self.localImageLabel.setText("")
        self.localImageLabel.setPixmap(QtGui.QPixmap(":/Icons/Images/icons image/localUpload.png"))
        self.localImageLabel.setScaledContents(False)
        self.localImageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.localImageLabel.setObjectName("localImageLabel")
        self.gridLayout_3.addWidget(self.localImageLabel, 0, 2, 1, 1)
        self.localInfoLabel = QtWidgets.QLabel(self.mainMenuFrame)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        self.localInfoLabel.setFont(font)
        self.localInfoLabel.setTextFormat(QtCore.Qt.RichText)
        self.localInfoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.localInfoLabel.setWordWrap(True)
        self.localInfoLabel.setObjectName("localInfoLabel")
        self.gridLayout_3.addWidget(self.localInfoLabel, 2, 2, 1, 1)
        self.chatInfoLabel = QtWidgets.QLabel(self.mainMenuFrame)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        self.chatInfoLabel.setFont(font)
        self.chatInfoLabel.setTextFormat(QtCore.Qt.RichText)
        self.chatInfoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.chatInfoLabel.setWordWrap(True)
        self.chatInfoLabel.setObjectName("chatInfoLabel")
        self.gridLayout_3.addWidget(self.chatInfoLabel, 2, 0, 1, 1)
        self.syncInfoLabel = QtWidgets.QLabel(self.mainMenuFrame)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        self.syncInfoLabel.setFont(font)
        self.syncInfoLabel.setTextFormat(QtCore.Qt.RichText)
        self.syncInfoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.syncInfoLabel.setWordWrap(True)
        self.syncInfoLabel.setObjectName("syncInfoLabel")
        self.gridLayout_3.addWidget(self.syncInfoLabel, 2, 1, 1, 1)
        self.syncImageLabel = QtWidgets.QLabel(self.mainMenuFrame)
        self.syncImageLabel.setText("")
        self.syncImageLabel.setPixmap(QtGui.QPixmap(":/Icons/Images/icons image/sync.png"))
        self.syncImageLabel.setScaledContents(False)
        self.syncImageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.syncImageLabel.setObjectName("syncImageLabel")
        self.gridLayout_3.addWidget(self.syncImageLabel, 0, 1, 1, 1)
        self.syncTopicLabel = QtWidgets.QLabel(self.mainMenuFrame)
        self.syncTopicLabel.setMinimumSize(QtCore.QSize(0, 0))
        self.syncTopicLabel.setMaximumSize(QtCore.QSize(16777215, 32))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        self.syncTopicLabel.setFont(font)
        self.syncTopicLabel.setTextFormat(QtCore.Qt.RichText)
        self.syncTopicLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.syncTopicLabel.setObjectName("syncTopicLabel")
        self.gridLayout_3.addWidget(self.syncTopicLabel, 1, 1, 1, 1)
        self.localTopicLabel = QtWidgets.QLabel(self.mainMenuFrame)
        self.localTopicLabel.setMaximumSize(QtCore.QSize(16777215, 32))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        self.localTopicLabel.setFont(font)
        self.localTopicLabel.setTextFormat(QtCore.Qt.RichText)
        self.localTopicLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.localTopicLabel.setObjectName("localTopicLabel")
        self.gridLayout_3.addWidget(self.localTopicLabel, 1, 2, 1, 1)
        self.chatTopicLbael = QtWidgets.QLabel(self.mainMenuFrame)
        self.chatTopicLbael.setMaximumSize(QtCore.QSize(16777215, 32))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        self.chatTopicLbael.setFont(font)
        self.chatTopicLbael.setTextFormat(QtCore.Qt.RichText)
        self.chatTopicLbael.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.chatTopicLbael.setWordWrap(True)
        self.chatTopicLbael.setObjectName("chatTopicLbael")
        self.gridLayout_3.addWidget(self.chatTopicLbael, 1, 0, 1, 1)
        self.chatImageLabel = QtWidgets.QLabel(self.mainMenuFrame)
        self.chatImageLabel.setText("")
        self.chatImageLabel.setPixmap(QtGui.QPixmap(":/Icons/Images/icons image/Chat.png"))
        self.chatImageLabel.setScaledContents(False)
        self.chatImageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.chatImageLabel.setObjectName("chatImageLabel")
        self.gridLayout_3.addWidget(self.chatImageLabel, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.mainMenuFrame, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.mainMenuPage)
        self.playerPage = QtWidgets.QWidget()
        self.playerPage.setObjectName("playerPage")
        self.gridLayout = QtWidgets.QGridLayout(self.playerPage)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.mainFrame = QtWidgets.QFrame(self.playerPage)
        self.mainFrame.setStyleSheet("QFrame#mainFrame{\n"
"    background-color: white;\n"
"    /*background-color: rgb(15, 15, 15);*/\n"
"}\n"
"\n"
"")
        self.mainFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.mainFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mainFrame.setObjectName("mainFrame")
        self.playerMainBackground = QtWidgets.QVBoxLayout(self.mainFrame)
        self.playerMainBackground.setSpacing(0)
        self.playerMainBackground.setObjectName("playerMainBackground")
        self.screenFrame = QtWidgets.QFrame(self.mainFrame)
        self.screenFrame.setStyleSheet("background-color: rgb(40, 40, 40)")
        self.screenFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.screenFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.screenFrame.setObjectName("screenFrame")
        self.screenLayout = QtWidgets.QGridLayout(self.screenFrame)
        self.screenLayout.setContentsMargins(0, 0, 0, 0)
        self.screenLayout.setHorizontalSpacing(0)
        self.screenLayout.setObjectName("screenLayout")
        self.playerMainBackground.addWidget(self.screenFrame)
        self.slidersFrame = QtWidgets.QFrame(self.mainFrame)
        self.slidersFrame.setEnabled(True)
        self.slidersFrame.setMinimumSize(QtCore.QSize(0, 40))
        self.slidersFrame.setMaximumSize(QtCore.QSize(16777215, 40))
        self.slidersFrame.setStyleSheet("")
        self.slidersFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.slidersFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slidersFrame.setObjectName("slidersFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.slidersFrame)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.passedTimeLabel = QtWidgets.QLabel(self.slidersFrame)
        self.passedTimeLabel.setMinimumSize(QtCore.QSize(50, 0))
        self.passedTimeLabel.setStyleSheet("background-color: transparent;\n"
"color:black")
        self.passedTimeLabel.setObjectName("passedTimeLabel")
        self.horizontalLayout.addWidget(self.passedTimeLabel)
        self.seekSlider = JumpSlider(self.slidersFrame)
        self.seekSlider.setEnabled(False)
        self.seekSlider.setStyleSheet("QSlider::groove:horizontal { \n"
"    background: transparent;\n"
"    background-color: #333333;\n"
"    height: 5px; \n"
"}\n"
"QSlider::handle:horizontal { \n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0.965909, x2:0, y2:0, stop:0\n"
"     rgba(90, 220, 255, 255), stop:0.4\n"
"     rgba(1, 66, 145, 255), stop:0.5 \n"
"     rgba(1, 66, 145, 255), stop:1 \n"
"    rgba(189,199, 228, 255));\n"
"\n"
"    border: 1px solid rgba(64, 121 , 200, 100); \n"
"    width: 8px; \n"
"    height: 5x; \n"
"    line-height: 5px; \n"
"    margin-top: -3px; \n"
"    margin-bottom: -3px; \n"
"    border-radius: 5px; \n"
"}\n"
"QSlider::handle:horizontal:disabled { \n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.965909, x2:0, y2:0, stop:0 \n"
"rgba(122, 151, 203, 255), stop:0.482955\n"
"rgba(1, 43, 92, 255), stop:1 \n"
"rgba(122, 151, 203, 255)); \n"
"\n"
"    border: 1px solid rgba(50, 100 , 180, 150); \n"
"    width: 8px; \n"
"    height: 5x; \n"
"    line-height: 5px; \n"
"    margin-top: -3px; \n"
"    margin-bottom: -3px; \n"
"    border-radius: 5px; \n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0.965909, x2:0, y2:0, stop:0\n"
"     rgba(128, 230, 255, 255), stop:0.5\n"
"     rgba(1, 66, 145, 255), stop:0.5 \n"
"     rgba(1, 66, 145, 255), stop:1 \n"
"    rgba(209,217, 237, 255));\n"
"\n"
"}\n"
"\n"
"QSlider::handle:horizontal:pressed {\n"
"    border: 1px inset rgba(64, 121 , 200, 100); \n"
"}\n"
"\n"
"QSlider::add-page:Horizontal {\n"
"background-color:rgb(222, 232, 243);\n"
"border: 1px solid rgb(191, 197, 207);\n"
" }\n"
"QSlider::sub-page:Horizontal {\n"
" background-color: qlineargradient(spread:pad, x1:0, y1:0.965909, x2:0, y2:0, stop:0 rgba(187, 201, 228, 255), stop:0.482955 rgba(1, 66, 145, 255), stop:1 rgba(187, 201, 228, 255)); }")
        self.seekSlider.setProperty("value", 0)
        self.seekSlider.setSliderPosition(0)
        self.seekSlider.setTracking(True)
        self.seekSlider.setOrientation(QtCore.Qt.Horizontal)
        self.seekSlider.setObjectName("seekSlider")
        self.horizontalLayout.addWidget(self.seekSlider)
        self.videoLenghtLabel = QtWidgets.QLabel(self.slidersFrame)
        self.videoLenghtLabel.setMinimumSize(QtCore.QSize(50, 0))
        self.videoLenghtLabel.setStyleSheet("background-color: transparent;\n"
"color:black")
        self.videoLenghtLabel.setObjectName("videoLenghtLabel")
        self.horizontalLayout.addWidget(self.videoLenghtLabel)
        self.playerMainBackground.addWidget(self.slidersFrame)
        self.buttonsFrame = QtWidgets.QFrame(self.mainFrame)
        self.buttonsFrame.setMaximumSize(QtCore.QSize(16777215, 50))
        self.buttonsFrame.setStyleSheet("QPushButton{\n"
"    padding-left: 3px;\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.965909, x2:0, y2:0,     stop:0 \n"
"\n"
"    rgba(90, 220, 255, 255), stop:0.3\n"
"    rgba(1, 66, 145, 255), stop:0.5\n"
"    rgba(1, 66, 145, 255), stop:1     \n"
"    rgba(189,199, 228, 255));\n"
"\n"
"\n"
"    border: 2px outset  rgb(102,149, 187);\n"
"    border-radius: 17px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    border: 2px inset  rgb(102,149, 187);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.965909, x2:0, y2:0,     stop:0 \n"
"\n"
"    rgba(128, 230, 255, 225), stop:0.35\n"
"    rgba(1, 66, 145, 240), stop:0.5     \n"
"    rgba(1, 66, 145, 240), stop:1     \n"
"    rgba(189,199, 228, 200));\n"
"}\n"
"\n"
"\n"
"")
        self.buttonsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.buttonsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.buttonsFrame.setObjectName("buttonsFrame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.buttonsFrame)
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.playButton = QtWidgets.QPushButton(self.buttonsFrame)
        self.playButton.setEnabled(True)
        self.playButton.setMinimumSize(QtCore.QSize(35, 35))
        self.playButton.setMaximumSize(QtCore.QSize(35, 35))
        self.playButton.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.playButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.playButton.setStyleSheet("QPushButton{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.965909, x2:0, y2:0,     stop:0 \n"
"\n"
"    rgba(90, 220, 255, 255), stop:0.35\n"
"    rgba(1, 66, 145, 255), stop:0.5\n"
"    rgba(1, 66, 145, 255), stop:1     \n"
"    rgba(189,199, 228, 255));\n"
"\n"
"    border: 2px outset  rgb(102,149, 187);\n"
"    border-radius: 17px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    border: 2px inset  rgb(102,149, 187);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.965909, x2:0, y2:0,     stop:0 \n"
"\n"
"    rgba(128, 230, 255, 225), stop:0.35\n"
"    rgba(1, 66, 145, 240), stop:0.5     \n"
"    rgba(1, 66, 145, 240), stop:1     \n"
"    rgba(189,199, 228, 200));\n"
"}\n"
"\n"
"\n"
"")
        self.playButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Icons/Images/icons image/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playButton.setIcon(icon1)
        self.playButton.setIconSize(QtCore.QSize(20, 20))
        self.playButton.setCheckable(False)
        self.playButton.setAutoDefault(True)
        self.playButton.setDefault(False)
        self.playButton.setFlat(True)
        self.playButton.setObjectName("playButton")
        self.horizontalLayout_4.addWidget(self.playButton, 0, QtCore.Qt.AlignVCenter)
        spacerItem = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.fastBackwardButton = QtWidgets.QPushButton(self.buttonsFrame)
        self.fastBackwardButton.setEnabled(True)
        self.fastBackwardButton.setMinimumSize(QtCore.QSize(30, 30))
        self.fastBackwardButton.setMaximumSize(QtCore.QSize(30, 30))
        self.fastBackwardButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Icons/Images/icons image/fast backward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fastBackwardButton.setIcon(icon2)
        self.fastBackwardButton.setAutoRepeat(False)
        self.fastBackwardButton.setAutoExclusive(False)
        self.fastBackwardButton.setAutoDefault(False)
        self.fastBackwardButton.setDefault(False)
        self.fastBackwardButton.setFlat(False)
        self.fastBackwardButton.setObjectName("fastBackwardButton")
        self.horizontalLayout_4.addWidget(self.fastBackwardButton)
        self.stopButton = QtWidgets.QPushButton(self.buttonsFrame)
        self.stopButton.setEnabled(True)
        self.stopButton.setMinimumSize(QtCore.QSize(30, 30))
        self.stopButton.setMaximumSize(QtCore.QSize(30, 30))
        self.stopButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/Icons/Images/icons image/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stopButton.setIcon(icon3)
        self.stopButton.setAutoRepeat(False)
        self.stopButton.setAutoExclusive(False)
        self.stopButton.setAutoDefault(False)
        self.stopButton.setDefault(False)
        self.stopButton.setFlat(False)
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout_4.addWidget(self.stopButton)
        self.fastForwardButton = QtWidgets.QPushButton(self.buttonsFrame)
        self.fastForwardButton.setEnabled(True)
        self.fastForwardButton.setMinimumSize(QtCore.QSize(30, 30))
        self.fastForwardButton.setMaximumSize(QtCore.QSize(30, 30))
        self.fastForwardButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/Icons/Images/icons image/fast forward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fastForwardButton.setIcon(icon4)
        self.fastForwardButton.setAutoRepeat(False)
        self.fastForwardButton.setAutoExclusive(False)
        self.fastForwardButton.setAutoDefault(False)
        self.fastForwardButton.setDefault(False)
        self.fastForwardButton.setFlat(False)
        self.fastForwardButton.setObjectName("fastForwardButton")
        self.horizontalLayout_4.addWidget(self.fastForwardButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.openParticipantsButton = QtWidgets.QPushButton(self.buttonsFrame)
        self.openParticipantsButton.setMinimumSize(QtCore.QSize(30, 30))
        self.openParticipantsButton.setMaximumSize(QtCore.QSize(30, 30))
        self.openParticipantsButton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/Icons/Images/icons image/white participants.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openParticipantsButton.setIcon(icon5)
        self.openParticipantsButton.setObjectName("openParticipantsButton")
        self.horizontalLayout_4.addWidget(self.openParticipantsButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.volumeLabel = QtWidgets.QLabel(self.buttonsFrame)
        self.volumeLabel.setEnabled(False)
        self.volumeLabel.setMaximumSize(QtCore.QSize(30, 16777215))
        self.volumeLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.volumeLabel.setStyleSheet("  padding-right: 1px;\n"
"  padding-left: 10px;\n"
"")
        self.volumeLabel.setText("")
        self.volumeLabel.setPixmap(QtGui.QPixmap(":/Icons/Images/icons image/volume mini.png"))
        self.volumeLabel.setObjectName("volumeLabel")
        self.horizontalLayout_4.addWidget(self.volumeLabel)
        self.volumeSlider = JumpSlider(self.buttonsFrame)
        self.volumeSlider.setEnabled(False)
        self.volumeSlider.setMaximumSize(QtCore.QSize(150, 16777215))
        self.volumeSlider.setStyleSheet("QSlider::groove:horizontal { \n"
"    background: transparent;\n"
"    background-color: #333333;\n"
"    height: 5px; \n"
"}\n"
"QSlider::handle:horizontal { \n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0.965909, x2:0, y2:0, stop:0\n"
"     rgba(90, 220, 255, 255), stop:0.4\n"
"     rgba(1, 66, 145, 255), stop:0.5 \n"
"     rgba(1, 66, 145, 255), stop:1 \n"
"    rgba(189,199, 228, 255));\n"
"\n"
"    border: 1px solid rgba(64, 121 , 200, 100); \n"
"    width: 8px; \n"
"    height: 5x; \n"
"    line-height: 5px; \n"
"    margin-top: -3px; \n"
"    margin-bottom: -3px; \n"
"    border-radius: 5px; \n"
"}\n"
"QSlider::handle:horizontal:disabled { \n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.965909, x2:0, y2:0, stop:0 \n"
"rgba(122, 151, 203, 255), stop:0.482955\n"
"rgba(1, 43, 92, 255), stop:1 \n"
"rgba(122, 151, 203, 255)); \n"
"\n"
"    border: 1px solid rgba(50, 100 , 180, 150); \n"
"    width: 8px; \n"
"    height: 5x; \n"
"    line-height: 5px; \n"
"    margin-top: -3px; \n"
"    margin-bottom: -3px; \n"
"    border-radius: 5px; \n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0.965909, x2:0, y2:0, stop:0\n"
"     rgba(128, 230, 255, 255), stop:0.5\n"
"     rgba(1, 66, 145, 255), stop:0.5 \n"
"     rgba(1, 66, 145, 255), stop:1 \n"
"    rgba(209,217, 237, 255));\n"
"\n"
"}\n"
"\n"
"QSlider::handle:horizontal:pressed {\n"
"    border: 1px inset rgba(64, 121 , 200, 100); \n"
"}\n"
"\n"
"QSlider::add-page:Horizontal {\n"
"background-color:rgb(222, 232, 243);\n"
"border: 1px solid rgb(191, 197, 207);\n"
" }\n"
"QSlider::sub-page:Horizontal {\n"
" background-color: qlineargradient(spread:pad, x1:0, y1:0.965909, x2:0, y2:0, stop:0 rgba(187, 201, 228, 255), stop:0.482955 rgba(1, 66, 145, 255), stop:1 rgba(187, 201, 228, 255)); }")
        self.volumeSlider.setMaximum(400)
        self.volumeSlider.setProperty("value", 100)
        self.volumeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.volumeSlider.setObjectName("volumeSlider")
        self.horizontalLayout_4.addWidget(self.volumeSlider)
        self.playerMainBackground.addWidget(self.buttonsFrame)
        self.gridLayout.addWidget(self.mainFrame, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.playerPage)
        self.horizontalLayout_3.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 844, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuOnline = QtWidgets.QMenu(self.menubar)
        self.menuOnline.setObjectName("menuOnline")
        MainWindow.setMenuBar(self.menubar)
        self.participantsPanel = ParticipantsPanel(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        self.participantsPanel.setFont(font)
        self.participantsPanel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.participantsPanel.setObjectName("participantsPanel")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.ParticipantsLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.ParticipantsLayout.setContentsMargins(0, 0, 0, 0)
        self.ParticipantsLayout.setObjectName("ParticipantsLayout")
        self.participantsPanel.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.participantsPanel)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionShortcutEditor = QtWidgets.QAction(MainWindow)
        self.actionShortcutEditor.setObjectName("actionShortcutEditor")
        self.actionJoin_Group = QtWidgets.QAction(MainWindow)
        self.actionJoin_Group.setObjectName("actionJoin_Group")
        self.actionCreate_Group = QtWidgets.QAction(MainWindow)
        self.actionCreate_Group.setObjectName("actionCreate_Group")
        self.actionStart_Video = QtWidgets.QAction(MainWindow)
        self.actionStart_Video.setObjectName("actionStart_Video")
        self.actionSet_Ip = QtWidgets.QAction(MainWindow)
        self.actionSet_Ip.setObjectName("actionSet_Ip")
        self.actionIs_Connected = QtWidgets.QAction(MainWindow)
        self.actionIs_Connected.setObjectName("actionIs_Connected")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionShortcutEditor)
        self.menuOnline.addAction(self.actionSet_Ip)
        self.menuOnline.addAction(self.actionIs_Connected)
        self.menuOnline.addSeparator()
        self.menuOnline.addAction(self.actionJoin_Group)
        self.menuOnline.addAction(self.actionCreate_Group)
        self.menuOnline.addAction(self.actionStart_Video)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuOnline.menuAction())

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Video Player"))
        self.browseRoomButton.setText(_translate("MainWindow", "Browse Room"))
        self.createRoomButton.setText(_translate("MainWindow", "Create Room"))
        self.usernameInput.setPlaceholderText(_translate("MainWindow", "Username"))
        self.localInfoLabel.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">No more hours wasted on                                 uploading! </span></p><p><span style=\" font-size:12pt; font-weight:600;\">Use Videos from your local drives!</span></p></body></html>"))
        self.chatInfoLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Chat with your friends while watching to see their reaction!</span></p></body></html>"))
        self.syncInfoLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">No more 3... 2... 1...! Automatically synchronize between you and your friends.</span></p><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Watch videos with your friends online for free!</span></p></body></html>"))
        self.syncTopicLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">Auto Sync</span></p></body></html>"))
        self.localTopicLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">Use Local Videos</span></p></body></html>"))
        self.chatTopicLbael.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">Chat While Watching</span></p></body></html>"))
        self.passedTimeLabel.setText(_translate("MainWindow", "00:00:00"))
        self.videoLenghtLabel.setText(_translate("MainWindow", "00:00:00"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuOnline.setTitle(_translate("MainWindow", "Online"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setToolTip(_translate("MainWindow", "Open File"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setToolTip(_translate("MainWindow", "Exit App"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.actionShortcutEditor.setText(_translate("MainWindow", "Shortcuts Editor"))
        self.actionShortcutEditor.setToolTip(_translate("MainWindow", "Shortcuts Editor"))
        self.actionShortcutEditor.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionJoin_Group.setText(_translate("MainWindow", "Join Group"))
        self.actionCreate_Group.setText(_translate("MainWindow", "Create Group"))
        self.actionStart_Video.setText(_translate("MainWindow", "Start Video"))
        self.actionSet_Ip.setText(_translate("MainWindow", "Set Server Ip"))
        self.actionIs_Connected.setText(_translate("MainWindow", "Am I Conncted?"))
from widgets.ParticipantsPanel import ParticipantsPanel
from widgets.jump_slider import JumpSlider

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
