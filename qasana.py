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
    workspace_id = {}
    workspace_id = {}
    
    def __init__ ( self, parent = None ):
        QMainWindow.__init__( self, parent )
        #Load the ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi( self )
        #Set the MainWindow Title
        self.setWindowTitle('QAsana - ' + self.version)
        #Connect the function with the signal
        self.ui.pushSettings.clicked.connect(self.openKeyDialog)
        self.ui.comboWorkspace.currentIndexChanged.connect(self.comboWorkspaceChanged)
        self.loadAsana()
        #When the software are closed on console the software are closed
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        #Show the form
        self.show()
        
    def openKeyDialog(self):
        key, ok = QInputDialog.getText(self, 'Athurization Key', 'Insert the key:',QLineEdit.Normal,self.settings.value('Key'))
        if not self.settings.value('Key'):
            self.settings.setValue('Key',key)
        
    def loadAsana(self):
        if self.settings.value('Key') != -1:
            self.asana_api = asana.AsanaAPI(self.settings.value('Key'), debug=True)
            workspace = self.asana_api.list_workspaces()
            for i in workspace:
                self.workspace_id[i['name']] = i['id']
                self.ui.comboWorkspace.addItem(i['name'])
            self.comboWorkspaceChanged()
        else:
            QMessageBox.critical(self.window(), "Key not configured","Set the key for access to Asana!")
            
    def comboWorkspaceChanged(self):
        task_id = self.workspace_id[self.ui.comboWorkspace.currentText()]
        tasks = self.asana_api.list_projects(task_id, False)
        self.ui.comboProject.clear()
        for i in tasks:
            self.ui.comboProject.addItem(i['name'])
            
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
