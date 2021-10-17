#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtWidgets import QCompleter, QComboBox, QStyledItemDelegate


class ExtendedComboBox(QComboBox):
    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

        # add a filter model to filter matching items
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.pFilterModel, self)
        self.mCompleterItemDelegate = QStyledItemDelegate(self)

        self.completer.popup().setItemDelegate(self.mCompleterItemDelegate)
        self.completer.popup().setStyleSheet(
            """
            QLineEdit {
                border: 2px solid gray;
                border-radius: 15px;
                padding: 6px;
                selection-background-color: darkgray;
                min-width: 10em;
                font: 20px;
                outline: 0px;
            }            
            """ +
            "QAbstractItemView {"
            "    min-width: 200px;"
            "}\n"
            "QAbstractItemView::item {"
            "    min-height: 30px;"
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

        )
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)

    # on selection of an item from the completer, select the corresponding item from combobox
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
            self.activated[str].emit(self.itemText(index))

    # on model change, update the models of the filter and completer as well
    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)
        self.completer.popup().setItemDelegate(self.mCompleterItemDelegate)

    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QStringListModel

    app = QApplication(sys.argv)

    string_list = ['hola muchachos', 'adios amigos', 'hello world', 'good bye']

    combo = ExtendedComboBox()

    # either fill the standard model of the combobox
    combo.addItems(string_list)

    # or use another model
    #combo.setModel(QStringListModel(string_list))

    combo.resize(300, 40)
    combo.show()

    sys.exit(app.exec_())
