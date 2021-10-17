from PyQt5 import QtGui, QtCore, QtWidgets
import shortcut_dialog
import warnings
import json
import os


def multiple_keys_shortcut(window, method, *args):
    action = QtWidgets.QAction(window)
    action.setShortcuts(args)
    action.triggered.connect(method)
    window.addAction(action)
    return action


class KeySequenceRecorder(QtWidgets.QLineEdit):
    updated = QtCore.pyqtSignal(QtGui.QKeySequence)

    modToString = {QtCore.Qt.Key_Control: "Ctrl", QtCore.Qt.Key_Shift: "Shift",
                   QtCore.Qt.Key_Alt: "Alt", QtCore.Qt.Key_Meta: "Meta"}

    def __init__(self, keySequence, *args):
        super(KeySequenceRecorder, self).__init__(*args)
        self.keySequence = keySequence
        self.setKeySequence(keySequence)
        self.home(False)
        self.setReadOnly(True)

    def setKeySequence(self, keySequence):
        self.keySequence = keySequence
        self.setText(self.keySequence.toString(QtGui.QKeySequence.NativeText))

    def clearText(self):
        self.keySequence = QtGui.QKeySequence('')
        self.setText('')

    def keyPressEvent(self, e):
        if e.type() == QtCore.QEvent.KeyPress:
            key = e.key()

            if key == QtCore.Qt.Key_unknown:
                warnings.warn("Unknown key from a macro probably")
                return

            # the user have clicked just and only the special keys Ctrl, Shift, Alt, Meta.
            if (key == QtCore.Qt.Key_Control or
                    key == QtCore.Qt.Key_Shift or
                    key == QtCore.Qt.Key_Alt or
                    key == QtCore.Qt.Key_Meta):
                return

            # check for a combination of user clicks
            modifiers = e.modifiers()
            keyText = e.text()
            # if the keyText is empty than it's a special key like F1, F5, ...

            if modifiers & QtCore.Qt.ShiftModifier:
                key += QtCore.Qt.SHIFT
            if modifiers & QtCore.Qt.ControlModifier:
                key += QtCore.Qt.CTRL
            if modifiers & QtCore.Qt.AltModifier:
                key += QtCore.Qt.ALT
            if modifiers & QtCore.Qt.MetaModifier:
                key += QtCore.Qt.META

            self.setKeySequence(QtGui.QKeySequence(key))
            self.clearFocus()
            self.updated.emit(self.keySequence)


class Action:
    actions_list = []

    def __init__(self, action):
        self.action = action
        self.text = self.getText(action)
        self.shortcut = action.shortcut()
        Action.actions_list.append(self)

    @staticmethod
    def getText(action):
        if action.toolTip():
            return action.toolTip()
        elif action.statusTip():
            return action.statusTip()
        elif action.objectName():
            return action.objectName()

    @classmethod
    def saveJson(cls):
        action_dict = cls.getWindowJson()
        if not os.path.isdir('data'):
            os.makedirs('data')
        with open('data/shortcuts.json', 'w') as json_file:
            json.dump(action_dict, json_file, indent=4)

    @classmethod
    def getWindowJson(cls):
        return {action.text: {'enabled': action.action.isEnabled(), 'shortcut': action.shortcut.toString()} for action
                in cls.actions_list}

    @classmethod
    def loadJson(cls, actions, settings=None):
        action_dict = settings
        if settings is None:
            try:
                with open('data/shortcuts.json', 'r') as json_file:
                    action_dict = json.load(json_file)
            except FileNotFoundError:
                return False
        for tip in action_dict:
            for action in actions:
                if tip == cls.getText(action):
                    if action_dict[tip]['shortcut']:  # has a shortcut
                        cls.removeActionShortcut(actions, action_dict[tip])
                        action.setShortcut(action_dict[tip]['shortcut'])
                    action.setDisabled(not action_dict[tip]['enabled'])
        return True

    @staticmethod
    def removeActionShortcut(action_list, shortcut):
        for action in action_list:
            if action.shortcut() == shortcut:
                action.setShortcut(QtGui.QKeySequence(''))

    @staticmethod
    def getFilteredWindowActions(window):
        return list(filter(lambda action: action.toolTip() or action.statusTip() or action.objectName(),
                           set(window.findChildren(QtWidgets.QAction)) - set(window.menuBar().actions())))

    @classmethod
    def loadActions(cls, window):
        for action in sorted(cls.getFilteredWindowActions(window), key=lambda ac: cls.getText(ac).lower()):
            cls(action)

    @classmethod
    def clearData(cls):
        cls.actions_list.clear()


