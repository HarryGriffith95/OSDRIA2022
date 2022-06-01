from enum import Enum
from PySide2.QtCore import Signal, QRect
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QLabel
from models.model import OverviewSelection

import osdria_app_rc


class SectionSelector(QLabel):
    """hover effect over different sections of logo
    and navigation to respective page"""
    hovered = Signal(int)
    clicked = Signal()

    def __init__(self, parent):
        super(SectionSelector, self).__init__(parent)
        self.image = [
            QPixmap(":/icons/img/logo_light@2x.png"),
            QPixmap(":/icons/img/logo_light_energy@2x.png"),
            QPixmap(":/icons/img/logo_light_water@2x.png"),
            QPixmap(":/icons/img/logo_light_food@2x.png"),
            QPixmap(":/icons/img/logo_light_business@2x.png")
        ]
        self._section = OverviewSelection.OVERVIEW
        self.updateGeometry()

    def change_icon(self, selection):
        self.setPixmap(self.image[selection.value])

    def mouseMoveEvent(self, event):
        """set section variable according to mouse position"""
        relative_x = event.pos().x() / self.width()
        relative_y = event.pos().y() / self.height()

        # check conditions for all four section regions
        energy_x = (relative_x > 50 / 1800) & (relative_x < 570 / 1800)
        energy_y = (relative_y > 950 / 1800) & (relative_y < 1500 / 1800)
        water_x = (relative_x > 700 / 1800) & (relative_x < 1100 / 1800)
        water_y = (relative_y > 0 / 1800) & (relative_y < 500 / 1800)
        food_x = (relative_x > 1230 / 1800) & (relative_x < 1750 / 1800)
        food_y = (relative_y > 950 / 1800) & (relative_y < 1500 / 1800)
        business_x = (relative_x > 570 / 1800) & (relative_x < 1230 / 1800)
        business_y = (relative_y > 600 / 1800) & (relative_y < 1200 / 1800)

        # perform hovering effect for the corresponding section
        if energy_x & energy_y:
            self._section = OverviewSelection.ENERGY
        elif water_x & water_y:
            self._section = OverviewSelection.WATER
        elif food_x & food_y:
            self._section = OverviewSelection.FOOD
        elif business_x & business_y:
            self._section = OverviewSelection.BUSINESS
        else:
            self._section = OverviewSelection.OVERVIEW

        # emit hovered signal to change title
        self.hovered.emit(self._section.value)

    def mousePressEvent(self, event):
        # only emit clicked signal on actual sections
        if self._section != OverviewSelection.OVERVIEW:
            self.clicked.emit()

    def showEvent(self, event):
        self.change_icon(OverviewSelection.OVERVIEW)

    def resizeEvent(self, event):
        """keep aspect ratio of logo"""
        width = self.width()
        height = self.height()
        pos_x = (self.parent().width() - width) / 2
        pos_y = (self.parent().height() - height) / 2
        min_size = min(width, height)
        self.setGeometry(QRect(pos_x, pos_y, min_size, min_size))
