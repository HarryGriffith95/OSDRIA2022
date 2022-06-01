# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'optimization_dialog_view.ui',
# licensing of 'optimization_dialog_view.ui' applies.
#
# Created: Sat Apr 20 07:34:01 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_OptimizationDialog(object):
    def setupUi(self, OptimizationDialog):
        OptimizationDialog.setObjectName("OptimizationDialog")
        OptimizationDialog.resize(400, 400)
        self.verticalLayout = QtWidgets.QVBoxLayout(OptimizationDialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dialog_frame = QtWidgets.QFrame(OptimizationDialog)
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
        self.name = QtWidgets.QLabel(self.dialog_frame)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.name.setFont(font)
        self.name.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.name.setObjectName("name")
        self.horizontalLayout.addWidget(self.name)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.logo = QtWidgets.QLabel(self.dialog_frame)
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap(":/icons/img/logo@2x.png"))
        self.logo.setObjectName("logo")
        self.horizontalLayout_3.addWidget(self.logo)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.information_text = QtWidgets.QLabel(self.dialog_frame)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.information_text.setFont(font)
        self.information_text.setAlignment(QtCore.Qt.AlignCenter)
        self.information_text.setObjectName("information_text")
        self.horizontalLayout_4.addWidget(self.information_text)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.cancel_button = QtWidgets.QPushButton(self.dialog_frame)
        self.cancel_button.setMinimumSize(QtCore.QSize(100, 30))
        self.cancel_button.setFlat(False)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout_2.addWidget(self.cancel_button)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.dialog_frame)

        self.retranslateUi(OptimizationDialog)
        QtCore.QMetaObject.connectSlotsByName(OptimizationDialog)

    def retranslateUi(self, OptimizationDialog):
        OptimizationDialog.setWindowTitle(QtWidgets.QApplication.translate("OptimizationDialog", "Dialog", None, -1))
        self.name.setText(QtWidgets.QApplication.translate("OptimizationDialog", "Optimization of System Configuration", None, -1))
        self.information_text.setText(QtWidgets.QApplication.translate("OptimizationDialog", "TextLabel", None, -1))
        self.cancel_button.setText(QtWidgets.QApplication.translate("OptimizationDialog", "Cancel", None, -1))

import osdria_app_rc
