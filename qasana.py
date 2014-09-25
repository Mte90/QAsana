#!/usr/bin/python3
#Initialize PyQT
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from asana import asana
#The fondamental for working with python
import os,sys,signal
from ui_main import Ui_MainWindow
class MainWindow ( QMainWindow , Ui_MainWindow):
    #Create settings for the software
    settings = QSettings('Mte90','QAsana')
    settings.setFallbacksEnabled(False)
    version = '1.0'
    workspaces_id = {}
    projects_id = {}
    proj_tasks_id = {}
    qsubtasks = QStandardItemModel()
    
    def __init__ ( self, parent = None ):
        QMainWindow.__init__( self, parent )
        #Load the ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi( self )
        #Set the MainWindow Title
        self.setWindowTitle('QAsana - ' + self.version + ' by Mte90')
        #Connect the function with the signal
        self.ui.pushSettings.clicked.connect(self.openKeyDialog)
        self.ui.comboWorkspace.currentIndexChanged.connect(self.comboWorkspaceChanged)
        self.ui.comboProject.currentIndexChanged.connect(self.comboProjectChanged)
        #When the software are closed on console the software are closed
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        #center the window on the screen
        #http://www.eurion.net/python-snippets/snippet/Center%20window.html
        screen = QDesktopWidget().screenGeometry()
        # ... and get this windows' dimensions
        mysize = self.geometry()
        # The horizontal position is calulated as screenwidth - windowwidth /2
        hpos = ( screen.width() - mysize.width() ) / 2
        # And vertical position the same, but with the height dimensions
        vpos = ( screen.height() - mysize.height() - mysize.height() ) / 2
        # And the move call repositions the window
        #self.move(hpos, vpos)
        #Show the form
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.show()
        self.loadAsana()
        
    def openKeyDialog(self):
        key, ok = QInputDialog.getText(self, 'Authorization Key', 'Insert the key:',QLineEdit.Normal,self.settings.value('Key'))
        if not self.settings.value('Key'):
            self.settings.setValue('Key',key)
        
    def loadAsana(self):
        if self.settings.value('Key') != -1:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.asana_api = asana.AsanaAPI(self.settings.value('Key'))
            workspace = self.asana_api.list_workspaces()
            for i in workspace:
                self.workspaces_id[i['name']] = i['id']
                self.ui.comboWorkspace.addItem(i['name'])
            self.comboWorkspaceChanged()
        else:
            QMessageBox.critical(self.window(), "Key not configured","Set the key for access to Asana!")
    
    def comboWorkspaceChanged(self):
        self.ui.comboProject.currentIndexChanged.disconnect(self.comboProjectChanged)
        task_id = self.workspaces_id[self.ui.comboWorkspace.currentText()]
        projects = self.asana_api.list_projects(task_id, False)
        self.ui.comboProject.clear()
        for i in projects:
            self.projects_id[i['name']] = i['id']
            self.ui.comboProject.addItem(i['name'])
        self.ui.comboProject.currentIndexChanged.connect(self.comboProjectChanged)
        self.comboProjectChanged()
    
    def comboProjectChanged(self):
        project_id = self.projects_id[self.ui.comboProject.currentText()]
        proj_tasks = self.asana_api.get_project_tasks(project_id, False)
        self.qsubtasks = QStandardItemModel()
        for i in proj_tasks:
            item = QStandardItem(i['name'])
            if not i['name'].endswith(':'):
                check = Qt.Unchecked
                item.setCheckState(check)
                item.setCheckable(True)
            self.qsubtasks.appendRow(item)
            self.proj_tasks_id[i['name']] = i['id']
        self.ui.listTasks.setModel(self.qsubtasks)
        QApplication.restoreOverrideCursor()
            
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
