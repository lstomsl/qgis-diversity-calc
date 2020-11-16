# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'diversity_results_dialog_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dlgResults(object):
    def setupUi(self, dlgResults):
        dlgResults.setObjectName("dlgResults")
        dlgResults.resize(640, 480)
        self.verticalLayoutWidget = QtWidgets.QWidget(dlgResults)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 621, 461))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.lytMain = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.lytMain.setContentsMargins(0, 0, 0, 0)
        self.lytMain.setObjectName("lytMain")
        self.trwResults = QtWidgets.QTreeWidget(self.verticalLayoutWidget)
        self.trwResults.setAlternatingRowColors(True)
        self.trwResults.setObjectName("trwResults")
        self.lytMain.addWidget(self.trwResults)

        self.retranslateUi(dlgResults)
        QtCore.QMetaObject.connectSlotsByName(dlgResults)

    def retranslateUi(self, dlgResults):
        _translate = QtCore.QCoreApplication.translate
        dlgResults.setWindowTitle(_translate("dlgResults", "Diversity Results"))
        self.trwResults.headerItem().setText(0, _translate("dlgResults", "Name"))
        self.trwResults.headerItem().setText(1, _translate("dlgResults", "Count"))
        self.trwResults.headerItem().setText(2, _translate("dlgResults", "Richness"))
        self.trwResults.headerItem().setText(3, _translate("dlgResults", "Evenness"))
        self.trwResults.headerItem().setText(4, _translate("dlgResults", "Shannons"))
        self.trwResults.headerItem().setText(5, _translate("dlgResults", "Simpsons"))

