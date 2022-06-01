from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

"""linkage between button states & modes and QIcon image type:
isEnabled | isChecked |     image type      | toggle colour | button colour
    0           0       not available, off      grey            grey
    0           1       available, on           white          white
    1           0       normal, off             orange
    1           1       normal, on              
"""


class ToolButton(QToolButton):
    """define functionality of tool button
    with hover effect"""

    def __init__(self, parent):
        super(ToolButton, self).__init__(parent)

    def setChecked(self, checked=True):
        self.setEnabled(True)
        super(ToolButton, self).setChecked(checked)
        self.setEnabled(False)

    def enterEvent(self, event):
        if not self.isChecked():
            self.setEnabled(True)

    def leaveEvent(self, event):
        if not self.isChecked():
            self.setEnabled(False)