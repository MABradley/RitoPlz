from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

import sys
import math
import Database
import DataClasses
import ApiConnection
import DeveloperKeyDialog
import OnlineResources
import TrackedSummoners
from PyQt5 import QtCore, QtGui, QtWidgets

if __name__ == "__main__":
    database = Database.Database("locallol.db")
    database.PrintTableCounts()
    apiConnection = ApiConnection.ApiConnection(database)
    if len(database.key) == 0 or not apiConnection.VerifyKey(database.key):
        if DeveloperKeyDialog.PromptKey(apiConnection):
           print('Valid Key Stored')
        else:
            print('No Key Stored')
    else:
        print("Already Have Valid Key")
    database.CheckForOutdatedSummoners()
    apiConnection.EmptyQueue()
    #database.PrintSummoners()
    dataDragon = OnlineResources.DataDragon(database)
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    trackedSummonersView = TrackedSummoners.TrackedSummonersView(database, dataDragon, apiConnection, mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
