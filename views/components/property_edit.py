from PySide2.QtCore import Signal, QSize, Qt
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QLineEdit

from views.property_popup_view import PropertyPopupView
from controllers.property_popup_ctrl import PropertyPopupCtrl

from models.property import PropertyValue
from models.constants import PropType

class PropertyEdit(QLineEdit):
    """custom QLineEdit class for click-able actions
    @signal: clicked()
    @signal: inputFinished(str)"""
    clicked = Signal()
    inputFinished = Signal(str)

    def __init__(self, parent):
        super(PropertyEdit, self).__init__(parent)
        self.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.returnPressed.connect(self.clearFocus)
        self._model = PropertyValue()
        self._popup = False
        self.clearFocus()

    def set_model(self, model):
        self._model = model
        self._model.value_changed.connect(
            # todo issue: cancel button updates dialog model
           lambda: self.setText(str(self._model.value)))
        self.add_unit(model.value)
        if model.type == PropType.POPUP_MENU:
            self.setReadOnly(True)
            self.set_popup(True)
        elif model.type == PropType.DIALOG:
            self.setReadOnly(True)
        elif model.type == PropType.LINE_EDIT:
            self.setReadOnly(model.read_only)
            # display of content done by self.focusOutEvent()
            self._model.value_changed.disconnect()

    def text(self):
        if self._model.unit is "":
            return super().text()
        else:
            # remove unit
            return super().text().split(" " + self._model.unit)[0]

    def is_popup(self):
        return self._popup

    def set_popup(self, value):
        self._popup = value
        if not self.actions():
            dropdown_icon = QIcon()
            dropdown_icon.addPixmap(QPixmap(":/icons/img/dropdown_normal@2x.png"), QIcon.Normal, QIcon.Off)
            dropdown_icon.actualSize(QSize(10, 10))
            popup_action = self.addAction(dropdown_icon, QLineEdit.TrailingPosition)
            popup_action.triggered.connect(self.show_popup)

    def mousePressEvent(self, event):
        super().setText(self.text())
        if self.isReadOnly():
            self.clicked.emit()

        if self.is_popup():
            self.show_popup()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        # add unit
        self.add_unit(super().text())

        if self.hasAcceptableInput() & (self._model.type == PropType.LINE_EDIT):
            self._model.value = self.text()

    def add_unit(self, value):
        """adding unit to displayed text"""
        displayed_text = str(value)
        if self._model.unit is not "":
            displayed_text += " " + self._model.unit
        super().setText(displayed_text)

    def show_popup(self):
        if len(self._model.choices) > 1:
            popup_ctrl = PropertyPopupCtrl(self._model)
            popup_view = PropertyPopupView(self, self._model, popup_ctrl)
            popup_view.show_popup()
