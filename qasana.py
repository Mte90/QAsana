#!/usr/bin/python3
#Initialize PyQT
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from asana import asana
from subprocess import Popen
#The fondamental for working with python
import os,sys,signal,argparse,time
from ui_main import Ui_MainWindow
class MainWindow ( QMainWindow , Ui_MainWindow):
    #Create settings for the software
    settings = QSettings('Mte90','QAsana')
    settings.setFallbacksEnabled(False)
    version = '1.0'
    appname = 'QAsana - ' + version + ' by Mte90'
    workspaces_id = {}
    projects_id = {}
    proj_tasks_id = {}
    
    def __init__ ( self, parent = None ):
        #http://pythonadventures.wordpress.com/2013/01/10/launch-just-one-instance-of-a-qt-application/
        wid = os.popen('xdotool search --name "' + self.appname + '"').readlines()
        if_focus = os.popen('xdotool getactivewindow').readlines()
        #Check if multiple rows output
        if len(wid) > 0:
            wid = wid[0]
        #hide if the window have focues when executed again
        if if_focus[0] == wid:
            os.system('xdotool windowunmap "' + wid + '"')
            sys.exit()
        mouse = QCursor.pos()
        #Software already opened
        if wid:
            #Show
            os.system('xdotool windowmap ' + wid)
            #get focus
            os.system('xdotool windowactivate ' + wid)
            #move under cursor
            os.system('xdotool getactivewindow windowmove ' + str(mouse.x() - 50) + ' ' + str(mouse.y() - 50))
            sys.exit()
        else:
            #Load the ui
            QMainWindow.__init__( self, parent )
            self.ui = Ui_MainWindow()
            self.ui.setupUi( self )
            #Set the MainWindow Title
            self.setWindowTitle(self.appname)
            #Connect the function with the signal
            self.ui.pushSettings.clicked.connect(self.openKeyDialog)
            self.ui.pushRefresh.clicked.connect(self.loadAsana)
            self.ui.pushAddTask.clicked.connect(self.addTask)
            self.ui.pushUpdate.clicked.connect(self.updateTaskList)
            self.ui.lineTask.returnPressed.connect(self.addTask)
            self.ui.comboWorkspace.currentIndexChanged.connect(self.comboWorkspaceChanged)
            self.ui.comboProject.currentIndexChanged.connect(self.comboProjectChanged)
            #When the software are closed on console the software are closed
            signal.signal(signal.SIGINT, signal.SIG_DFL)
            parser = argparse.ArgumentParser()
            parser.add_argument("--hide", help="hide the window at startup", action="store_true")
            args = parser.parse_args()
            #Show the form
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.show()
            if not args.hide:
                #move under cursor
                os.system('xdotool getactivewindow windowmove ' + str(mouse.x() - 50) + ' ' + str(mouse.y() - 50))
            else:
                wid = os.popen('xdotool search --name "' + self.appname + '"').readlines()
                #Check if multiple rows output
                if len(wid) > 0:
                    wid = wid[0]
                os.popen('xdotool windowunmap "' + wid + '"')
            self.loadAsana()
        
    def openKeyDialog(self):
        key, ok = QInputDialog.getText(self, 'Authorization Key', 'Insert the key:',QLineEdit.Normal,self.settings.value('Key'))
        if not self.settings.value('Key'):
            self.settings.setValue('Key',key)
        
    def loadAsana(self):
        if self.settings.value('Key') != -1:
            self.ui.comboWorkspace.currentIndexChanged.disconnect(self.comboWorkspaceChanged)
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.asana_api = asana.AsanaAPI(self.settings.value('Key'), debug=True)
            #get workspace
            workspace = self.asana_api.list_workspaces()
            self.ui.comboWorkspace.clear()
            for i in workspace:
                self.workspaces_id[i['name']] = i['id']
                #populate the combobox
                self.ui.comboWorkspace.addItem(i['name'])
            self.ui.comboWorkspace.currentIndexChanged.connect(self.comboWorkspaceChanged)
            self.comboWorkspaceChanged()
        else:
            QMessageBox.critical(self.window(), "Key not configured","Set the key for access to Asana!")
    
    def comboWorkspaceChanged(self):
        self.ui.comboProject.currentIndexChanged.disconnect(self.comboProjectChanged)
        self.workspace_id = self.workspaces_id[self.ui.comboWorkspace.currentText()]
        #get projects
        projects = self.asana_api.list_projects(self.workspace_id, False)
        self.ui.comboProject.clear()
        for i in projects:
            self.projects_id[i['name']] = i['id']
            #populate the combobox
            self.ui.comboProject.addItem(i['name'])
        self.ui.comboProject.currentIndexChanged.connect(self.comboProjectChanged)
        self.comboProjectChanged()
    
    def comboProjectChanged(self):
        if len(self.ui.comboProject.currentText()) > 0:
            self.project_id = self.projects_id[self.ui.comboProject.currentText()]
            #get project tasks
            proj_tasks = self.asana_get_project_tasks(self.project_id)
            qsubtasks = QStandardItemModel()
            for i in proj_tasks:
                item = QStandardItem(i['name'])
                if not i['name'].endswith(':'):
                    check = Qt.Unchecked
                    item.setCheckState(check)
                    item.setCheckable(True)
                    self.projects_id[i['name']] = i['id']
                #populate the listview
                qsubtasks.appendRow(item)
            self.ui.listTasks.setModel(qsubtasks)
            QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))
            qsubtasks.itemChanged.connect(self.checkTasks)
        
    def checkTasks(self, item):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.asana_api.rm_project_task(self.projects_id[item.text()], self.project_id)
        self.ui.listTasks.model().removeRow(item.row())
        QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))
        
    def addTask(self):
        task = self.ui.lineTask.text()
        self.ui.lineTask.setText('')
        self.asana_api.create_task(task, self.workspace_id, 'me', None, False, None, None, None, [self.project_id])
        
    def updateTaskList(self):
        self.comboProjectChanged()
        
    #fix the include_archived not supported on get_project_tasks
    def asana_get_project_tasks(self,project_id):
        return self.asana_api._asana('projects/' + str(project_id) + '/tasks?completed_since=now')
            
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
