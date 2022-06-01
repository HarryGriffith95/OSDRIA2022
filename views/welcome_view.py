from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

from views.welcome_view_ui import Ui_Dialog


class WelcomeView(QDialog):
    """Creation of the Welcome Screen
    includes interaction for creating new file
    as well as opening existing file
    """
    def __init__(self, welcome_controller):
        settings = Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        super().__init__(None, settings)

        self._welcome_controller = welcome_controller
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._ui = Ui_Dialog()
        self._ui.setupUi(self)

        # connect widgets to controller
        self._ui.button_close.clicked.connect(
            lambda: self._welcome_controller.close_app(self))
        self._ui.frame_create.clicked.connect(
            lambda: self._welcome_controller.create_project(self))
        self._ui.frame_open.clicked.connect(
            lambda: self._welcome_controller.open_project(self))

    def mousePressEvent(self, event):
        if event.button() is Qt.LeftButton:
            self.relative_cursor_position = self.pos() - event.globalPos()
            self.left_click = True

    def mouseReleaseEvent(self, event):
        if event.button() is Qt.LeftButton:
            self.left_click = False

    def mouseMoveEvent(self, event):
        """move dialog with mouse clicked move"""
        if self.leftClick:
            self.move(event.globalPos() + self.relative_cursor_position)