class VisualAction(Action):
    actions_list = []
    tableWidget = None
    parent = None
    lineEditStyleSheet = '''
                                QLineEdit
                                {
                                    background-color:transparent;
                                }
                                QLineEdit:hover
                                 {
                                    background-color: rgb(224, 232, 246);
                                }
                                QLineEdit:focus
                                {
                                    background-color: rgba(193, 210, 238, 200);
                                    border: 1px solid rgb(60, 127, 177)
                                }
                                '''

    @classmethod
    def init(cls, table, parent):
        cls.tableWidget = table
        cls.parent = parent

    def __init__(self, action, row_number):
        super(VisualAction, self).__init__(action)
        self.checkBox = QtWidgets.QCheckBox()
        self.checkBox.setChecked(action.isEnabled())
        self.checkBox.stateChanged.connect(action.setEnabled)
        widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QGridLayout(widget)
        self.layout.addWidget(self.checkBox)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        rowPosition = self.tableWidget.rowCount()
        if row_number == rowPosition:
            self.tableWidget.insertRow(rowPosition)
        self.tableWidget.setCellWidget(row_number, 0, widget)
        self.lineEdit = KeySequenceRecorder(action.shortcut(), self.parent)
        self.lineEdit.setStyleSheet(self.lineEditStyleSheet)
        self.tableWidget.setCellWidget(row_number, 1, self.lineEdit)
        self.lineEdit.updated.connect(self.setShortcut)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(row_number, item)
        item.setText(self.text)
        VisualAction.actions_list.append(self)

    def setShortcut(self, shortcut):
        action = None
        try:
            for action in self.actions_list:
                if action.shortcut == shortcut and self is not action:
                    raise ValueError('Shortcut is already in use by "{}"\n'.format(action.text))
            else:  # the shortcut is free
                self.lineEdit.setStyleSheet(self.lineEditStyleSheet)
                self.action.setShortcut(shortcut)
                self.shortcut = shortcut
        except ValueError as e:
            self.lineEdit.clearText()
            reply = QtWidgets.QMessageBox.question(self.parent, "Shortcut in use", str(e) + "What would you like to do?"
                                                   , QtWidgets.QMessageBox.Retry |
                                                   QtWidgets.QMessageBox.Ignore |
                                                   QtWidgets.QMessageBox.Cancel
                                               )

            if reply == QtWidgets.QMessageBox.Retry:
                self.tableWidget.parent().activateWindow()
                self.lineEdit.setFocus()
                self.lineEdit.setStyleSheet('''
                                        QLineEdit
                                        {
                                            background-color:transparent;
                                        }
                                        QLineEdit:hover
                                         {
                                            background-color: rgb(224, 232, 246);
                                        }
                                        QLineEdit:focus
                                        {
                                            background-color: rgba(255, 8, 8, 50);
                                            border: 1px solid rgba(255, 8, 8, 200);
                                        }
                                        ''')
            elif reply == QtWidgets.QMessageBox.Cancel:
                self.lineEdit.clearFocus()
            else:  # Ignore - solve the collision
                action.action.setShortcut('')
                action.shortcut = QtGui.QKeySequence('')
                action.lineEdit.setKeySequence(QtGui.QKeySequence(''))

                self.lineEdit.setStyleSheet(self.lineEditStyleSheet)
                self.lineEdit.setKeySequence(shortcut)
                self.action.setShortcut(shortcut)
                self.shortcut = shortcut

    @classmethod
    def loadActions(cls, window):
        for idx, action in enumerate(sorted(cls.getFilteredWindowActions(window),
                                            key=lambda ac: cls.getText(ac).lower())):
            cls(action, idx)

    @classmethod
    def clearData(cls):
        cls.actions_list.clear()
        cls.tableWidget = None
        cls.parent = None


class MainDialog(QtWidgets.QDialog, shortcut_dialog.Ui_Dialog):
    def __init__(self, parent, restoreDefaultShortcuts):
        super(MainDialog, self).__init__(parent)
        self.setupUi(self)
        self.resize(400, 400)
        Action.clearData()
        Action.loadActions(parent)
        self.beforeChanges = Action.getWindowJson()
        Action.clearData()

        self.tableWidget.setContentsMargins(0, 0, 0, 0)
        self.parentActions = VisualAction.getFilteredWindowActions(parent)
        VisualAction.init(self.tableWidget, self)
        VisualAction.loadActions(parent)

        btn = QtWidgets.QPushButton("Restore To default", self)
        btn.clicked.connect(lambda: restoreDefaultShortcuts(self.tableWidget))
        self.layout().addWidget(btn)

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        header = self.tableWidget.verticalHeader()
        header.setDefaultSectionSize(32)

    def closeEvent(self, QCloseEvent):
        self.safeClose()
        super(MainDialog, self).closeEvent(QCloseEvent)

    def safeClose(self):
        if self.beforeChanges == VisualAction.getWindowJson():
            return
        reply = QtWidgets.QMessageBox.question(self, "Save Changes?", "Would you like to save your changes?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            VisualAction.saveJson()
        else:
            Action.loadJson(Action.getFilteredWindowActions(self.parent()), self.beforeChanges)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.safeClose()
        else:
            super(MainDialog, self).keyPressEvent(event)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication([sys.argv])
    dialog = KeySequenceRecorder(QtGui.QKeySequence('A'))
    dialog.show()
    app.exec_()
