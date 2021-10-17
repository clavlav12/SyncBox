from ChatDialog.chat import Ui_Dialog
from PyQt5 import QtCore, QtWidgets

"""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
</style></head><body style=" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;">  
"""


class ChatDialog(Ui_Dialog, QtWidgets.QDialog):
    send_message = QtCore.pyqtSignal(str, str)  # receiver, message

    def __init__(self, parent=None):
        super(ChatDialog, self).__init__(parent)
        self.setupUi(self)
        # self.setGeometry(pos.x(), pos.y(), 200, 400)
        self.last_sender = None
        self.last_receiver = None
        self.comboBox.setView(QtWidgets.QListView())
        self.comboBox.setStyleSheet(self.comboBox.styleSheet() + '\n' + "QListView::item {height:30px;}")
        self.comboBox.setCurrentIndex(0)
        self.lineEdit.setFocus()
        self.lineEdit.returnPressed.connect(self.sendMessage)
        self.comboBox.textActivated.connect(self.textChosen)

    def connect(self, player):
        self.client = player.client
        player.message_received.connect(self.messageReceived)
        player.users_updated.connect(self.users_updated)

    def sendMessage(self):
        msg = self.lineEdit.text()
        if not msg:  # empty line edit
            return
        self.comboBox.setCurrentIndex(self.comboBox.currentIndex())
        receiver = self.comboBox.currentText()
        self.textBrowser.insertHtml(self.createMessage('Me', receiver, msg))
        self.lineEdit.clear()
        self.send_message.emit(receiver, msg)

    def textChosen(self):
        self.lineEdit.setFocus()

    def users_updated(self, users):
        users = list(users.keys())
        index = self.comboBox.currentIndex()
        self.comboBox.setCurrentIndex(index)
        current_text = self.comboBox.currentText()
        users.sort()
        self.comboBox.clear()
        self.comboBox.addItem('Everyone')
        for user in users:
            if user != self.client.username:
                self.comboBox.addItem(user)
        index = self.comboBox.findText(current_text)
        if index == -1:
            index = 0
        self.comboBox.setCurrentIndex(index)

    def messageReceived(self, message, sender, receiver):
        self.textBrowser.insertHtml(self.createMessage(sender, receiver, message))

    def createMessage(self, sender, receiver, message):
        if sender == "Me":
            if receiver == 'Everyone':
                name = '''
                <span style=" font-size:8pt; color:#737374;">From</span>
                <span style=" font-size:8pt; color:#737374;">{}</span>
                <span style=" font-size:8pt; color:#737374;">to</span>
                 <span style=" font-size:8pt;"> </span><span style=" font-size:8pt; color:#0496fe;">{}</span><span 
                 style=" font-size:8pt; color:#9b9b9b;">:</span><span style=" font-size:8pt;"><br></span>'''.\
                    format(sender, receiver)
            else:
                name = '''
                <span style=" font-size:8pt; color:#737374;">From</span>
                <span style=" font-size:8pt; color:#737374;">{}</span>
                <span style=" font-size:8pt; color:#737374;">to</span>
                 <span style=" font-size:8pt;"> </span><span style=" font-size:8pt; color:#0496fe;">{}</span><span 
                 style=" font-size:8pt; color:#9b9b9b;">:</span><span style=" font-size:8pt;"></span><span 
                 style=" font-size:8pt; color:#CD5C5C;"> (private)</span><span style=" font-size:8pt;"><br></span>'''. \
                    format(sender, receiver)
            msg = '''<span style=" font-size:8pt; color:#000000;">{}</span>
            <span style=" font-size:8pt;"><br></span>'''.format(message)
        else:
            if receiver == 'Everyone':
                name = '''
                    <span style=" font-size:8pt; color:#737374;">From </span>
                    <span style=" font-size:8pt; color:#0496fe;">{}</span>
                    <span style=" font-size:8pt; color:#737374;"> to</span><span style=" font-size:8pt;"> </span>
                    <span style=" font-size:8pt; color:#0496fe;">{}</span>
                    <span style=" font-size:8pt; color:#737374;">:</span><span style=" 
                    font-size:8pt; color:#9b9b9b;"><br></span><span style=" font-size:8pt;">'''.\
                    format(sender, receiver)
            else:
                name = '''
                    <span style=" font-size:8pt; color:#737374;">From </span>
                    <span style=" font-size:8pt; color:#0496fe;">{}</span>
                    <span style=" font-size:8pt; color:#737374;"> to</span><span style=" font-size:8pt;"> </span>
                    <span style=" font-size:8pt; color:#0496fe;">Me</span>
                    <span style=" font-size:8pt; color:#737374;">:</span>
                    <span style=" font-size:8pt; color:#CD5C5C;"> (private)</span><span style=" 
                    font-size:8pt; color:#9b9b9b;"><br></span><span style=" font-size:8pt;">'''.\
                    format(sender, receiver)

            msg = '''<span style=" font-size:8pt; color:#000000;">
                {}<br></span>
                '''.format(message)

        if (sender != self.last_sender) or (receiver != self.last_receiver):  # new sender
            string = name + msg
            if self.last_sender is not None:  # just to skip the first time
                string = '<br>' + string
        else:
            string = msg
        self.last_sender = sender
        self.last_receiver = receiver
        return string


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = ChatDialog(None)
    Dialog.show()
    sys.exit(app.exec_())
