from PySide2.QtCore import QObject, Slot
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resources.appTexts as txt

FILE_EXTENSION = ".opf"
FILE_OPEN = "OSCAR files (*" + FILE_EXTENSION + ")"


class WelcomeCtrl(QObject):
    """controller for welcome view"""
    def __init__(self):
        super(WelcomeCtrl, self).__init__()

    @Slot(QDialog)
    def close_app(self, dialog):
        dialog.reject()

    @Slot(QDialog)
    def create_project(self, ui_dialog):
        self.dialog = QFileDialog(ui_dialog._ui.frame_create,
                                  txt.CREATE_PROJECT['sub'])
        self.dialog.setAcceptMode(QFileDialog.AcceptSave)
        self.dialog.accepted.connect(
            lambda: self.close_dialog(True, ui_dialog))
        self.dialog.open()

    @Slot(QDialog)
    def open_project(self, ui_dialog):
        self.dialog = QFileDialog(ui_dialog._ui.frame_open,
                                  txt.OPEN_PROJECT['sub'])
        self.dialog.setAcceptMode(QFileDialog.AcceptOpen)
        self.dialog.setNameFilter(FILE_OPEN)
        self.dialog.accepted.connect(
            lambda: self.close_dialog(False, ui_dialog))
        self.dialog.open()

    def close_dialog(self, new_project, dialog):
        self._filename = self.dialog.selectedFiles()[0]
        self._filename = self._filename.split(FILE_EXTENSION)[0]
        self._filename = self._filename + FILE_EXTENSION
        self._new_project = new_project
        dialog.accept()

    @property
    def new_project(self):
        return self._new_project

    @property
    def filename(self):
        return self._filename
