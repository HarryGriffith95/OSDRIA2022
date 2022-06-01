"""definition of all icons used in the app"""
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *


ICON_DIRECTORY = "/Users/stefan/Dropbox/Uni/Master/Semester_04/01_master_thesis/05_OSDRIA/01_GUI/gui_icons/"

ICON_BUTTON_LIST = ["add", "back", "close", "export", "graph",
                    "minus", "run", "scenarios", "trash"]
ICON_BUTTON_TYPES = ["normal", "select"]

ICON_TOGGLE_LIST = ["connect", "cursor", "draft", "sidebar",
                    "zoom-in", "zoom-out", "zoom-range"]
ICON_TOGGLE_TYPE = ["normal", "select_orange"]  # options: select, select_blue

ICON_IMAGE_LIST = ["new", "open", "logo"]


def init():
    """Initialise icons as class variable with both states as dictionary"""
    for button in ICON_BUTTON_LIST:
        globals()[button] = QIcon()
        for type in ICON_BUTTON_TYPES:
            iconMode = QIcon.Normal
            if type is "select":
                iconMode = QIcon.Active
            globals()[button].addPixmap(QPixmap(
                ICON_DIRECTORY + button + "_" + type + "@2x.png"),
                iconMode,
                QIcon.On)

    for toggle in ICON_TOGGLE_LIST:
        globals()[toggle] = QIcon()
        for type in ICON_TOGGLE_TYPE:
            iconMode = QIcon.Normal
            if type is "select_orange":
                iconMode = QIcon.Active
            globals()[button].addPixmap(QPixmap(
                ICON_DIRECTORY + toggle + "_" + type + "@2x.png"),
                iconMode,
                QIcon.On)

    for image in ICON_IMAGE_LIST:
        globals()[image] = QPixmap(ICON_DIRECTORY + image + "@2x.png")
