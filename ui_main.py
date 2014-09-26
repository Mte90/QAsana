# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/mte90/Desktop/Prog/QAsana/main.ui'
#
# Created: Fri Sep 26 11:31:12 2014
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(630, 470)
        MainWindow.setMaximumSize(QtCore.QSize(630, 470))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 631, 471))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setMaximumSize(QtCore.QSize(70, 16777215))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.comboWorkspace = QtGui.QComboBox(self.gridLayoutWidget)
        self.comboWorkspace.setMinimumSize(QtCore.QSize(160, 0))
        self.comboWorkspace.setObjectName(_fromUtf8("comboWorkspace"))
        self.horizontalLayout.addWidget(self.comboWorkspace)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.comboProject = QtGui.QComboBox(self.gridLayoutWidget)
        self.comboProject.setMinimumSize(QtCore.QSize(160, 0))
        self.comboProject.setObjectName(_fromUtf8("comboProject"))
        self.horizontalLayout.addWidget(self.comboProject)
        self.pushRefresh = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushRefresh.setMaximumSize(QtCore.QSize(70, 16777215))
        self.pushRefresh.setObjectName(_fromUtf8("pushRefresh"))
        self.horizontalLayout.addWidget(self.pushRefresh)
        self.pushSettings = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushSettings.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushSettings.setObjectName(_fromUtf8("pushSettings"))
        self.horizontalLayout.addWidget(self.pushSettings)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.listTasks = QtGui.QListView(self.gridLayoutWidget)
        self.listTasks.setObjectName(_fromUtf8("listTasks"))
        self.gridLayout.addWidget(self.listTasks, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", " Workspace", None))
        self.label_2.setText(_translate("MainWindow", "Project", None))
        self.pushRefresh.setText(_translate("MainWindow", "Refresh", None))
        self.pushSettings.setText(_translate("MainWindow", "Settings", None))

