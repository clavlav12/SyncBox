from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
import sys
import design
import os
import time
from editShortCutDialog import MainDialog as ShortcutEditor
from editShortCutDialog import Action as ActionHolder
from editShortCutDialog import VisualAction as visualActionHolder
import voliumAndTimeWidget
import socket
import select
from ChatDialog.ChatDialog import ChatDialog
import json
from widgets.IpDialog.getIP import getIP
from pymaybe import maybe
DESKTOP_PATH = os.path.normpath(os.path.expanduser("~/Desktop"))


def create_shortcut(window, method, tooltip, *keys):
    action = QtWidgets.QAction(window)
    action.setShortcuts(keys)
    action.triggered.connect(method)
    action.setToolTip(tooltip)
    window.addAction(action)
    return action


def memory_position(string):
    return str(string).split(' ')[-1]


class SettingLoadFailed(Exception):
    pass


class VideoPlayer(design.Ui_MainWindow, QtWidgets.QMainWindow):
    SLIDE_BAR_TIME = 1  # in sec
    VOLUME_SHORTCUT_CHANGE = 4  # in percentages
    TIME_SHORTCUT_CHANGE = 5  # in sec
    HIDE_MOUSE_DELAY = 2  # in sec - how much time until cursor disappear in fullscreen mode
    createGroupSignal = QtCore.pyqtSignal(str)
    joinGroupSignal = QtCore.pyqtSignal(str, str)
    voted = QtCore.pyqtSignal(bool)
    startVoteRequest = QtCore.pyqtSignal()
    pause_video_request = QtCore.pyqtSignal()
    play_video_request = QtCore.pyqtSignal()
    stop_video_request = QtCore.pyqtSignal()
    seek_request_signal = QtCore.pyqtSignal(int)
    disconnect_signal = QtCore.pyqtSignal()
    video_loaded_signal = QtCore.pyqtSignal()
    message_received = QtCore.pyqtSignal(str, str, str)  # message, sender, receiver
    users_updated = QtCore.pyqtSignal(dict)
    name_changed = QtCore.pyqtSignal(str)
    video_started_signal = QtCore.pyqtSignal()
    TIME_BETWEEN_SEEKS = 0

    def __init__(self):
        super(VideoPlayer, self).__init__()
        self.setupUi(self)
        self.releaseSliderTimer = None
        self.setCentralWidget(self.stackedWidget)
        self.clipboard = QtWidgets.QApplication.instance().clipboard()
        self.connected = None
        self.statusBar().hide()
        self.toggleFullscreenAction = create_shortcut(self, self.toggleFullScreen, 'Toggle Fullscreen',
                                                      'Ctrl+F', 'F11')
        self.debugAction = create_shortcut(self, self.returnToMainMenu, 'Debug', 'Ctrl+W')
        self.exitFullscreenAction = create_shortcut(self, self.exitFullscreen, 'Exit Fullscreen', 'Esc')
        self.pauseMenu = create_shortcut(self, self.request_toggle, 'Pause/Play Media', 'Space')
        self.actionExit.triggered.connect(self.safeQuit)
        self.actionOpen.triggered.connect(self.loadVideo)
        self.actionShortcutEditor.triggered.connect(self.openShortcutEditor)
        self.increaseAudio = create_shortcut(self,
                                             lambda: self.setVolume(self.volumeSlider.value()
                                                                    + self.VOLUME_SHORTCUT_CHANGE),
                                             "Volume Increase", 'UP')

        self.decreaseAudio = create_shortcut(self,
                                             lambda: self.setVolume(self.volumeSlider.value() -
                                                                    self.VOLUME_SHORTCUT_CHANGE),
                                             "Volume Decrease", 'Down')

        self.sync = create_shortcut(self, self.syncGroup, 'Sync Group', 'Ctrl+J')

        self.seekForwardAudio = create_shortcut(self, lambda: self.request_seek(
            self.mediaPlayer.position() + self.TIME_SHORTCUT_CHANGE * 1000), "Play Forward", 'Right')
        self.seekBackwardAudio = create_shortcut(self, lambda: self.request_seek(
            self.mediaPlayer.position() - self.TIME_SHORTCUT_CHANGE * 1000), "Play Backward", 'Left')

        self.fastForwardButton.clicked.connect(self.seekForwardAudio.trigger)
        self.fastBackwardButton.clicked.connect(self.seekBackwardAudio.trigger)

        ActionHolder.loadActions(self)
        self.defaultSettings = ActionHolder.getWindowJson()
        ActionHolder.loadJson(ActionHolder.getFilteredWindowActions(self))
        ActionHolder.clearData()
        self.client = None
        self.chatDialog = ChatDialog(self)
        self.createPlayerWindow()
        self.createMainMenuWindow()
        self.enterMainMenuWindow()
        self.chatDialog.connect(self)
        self.toggleFullscreenAction = create_shortcut(self, self.chatDialog.show, 'Open Chat',
                                                      'Ctrl+H')
        # self.enterPlayerWindow()
        self.playIcon = QtGui.QIcon()
        self.playIcon.addPixmap(QtGui.QPixmap(":/Icons/Images/icons image/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.pauseIcon = QtGui.QIcon()
        self.pauseIcon.addPixmap(QtGui.QPixmap(":/Icons/Images/icons image/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.videoStarted = False
        self.openParticipantsButton.clicked.connect(self.participantsPanel.toggleShow)
        #

    def connectToServer(self):
        ip = maybe(self.loadSetting('ip')).or_else('127.0.0.1')
        self.client = Client(self, ip)
        self.client.group_created.connect(lambda code: self.newGroup(True, code))
        self.client.joined_group.connect(lambda code: self.newGroup(False, code))
        self.client.creation_failed_signal.connect(self.creationFailed)
        self.client.group_not_found_signal.connect(self.GroupNotFound)
        self.client.start_video_vote_start.connect(self.askVote)
        self.client.start_video_vote_failed.connect(self.startFailed)
        self.client.start_video_vote_succeeded.connect(lambda: self.play(True))
        self.client.pause_video.connect(self.pause)
        self.client.play_video.connect(self.play)
        self.client.stop_video.connect(self.stop)
        self.client.seek_to.connect(self.seek)
        self.client.connected_signal.connect(self.serverConnected)
        self.client.message_received.connect(self.message_received.emit)
        self.client.users_updated.connect(self.uui)
        self.client.name_changed.connect(self.name_changed.emit)
        self.client.start()

    def uui(self, *args):
        print("users Update")
        self.users_updated.emit(*args)

    def serverConnected(self, ip):
        self.connected = ip

    def createMainMenuWindow(self):
        self.usernameInput.textChanged.connect(lambda: self.usernameInput.setStyleSheet(self.usernameInput.styleSheet()))
        noSpaces = QtCore.QRegExp(r'^[^<>\s&%$]*$')
        # noSpaces = QtCore.QRegExp(r'^(?!.*(Everyone|\s)).*$', QtCore.Qt.CaseInsensitive)
        noSpacesValidator = QtGui.QRegExpValidator(noSpaces, self.usernameInput)
        self.usernameInput.setValidator(noSpacesValidator)
        self.usernameInput.setMaxLength(22)
        self.createRoomButton.clicked.connect(self.createGroup)
        self.browseRoomButton.clicked.connect(self.joinGroup)

    def enterMainMenuWindow(self):
        self.exitFullscreen()
        txt = maybe(self.loadSetting('username')).or_else('')
        self.usernameInput.setText(txt)
        self.stackedWidget.setCurrentIndex(0)
        self.setStyleSheet(self.styleSheet() + 'QMainWindow{background-color:  rgb(170, 200, 255);}')
        if self.client is None:  # first time, need to connect...
            self.connectToServer()

    def mediaStateChanged(self, state):
        pass

    def getName(self):
        return self.client.username

    def createPlayerWindow(self):
        self.mediaPlayer = QMediaPlayer(self, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()
        self.screenLayout.addWidget(self.videoWidget)
        self.mediaPlayer.setVideoOutput(self.videoWidget)

        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.timeUpdate)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        self.mediaPlayer.videoAvailableChanged.connect(self.videoAvailableChanged)

        self.mediaPath = None
        self.media = None
        self.showSliderTimer = None
        self.showCursorTimer = None
        self.fullScreen = False
        self.actionJoin_Group.triggered.connect(self.joinGroup)
        self.actionCreate_Group.triggered.connect(self.createGroup)
        self.actionStart_Video.triggered.connect(lambda:
                                                 self.startVoteRequest.emit() if self.mediaLoaded else print("not loaded, ", self.mediaPlayer.mediaStatus()))

        self.actionSet_Ip.triggered.connect(self.changeIp)
        self.actionIs_Connected.triggered.connect(self.displayConnection)

        self.timeVolumePopup = voliumAndTimeWidget.TimeVolumeDisplay(self)
        self.timeVolumePopup.move(20, 20)
        self.timeVolumePopup.show()

        self.releaseSliderTimer = None

        # self.mainFrame.setStyleSheet('QFrame#mainFrame{background: rgba(255,255, 255, 255);}')
        # self.mainFrame.setStyleSheet('QFrame#mainFrame{background: rgba(255,255, 255, 255);}')

        self.videoLength = 0

        self.playButton.clicked.connect(self.playPauseClicked)
        # self.pauseButton.clicked.connect(self.pauseClicked)
        self.stopButton.clicked.connect(self.stopClicked)
        self.volumeSlider.valueChanged.connect(self.mediaPlayer.setVolume)
        self.volumeSlider.valueChanged.connect(lambda x: self.timeVolumePopup.setVolume(x // 4))

        self.last_time_requested = 0

    @property
    def mediaLoaded(self):
        return self.mediaPlayer.mediaStatus() == QMediaPlayer.LoadedMedia

    def playPauseClicked(self):
        if self.mediaPlayer.state() == 0:  # video have not started yet:
            self.actionStart_Video.trigger()
        else:
            self.request_toggle()

    def displayConnection(self):
        if self.connected is None:
            QtWidgets.QMessageBox.information(self, 'Not Connected To Server', 'You are not connected')
        else:
            QtWidgets.QMessageBox.information(self, 'Connected To Server', 'You are connected to ' + self.connected)

    def timeUpdate(self, position):
        # print(self.mediaPlayer.)
        if not self.seekSlider.hold():
            self.seekSlider.signalBLockedValueChange(position)
        if self.videoLength == 0:
            return
        self.timeVolumePopup.setTime(position, self.videoLength)
        self.passedTimeLabel.setText(self.timeVolumePopup.timeLable.text()[:8])  # without the %

    def handleError(self):
        print("Error: ", repr(self.mediaPlayer.errorString()))

    def enterPlayerWindow(self):
        self.playButton.setIcon(self.playIcon)
        name = self.usernameInput.text()
        self.setStyleSheet('QMainWindow{background-color: white}')
        self.changeSetting('username', name)
        self.stackedWidget.setCurrentIndex(1)

    def returnToMainMenu(self):
        self.mediaPlayer.stop()
        self.enterMainMenuWindow()

    def stopClicked(self):
        self.stop_video_request.emit()

    def pauseClicked(self):
        self.pause_video_request.emit()

    def playClicked(self):
        self.play_video_request.emit()

    def changeIp(self):
        ip, ok = getIP(self)
        if ok and ip:
            self.createSettingsFile()
            self.changeSetting('ip', ip)
            if self.client.connected:
                print("ip changed")
                self.client.disconnect_and_quit(True)
            Client.IP = ip
            self.connected = None
            self.connectToServer()

    def changeSetting(self, setting, value):
        try:
            with open('data/settings.json', 'r') as file:
                try:
                    data = json.load(file)
                except json.decoder.JSONDecodeError:
                    data = {}
            data[setting] = value
            with open('data/settings.json', 'w') as file:  # save IP
                json.dump(data, file, indent=4)
        except PermissionError:
            return False
        return True

    def loadSetting(self, setting):
        try:
            with open('data/settings.json', 'r') as file:
                data = json.load(file)
                return data[setting]
        except (FileNotFoundError, KeyError, PermissionError, json.decoder.JSONDecodeError):
            return None

    def getSettings(self, setting):
        pass

    @staticmethod
    def createSettingsFile():
        if not os.path.isdir('data'):
            os.makedirs('data')
        if not os.path.isfile('data/settings.json'):
            file = open('data/settings.json', 'w')
            file.close()

    def joinGroup(self):
        text, ok = QtWidgets.QInputDialog().getText(self, "QInputDialog().getText()",
                                                "Group Code:", QtWidgets.QLineEdit.Normal)
        if ok and text:
            self.joinGroupSignal.emit(text, self.usernameInput.text())

    def createGroup(self):
        self.createGroupSignal.emit(self.usernameInput.text())

    def askVote(self):
        if not self.mediaLoaded:
            self.voted.emit(False)
            return

        vote = QtWidgets.QMessageBox.question(self, "Start Video?",
                                          "Vote started.\nWould you like to start the video?",
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if vote == QtWidgets.QMessageBox.Yes:
            self.voted.emit(True)
        else:
            self.voted.emit(False)

    def startFailed(self):
        pass

    def newGroup(self, created, code):
        if created:
            QtWidgets.QMessageBox.information(self, 'Group Successfully Created', 'Group Successfully Created\n'
                                                                              'Your Group code is {}\n'
                                                                              'Group code copied to clipboard'.
                                          format(code))

            self.clipboard.setText(code)
        else:
            QtWidgets.QMessageBox.information(self, 'Successfully Joined Group', 'Successfully Joined Group\n'
                                                                             'Your Group code is {}\n'
                                                                             'Group code copied to clipboard'.
                                          format(code))

            self.clipboard.setText(code)
        self.enterPlayerWindow()

    def creationFailed(self):
        QtWidgets.QMessageBox.warning(self, 'Could Not Create Group', 'Creation failed for unknown reason')

    def GroupNotFound(self, code):
        QtWidgets.QMessageBox.warning(self, 'Could Not Join Group', 'Group with code {} could not be found'.format(code))

    def play(self, first_time=False):
        if first_time:
            print("First Time...")
            self.video_started_signal.emit()
            self.playButton.setEnabled(True)
            # self.pauseButton.setEnabled(True)
            self.stopButton.setEnabled(True)
            self.seekSlider.setEnabled(True)
            self.volumeSlider.setEnabled(True)
            # self.volumeImage.setEnabled(True)
        self.playButton.setStyleSheet('padding-left: 0px;')
        self.playButton.setIcon(self.pauseIcon)
        self.mediaPlayer.play()

    def pause(self):
        self.playButton.setStyleSheet('padding-left: 3px;')
        self.playButton.setIcon(self.playIcon)
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

    def stop(self):
        self.mediaPlayer.stop()
        self.playButton.setIcon(self.playIcon)

    def request_toggle(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.pause_video_request.emit()
        elif self.mediaPlayer.state() == QMediaPlayer.PausedState:
            self.play_video_request.emit()

    def restoreDefaultShortcuts(self, QTable):
        visualActionHolder.loadJson(ActionHolder.getFilteredWindowActions(self), self.defaultSettings)
        visualActionHolder.clearData()
        visualActionHolder.init(QTable, self)
        visualActionHolder.loadActions(self)
        visualActionHolder.saveJson()

    def mouseDoubleClickEvent(self, event):
        self.toggleFullScreen()

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton and self.fullScreen:
            self.showSliderBar()

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseMove:
            QtWidgets.QApplication.instance().restoreOverrideCursor()
            if self.fullScreen:
                self.showSliderBar()
                self.hideCursorIn(self.HIDE_MOUSE_DELAY)

        return QtWidgets.QMainWindow.eventFilter(self, source, event)

    def hideCursorIn(self, secs):
        if isinstance(self.showCursorTimer, QtCore.QTimer) and QtCore.QTimer.isActive(self.showCursorTimer):
            QtCore.QTimer.stop(self.showCursorTimer)
        self.showCursorTimer = QtCore.QTimer()
        self.showCursorTimer.setSingleShot(True)
        self.showCursorTimer.timeout.connect(
            lambda: QtWidgets.QApplication.instance().setOverrideCursor(QtCore.Qt.BlankCursor))
        self.showCursorTimer.start(secs * 1000)

    def showSliderBar(self, show_time=SLIDE_BAR_TIME):
        self.slidersFrame.show()
        if isinstance(self.showSliderTimer, QtCore.QTimer) and QtCore.QTimer.isActive(self.showSliderTimer):
            QtCore.QTimer.stop(self.showSliderTimer)

        self.showSliderTimer = QtCore.QTimer()
        self.showSliderTimer.setSingleShot(True)
        self.showSliderTimer.timeout.connect(self.hideSlidersFrame)
        self.showSliderTimer.start(show_time * 1000)

    def hideSlidersFrame(self):
        self.slidersFrame.hide()

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        super(VideoPlayer, self).mouseReleaseEvent(a0)

    def toggleFullScreen(self):
        if self.fullScreen:
            self.exitFullscreen()
        else:
            self.enterFullscreen()

    def exitFullscreen(self):
        if not self.fullScreen:
            return
        self.showNormal()
        if isinstance(self.showSliderTimer, QtCore.QTimer) and QtCore.QTimer.isActive(self.showSliderTimer):
            QtCore.QTimer.stop(self.showSliderTimer)
        self.buttonsFrame.show()
        self.slidersFrame.show()
        self.menubar.show()
        self.playerMainBackground.setContentsMargins(9, 9, 9, 9)
        self.fullScreen = False
        if self.participantsPanel.wasShown:
            self.participantsPanel.changeParticipantPanelMode('open')

    def enterFullscreen(self):
        if self.fullScreen or self.stackedWidget.currentIndex() != 1:  # main window
            return
        self.participantsPanel.updateWasShown()
        self.participantsPanel.changeParticipantPanelMode('close')
        self.showFullScreen()
        self.buttonsFrame.hide()
        self.slidersFrame.hide()
        self.menubar.hide()
        self.playerMainBackground.setContentsMargins(0, 0, 0, 0)
        self.fullScreen = True

    def openShortcutEditor(self):
        dialog = ShortcutEditor(self, self.restoreDefaultShortcuts)
        dialog.show()

    def loadVideo(self):
        self.mediaPath, _ = QtWidgets.QFileDialog= QtWidgets.QFileDialog.getOpenFileName(self, 'Choose a Video',
                                                                  self.loadSetting('init dir') or DESKTOP_PATH)

        if not self.mediaPath:
            return
        # self.mediaPlayer.play()
        self.mediaPlayer.setMedia(
            QMediaContent(QtCore.QUrl.fromLocalFile(self.mediaPath)))

        self.changeSetting('init dir', os.path.dirname(self.mediaPath))

    def videoAvailableChanged(self, available):
        if available:
            self.seekSlider.valueChanged.connect(self.request_seek)
            self.seekSlider.sliderReleased.connect(self.seekSliderRelease)
            self.seekSlider.sliderReleased.connect(lambda: self.updateTimeIn(300, self.seekSlider.value()))
            self.video_loaded_signal.emit()

    def durationChanged(self, videoLength):
        # Update seek scroller
        self.videoLength = videoLength
        self.seekSlider.setRange(0, self.videoLength)

        # update video length label
        self.videoLenghtLabel.setText(voliumAndTimeWidget.TimeVolumeDisplay.MStoDate(self.videoLength))

    def seekSliderRelease(self):
        return
        self.seekSlider.signalBLockedValueChange(self.seekValue)

    def updateTimeIn(self, delay, value):  # bug when releasing getting back to old position
        if isinstance(self.releaseSliderTimer, QtCore.QTimer) and QtCore.QTimer.isActive(self.releaseSliderTimer):
            QtCore.QTimer.stop(self.releaseSliderTimer)
        self.releaseSliderTimer = QtCore.QTimer()
        self.releaseSliderTimer.setSingleShot(True)
        self.releaseSliderTimer.timeout.connect(lambda: self.request_seek(delay + value))
        self.releaseSliderTimer.start(delay)

    def syncGroup(self):
        predict_time = int(1000 * 2/self.client.get_tick_rate)  # Predicted time until response from server
        self.request_seek(self.mediaPlayer.position() + predict_time)

    def setVolume(self, value):
        if not self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            return
        if self.fullScreen:
            self.timeVolumePopup.showVolume()
        self.volumeSlider.setValue(value)
        self.volumeSlider.setFocus()

    def seek(self, ms):
        if not self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            return
        if self.fullScreen:
            self.timeVolumePopup.showTime()
        if not ms == self.videoLength:
            self.mediaPlayer.blockSignals(True)
            self.mediaPlayer.setPosition(ms)
            self.mediaPlayer.blockSignals(False)

    def request_seek(self, ms):
        t = time.time()
        if (t - self.last_time_requested) > self.TIME_BETWEEN_SEEKS:
            self.seek_request_signal.emit(ms)
            self.last_time_requested = t
        # else:
        #     print("?")

    def closeEvent(self, *args, **kwargs):
        self.safeQuit()

    def safeQuit(self):
        if (self.client is not None) and self.connected:
            # print("safe quit")
            self.client.disconnect_and_quit(True)
        QtWidgets.QApplication.instance().quit()


class Client(QtCore.QThread):
    SERVER_PORT = 35241
    IP = "127.0.0.1"
    # IP = "31.44.141.250"
    group_created = QtCore.pyqtSignal(str)
    creation_failed_signal = QtCore.pyqtSignal()
    joined_group = QtCore.pyqtSignal(str)
    group_not_found_signal = QtCore.pyqtSignal(str)
    start_video_vote_start = QtCore.pyqtSignal()
    start_video_vote_failed = QtCore.pyqtSignal()
    start_video_vote_succeeded = QtCore.pyqtSignal()
    pause_video = QtCore.pyqtSignal()
    play_video = QtCore.pyqtSignal()
    stop_video = QtCore.pyqtSignal()
    seek_to = QtCore.pyqtSignal(int)
    connected_signal = QtCore.pyqtSignal(str)
    message_received = QtCore.pyqtSignal(str, str, str)  # message, sender, receiver
    users_updated = QtCore.pyqtSignal(dict)
    name_changed = QtCore.pyqtSignal(str)

    def __init__(self, player: VideoPlayer, defaultIP: str):
        super(Client, self).__init__(player)
        self.IP = defaultIP
        self.commands = {
            "created": self.created,
            "creation_failed": self.creation_failed,
            "joined": self.joined,
            "group_not_found": self.group_not_found,
            "start_video_vote_started": self.start_video_vote_started,
            "start_video_failed": self.start_video_failed,
            "start_video_succeeded": self.start_video_succeeded,
            "pause": self.pause,
            "play": self.play,
            "seek": self.seek,
            "stop": self.stop,
            "tick_rate": self.tick_rate,
            "users_list": self.users_list_update,
            "message_received": self.new_message_received,
            "late_start": self.late_start
        }
        self.socket = None
        self.get_tick_rate = None
        self.player = player
        self.connected = False
        self.username = None
        self.late = False
        self.last_seek_request = None  # sometimes seek request doesn't come in order. no need
        # to listen to late instructions

    def run(self):
        self.connected = self.connect_server()
        while self.connected:
            read_list = select.select([self.socket], [], [], 1)[0]
            if read_list:
                self.handle_request()
        # print("finished")
        self.socket.close()
        self.disconnect_and_quit(False)

    def connect_server(self):
        self.socket = socket.socket()
        self.socket.settimeout(10)
        try:
            ip = self.IP
            self.socket.connect((ip, self.SERVER_PORT))
        except (Exception, socket.timeout):
            return False
        else:
            self.connected_signal.emit(ip)
            self.player.createGroupSignal.connect(self.create_group)
            self.player.joinGroupSignal.connect(self.join_group)
            self.player.voted.connect(self.voted)
            self.player.startVoteRequest.connect(self.start_vote_request)
            self.player.play_video_request.connect(self.play_request)
            self.player.stop_video_request.connect(self.stop_request)
            self.player.pause_video_request.connect(self.pause_request)
            self.player.seek_request_signal.connect(self.seek_request)
            self.player.disconnect_signal.connect(self.disconnect_from_server)
            self.player.chatDialog.send_message.connect(self.send_message)
            self.player.video_loaded_signal.connect(self.video_loaded)
            self.socket.send(self.build_packet('get_tick_rate'))
            return True

    def disconnect_and_quit(self, server_open):
        if server_open:
            try:
                self.socket.send(self.build_packet('disconnect'))
            except:
                pass
        try:
            self.player.createGroupSignal.disconnect(self.create_group)
            self.player.joinGroupSignal.disconnect(self.join_group)
            self.player.voted.disconnect(self.voted)
            self.player.startVoteRequest.disconnect(self.start_vote_request)
            self.player.play_video_request.disconnect(self.play_request)
            self.player.stop_video_request.disconnect(self.stop_request)
            self.player.pause_video_request.disconnect(self.pause_request)
            self.player.seek_request_signal.disconnect(self.seek_request)
            self.player.disconnect_signal.disconnect(self.disconnect_from_server)
            self.player.video_loaded_signal.disconnect(self.video_loaded)
            # print("discconect called")
            self.connected = False
        except (TypeError, RuntimeError) as e:
            # methods are not connected. due to the asynchronic of the code this
            # method has been already called
            # print(repr(e))
            pass

    def handle_request(self):
        try:
            message = self.socket.recv(1024).decode()
            if not message:  # disconnected
                print("Empty message")
                self.disconnect_and_quit(False)
                return
            requests = self.smart_split(message, '\n')
            for request in requests:
                command, kwargs = self.split_message(request)
                self.commands[command](kwargs)
        except Exception as E:
            # warnings.warn("Something broken\n " + repr(E))
            raise E

    def create_group(self, name):
        self.socket.send(self.build_packet('create_group_requests', name=name))

    def join_group(self, code, name):
        self.socket.send(self.build_packet('join_group_request', group_code=code.strip(), name=name))

    def voted(self, should_start):
        if should_start:  # in favor of starting
            self.socket.send(self.build_packet('start_video_vote_accept'))
        else:  # against
            self.socket.send(self.build_packet('start_video_vote_deny'))

    def start_vote_request(self):
        self.socket.send(self.build_packet("start_video_request"))

    def play_request(self):
        self.socket.send(self.build_packet("play_request"))

    def pause_request(self):
        self.socket.send(self.build_packet("pause_request"))

    def stop_request(self):
        self.socket.send(self.build_packet("stop_request"))

    def seek_request(self, ms):
        print("requesting to seek to: ", ms)
        self.socket.send(self.build_packet('seek_request', time=ms))

    def disconnect_from_server(self):
        # print("asked to disconnect")
        self.disconnect_and_quit(True)

    def send_message(self, receiver, message):
        self.socket.send(self.build_packet('send_message', receiver=receiver, message=message))

    def video_loaded(self):
        if self.late:
            self.start_video_vote_succeeded.emit()
            self.socket.send(self.build_packet('get_state'))

    # commands:
    def created(self, kwargs):
        self.username = kwargs['username']
        self.name_changed.emit(self.username)
        self.group_created.emit(kwargs['group_code'])

    def creation_failed(self, kwargs):
        self.creation_failed_signal.emit()

    def joined(self, kwargs):
        self.username = kwargs['username']
        self.name_changed.emit(self.username)

        self.joined_group.emit(kwargs['group_code'])

    def group_not_found(self, kwargs):
        self.group_not_found_signal.emit(kwargs['group_code'])

    def start_video_vote_started(self, kwargs):
        self.start_video_vote_start.emit()

    def start_video_failed(self, kwargs):
        self.start_video_vote_failed.emit()

    def start_video_succeeded(self, kwargs):
        self.start_video_vote_succeeded.emit()

    def pause(self, kwargs):
        self.pause_video.emit()

    def play(self, kwargs):
        self.play_video.emit()

    def stop(self, kwargs):
        self.stop_video.emit()

    def seek(self, kwargs):
        print("seeking to: ", kwargs['time'])
        self.seek_to.emit(int(kwargs['time']))

    def tick_rate(self, kwargs):
        self.get_tick_rate = int(kwargs['rate'])

    def users_list_update(self, kwargs):
        self.users_updated.emit(json.loads(kwargs['users']))

    def new_message_received(self, kwargs):
        self.message_received.emit(kwargs['message'], kwargs['sender'], kwargs['receiver'])

    def late_start(self, kwargs):
        self.late = True
    # /commands

    @staticmethod
    def format_string(string):
        r"""Replaces %, & and = with \%, \& and \= respectively"""
        return str(string).replace('%', r'\%').replace('&', r'\&').replace('=', r'\=')

    @classmethod
    def build_packet(cls, command: str, **parameters):
        return cls.format_string(command).encode() + (b'?' if parameters else b'') + ('&'.join(
            ['{}={}'.format(cls.format_string(param), cls.format_string(val))
             for param, val in parameters.items()])).encode() + b'\n'

    @classmethod
    def split_message(cls, request: str):
        command, *arguments = cls.smart_split(request, '?')
        if arguments:
            a = [cls.smart_split(i, '=') for i in cls.smart_split(arguments[0], '&')]
            kwargs = dict(a)
        else:
            kwargs = {}
        return command, kwargs

    @staticmethod
    def smart_split(string, separator, saver='\\'):
        """Split string by the separator, as long as saver is not present before the separator.
        for example: string='Hello0Dear0W\0rld, separator='0', saver='\' returns ['Hello', 'Dear', 'W0rld']"""
        splited = string.split(separator)
        new_list = []
        i = 0
        while i < len(splited):
            item = splited[i]
            if item:
                if item[-1] == saver and not i+1 == len(splited):  # merge it with the next item
                    item = item[:-1]
                    item += separator + splited[i+1]
                    i += 1
                new_list.append(item)
            i += 1

        return new_list

    @staticmethod
    def encode_list(args):
        return ','.join(arg.replace(',', r'\,') for arg in args)

    @classmethod
    def decode_list(cls, lst):
        return cls.smart_split(lst, ',')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.focusChanged.connect(lambda old, new: print(new))
    vp = VideoPlayer()
    vp.show()
    app.installEventFilter(vp)
    sys.exit(app.exec_())
