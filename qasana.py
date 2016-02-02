#!/usr/bin/python3
# pylint: disable=fixme, line-too-long
#Initialize PyQT
from PyQt4.QtCore import Qt, QSettings
from PyQt4.QtGui import QApplication, QMainWindow, QCursor, QStandardItemModel, QStandardItem, QMessageBox, QLineEdit, QInputDialog, QFont
import asana
#The fondamental for working with python
import os, sys, signal, argparse
from ui_main import Ui_MainWindow
class MainWindow(QMainWindow, Ui_MainWindow):
    #Create settings for the software
    settings = QSettings('Mte90', 'QAsana')
    settings.setFallbacksEnabled(False)
    version = '2.0'
    appname = 'QAsana - ' + version + ' by Mte90'
    workspaces_id = {}
    workspace_id = ''
    projects_id = {}
    project_id = ''
    proj_tasks_id = {}
    asana_api = None

    def __init__(self, parent=None):
        #http://pythonadventures.wordpress.com/2013/01/10/launch-just-one-instance-of-a-qt-application/
        wid = self.get_pid()
        if_focus = os.popen('xdotool getactivewindow').readlines()
        #hide if the window have focues when executed again
        if if_focus[0] == wid:
            os.system('xdotool windowunmap "' + wid + '"')
            sys.exit()
        #Software already opened
        if wid:
            #Show
            os.system('xdotool windowmap ' + wid)
            #get focus
            os.system('xdotool windowactivate ' + wid)
            move_under_cursor()
            sys.exit()
        else:
            #Load the ui
            QMainWindow.__init__(self, parent)
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            #Set the MainWindow Title
            self.setWindowTitle(self.appname)
            #Connect the function with the signal
            self.ui.pushSettings.clicked.connect(self.openKeyDialog)
            self.ui.pushRefresh.clicked.connect(self.loadAsana)
            self.ui.pushAddTask.clicked.connect(self.addTask)
            self.ui.pushUpdate.clicked.connect(self.comboProjectChanged)
            self.ui.lineTask.returnPressed.connect(self.addTask)
            self.ui.comboWorkspace.currentIndexChanged.connect(self.comboWorkspaceChanged)
            self.ui.comboProject.currentIndexChanged.connect(self.comboProjectChanged)
            #When the software are closed on console the software are closed
            signal.signal(signal.SIGINT, signal.SIG_DFL)
            #Add hide parameter
            parser = argparse.ArgumentParser()
            parser.add_argument("--hide", help="hide the window at startup", action="store_true")
            args = parser.parse_args()
            #Show the form
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.show()
            if not args.hide:
                move_under_cursor()
            else:
                wid = self.get_pid()
                os.popen('xdotool windowunmap "' + wid + '"')
            self.loadAsana()

    def openKeyDialog(self):
        key, ok = QInputDialog.getText(self, 'Authorization Key', 'Insert the key:', QLineEdit.Normal, self.settings.value('Key'))
        if not self.settings.value('Key'):
            self.settings.setValue('Key', key)

    def loadAsana(self):
        if self.settings.value('Key') != -1:
            if self.settings.value('Key'):
                self.ui.comboWorkspace.currentIndexChanged.disconnect(self.comboWorkspaceChanged)
                QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                self.asana_api = asana.Client.access_token(self.settings.value('Key'))
                #get workspace
                workspace = self.asana_api.users.me()
                workspace = workspace['workspaces']
                self.ui.comboWorkspace.clear()
                for workspace in self.asana_api.workspaces.find_all():
                    self.workspaces_id[workspace['name']] = workspace['id']
                    #populate the combobox
                    self.ui.comboWorkspace.addItem(workspace['name'])
                self.ui.comboWorkspace.currentIndexChanged.connect(self.comboWorkspaceChanged)
                self.comboWorkspaceChanged()
            else:
                QMessageBox.critical(self.window(), "Key not configured", "Set the key for access to Asana!")
        else:
            QMessageBox.critical(self.window(), "Key not configured", "Set the key for access to Asana!")

    def comboWorkspaceChanged(self):
        self.ui.comboProject.currentIndexChanged.disconnect(self.comboProjectChanged)
        self.workspace_id = self.workspaces_id[self.ui.comboWorkspace.currentText()]
        #get projects
        self.ui.comboProject.clear()
        for projects in self.asana_api.projects.find_all({'workspace': self.workspace_id, 'archived': 'false'}):
            self.projects_id[projects['name']] = projects['id']
            #populate the combobox
            self.ui.comboProject.addItem(projects['name'])
        self.ui.comboProject.currentIndexChanged.connect(self.comboProjectChanged)
        self.comboProjectChanged()

    def comboProjectChanged(self):
        if len(self.ui.comboProject.currentText()) > 0:
            self.project_id = self.projects_id[self.ui.comboProject.currentText()]
            #get project tasks
            qsubtasks = QStandardItemModel()
            for proj_tasks in self.asana_api.tasks.find_by_project(self.project_id, { 'completed_since': 'now'}):
                item = QStandardItem(proj_tasks['name'])
                item.setEditable(True)
                item.setToolTip('Double click to edit')
                if not proj_tasks['name'].endswith(':'):
                    check = Qt.Unchecked
                    item.setCheckState(check)
                    item.setCheckable(True)
                    self.projects_id[proj_tasks['name']] = proj_tasks['id']
                    item.setStatusTip(str(proj_tasks['id']))
                else:
                    font = QFont()
                    font.setWeight(QFont.Bold)
                    item.setFont(font)
                #populate the listview
                qsubtasks.appendRow(item)
            self.ui.listTasks.setModel(qsubtasks)
            QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))
            qsubtasks.itemChanged.connect(self.checkTasks)

    def checkTasks(self, item):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        if item.checkState():
            self.asana_api.tasks.delete(self.projects_id[item.text()])
            self.ui.listTasks.model().removeRow(item.row())
        else:
            self.asana_api.tasks.update(item.statusTip(), {'id': item.statusTip(), 'name': item.text()})
        QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))

    def addTask(self):
        task = self.ui.lineTask.text()
        self.ui.lineTask.setText('')
        self.asana_api.tasks.create_in_workspace(self.workspace_id, {'name': task, 'projects': [self.project_id]})
        self.comboProjectChanged()

    def get_pid(self):
        wid = os.popen('xdotool search --name "' + self.appname + '"').readlines()
        #Check if multiple rows output
        if len(wid) > 0:
            wid = wid[0]
        return wid

def move_under_cursor():
    mouse = QCursor.pos()
    os.system('xdotool getactivewindow windowmove ' + str(mouse.x() - 50) + ' ' + str(mouse.y() - 50))

def main():
    #Start the software
    app = QApplication(sys.argv)
    MainWindow_ = QMainWindow()
    ui = MainWindow()
    ui.setupUi(MainWindow_)
    #Add the close feature at the program with the X
    sys.exit(app.exec_())

#Execute the software
main()
