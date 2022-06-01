from PySide2.QtWidgets import *
from PySide2.QtCore import *


class ProjectButton(QWidget):
    """define functionality of project button
    for welcomeScreen"""
    clicked = Signal()

    def __init__(self, parent):
        super(ProjectButton, self).__init__(parent)

    # emit clicked signal if mouse press on project button
    def mousePressEvent(self, event):
        self.clicked.emit()
