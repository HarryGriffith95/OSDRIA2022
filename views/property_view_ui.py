# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'property_view.ui',
# licensing of 'property_view.ui' applies.
#
# Created: Tue Feb 12 14:07:28 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_property(object):
    def setupUi(self, property):
        property.setObjectName("property")
        property.resize(240, 47)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(property.sizePolicy().hasHeightForWidth())
        property.setSizePolicy(sizePolicy)
        property.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Germany))
        self.verticalLayout = QtWidgets.QVBoxLayout(property)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.property_name = QtWidgets.QLabel(property)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(22)
        self.property_name.setFont(font)
        self.property_name.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Germany))
        self.property_name.setObjectName("property_name")
        self.verticalLayout.addWidget(self.property_name)
        self.property_value = PropertyEdit(property)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.property_value.setFont(font)
        self.property_value.setStyleSheet("border: 0px;")
        self.property_value.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Germany))
        self.property_value.setFrame(False)
        self.property_value.setReadOnly(True)
        self.property_value.setObjectName("property_value")
        self.verticalLayout.addWidget(self.property_value)

        self.retranslateUi(property)
        QtCore.QMetaObject.connectSlotsByName(property)

    def retranslateUi(self, property):
        property.setWindowTitle(QtWidgets.QApplication.translate("property", "Form", None, -1))
        self.property_name.setText(QtWidgets.QApplication.translate("property", "Property Name", None, -1))
        self.property_value.setText(QtWidgets.QApplication.translate("property", "Property Value", None, -1))

from views.components.property_edit import PropertyEdit
