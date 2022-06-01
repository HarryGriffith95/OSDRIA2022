from PySide2.QtCore import Signal
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from models.constants import PageType, ProcessCategory

from controllers.property_ctrl import PropertyCtrl
from controllers.draftbar_element_ctrl import DraftbarElementCtrl

from views.property_view import PropertyView
from views.draftbar_element_view import DraftbarElementView

SIDEBAR_WIDTH = 260


class Sidebar(QListWidget):
    """custom sidebar widget for displaying properties & draft elements"""
    def __init__(self, parent):
        super(Sidebar, self).__init__(parent)

    def toggle(self, show):
        """show or hide sidebar"""
        self.setMaximumWidth(SIDEBAR_WIDTH if show else 0)

    def load_data(self, property_list, page_type=PageType.OVERVIEW):
        """retrieve data to display properties"""
        self.clear()
        for index, prop in enumerate(property_list):
            if page_type == PageType.DRAFT:
                draft_property_ctrl = DraftbarElementCtrl(prop)
                item = DraftbarElementView(self, ProcessCategory(index), prop, draft_property_ctrl)
            else:
                property_ctrl = PropertyCtrl(prop)
                item = PropertyView(self, prop, property_ctrl)

            # add item as widget to WidgetList
            item_widget = QListWidgetItem(self)
            item_widget.setSizeHint(item.sizeHint())
            self.addItem(item_widget)
            self.setItemWidget(item_widget, item)
