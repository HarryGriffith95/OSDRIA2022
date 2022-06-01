# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'draftbar_element_view.ui',
# licensing of 'draftbar_element_view.ui' applies.
#
# Created: Sat Mar  2 15:48:32 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_DraftElement(object):
    def setupUi(self, DraftElement):
        DraftElement.setObjectName("DraftElement")
        DraftElement.resize(240, 106)
        DraftElement.setMaximumSize(QtCore.QSize(240, 16777215))
        DraftElement.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Germany))
        self.verticalLayout = QtWidgets.QVBoxLayout(DraftElement)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.element_label = QtWidgets.QPushButton(DraftElement)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.element_label.setFont(font)
        self.element_label.setStyleSheet("border: 0px")
        self.element_label.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Germany))
        self.element_label.setIconSize(QtCore.QSize(10, 10))
        self.element_label.setDefault(False)
        self.element_label.setFlat(True)
        self.element_label.setObjectName("element_label")
        self.horizontalLayout.addWidget(self.element_label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.dropdown_button = ToolButton(DraftElement)
        self.dropdown_button.setEnabled(False)
        self.dropdown_button.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Germany))
        self.dropdown_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/img/dropdown_normal@2x.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.dropdown_button.setIcon(icon)
        self.dropdown_button.setIconSize(QtCore.QSize(10, 10))
        self.dropdown_button.setObjectName("dropdown_button")
        self.horizontalLayout.addWidget(self.dropdown_button)
        spacerItem1 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.element_list = QtWidgets.QTableView(DraftElement)
        self.element_list.setMaximumSize(QtCore.QSize(240, 100))
        self.element_list.setFrameShadow(QtWidgets.QFrame.Plain)
        self.element_list.setLineWidth(0)
        self.element_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.element_list.setDragEnabled(True)
        self.element_list.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.element_list.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.element_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.element_list.setShowGrid(False)
        self.element_list.setObjectName("element_list")
        self.element_list.horizontalHeader().setVisible(False)
        self.element_list.horizontalHeader().setDefaultSectionSize(80)
        self.element_list.horizontalHeader().setHighlightSections(False)
        self.element_list.horizontalHeader().setMinimumSectionSize(80)
        self.element_list.verticalHeader().setVisible(False)
        self.element_list.verticalHeader().setDefaultSectionSize(60)
        self.element_list.verticalHeader().setHighlightSections(False)
        self.element_list.verticalHeader().setMinimumSectionSize(60)
        self.verticalLayout.addWidget(self.element_list)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(DraftElement)
        QtCore.QMetaObject.connectSlotsByName(DraftElement)

    def retranslateUi(self, DraftElement):
        DraftElement.setWindowTitle(QtWidgets.QApplication.translate("DraftElement", "Form", None, -1))
        self.element_label.setText(QtWidgets.QApplication.translate("DraftElement", "Element Type", None, -1))

from views.components.tool_button import ToolButton
import osdria_app_rc
