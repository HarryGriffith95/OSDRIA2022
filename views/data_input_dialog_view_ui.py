# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data_input_dialog_view.ui',
# licensing of 'data_input_dialog_view.ui' applies.
#
# Created: Fri Feb 15 10:17:15 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_DataInputDialog(object):
    def setupUi(self, DataInputDialog):
        DataInputDialog.setObjectName("DataInputDialog")
        DataInputDialog.resize(830, 450)
        self.verticalLayout = QtWidgets.QVBoxLayout(DataInputDialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dialog_frame = QtWidgets.QFrame(DataInputDialog)
        self.dialog_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dialog_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.dialog_frame.setLineWidth(0)
        self.dialog_frame.setObjectName("dialog_frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.dialog_frame)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.name = QtWidgets.QLabel(self.dialog_frame)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.name.setFont(font)
        self.name.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Germany))
        self.name.setObjectName("name")
        self.verticalLayout_2.addWidget(self.name)
        self.value = QtWidgets.QLineEdit(self.dialog_frame)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(22)
        self.value.setFont(font)
        self.value.setObjectName("value")
        self.verticalLayout_2.addWidget(self.value)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.data_table = QtWidgets.QTableView(self.dialog_frame)
        self.data_table.setObjectName("data_table")
        self.data_table.horizontalHeader().setCascadingSectionResizes(False)
        self.verticalLayout_3.addWidget(self.data_table)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.cancel_button = QtWidgets.QPushButton(self.dialog_frame)
        self.cancel_button.setFlat(True)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout_2.addWidget(self.cancel_button)
        self.apply_button = QtWidgets.QPushButton(self.dialog_frame)
        self.apply_button.setFlat(True)
        self.apply_button.setObjectName("apply_button")
        self.horizontalLayout_2.addWidget(self.apply_button)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.dialog_frame)

        self.retranslateUi(DataInputDialog)
        QtCore.QMetaObject.connectSlotsByName(DataInputDialog)

    def retranslateUi(self, DataInputDialog):
        DataInputDialog.setWindowTitle(QtWidgets.QApplication.translate("DataInputDialog", "Dialog", None, -1))
        self.name.setText(QtWidgets.QApplication.translate("DataInputDialog", "Name", None, -1))
        self.value.setText(QtWidgets.QApplication.translate("DataInputDialog", "Value", None, -1))
        self.cancel_button.setText(QtWidgets.QApplication.translate("DataInputDialog", "Cancel", None, -1))
        self.apply_button.setText(QtWidgets.QApplication.translate("DataInputDialog", "OK", None, -1))

