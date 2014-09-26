#!/usr/bin/python3
#Initialize PyQT
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from asana import asana
from subprocess import Popen
#The fondamental for working with python
import os,sys,signal,argparse
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
    qsubtasks = QStandardItemModel()
    
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
            self.asana_api = asana.AsanaAPI(self.settings.value('Key'))
            #get workspace
            workspace = self.asana_api.list_workspaces()
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
        task_id = self.workspaces_id[self.ui.comboWorkspace.currentText()]
        #get projects
        projects = self.asana_api.list_projects(task_id, False)
        self.ui.comboProject.clear()
        for i in projects:
            self.projects_id[i['name']] = i['id']
            #populate the combobox
            self.ui.comboProject.addItem(i['name'])
        self.ui.comboProject.currentIndexChanged.connect(self.comboProjectChanged)
        self.comboProjectChanged()
    
    def comboProjectChanged(self):
        project_id = self.projects_id[self.ui.comboProject.currentText()]
        #get project tasks
        proj_tasks = self.asana_get_project_tasks(project_id)
        self.qsubtasks = QStandardItemModel()
        for i in proj_tasks:
            item = QStandardItem(i['name'])
            if not i['name'].endswith(':'):
                check = Qt.Unchecked
                item.setCheckState(check)
                item.setCheckable(True)
            #populate the listview
            self.qsubtasks.appendRow(item)
            self.proj_tasks_id[i['name']] = i['id']
        self.ui.listTasks.setModel(self.qsubtasks)
        QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))
        
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
