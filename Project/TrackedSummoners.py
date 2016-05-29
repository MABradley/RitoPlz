from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

import sys
import DataClasses
from PyQt5 import QtCore, QtGui, QtWidgets

class TrackedSummonersView(object):
    def __init__(self, database, dataDragon, apiConnection, mainWindow):
        self.database = database
        self.dataDragon = dataDragon
        self.apiConnection = apiConnection
        self.mainWindow = mainWindow
        for summoner in database.SelectSummoners(DataClasses.SummonerFilter()):
            self.summoner = summoner
            break
        self.setupUi(mainWindow)


    def setupUi(self, TrackedSummonersView):
        TrackedSummonersView.setObjectName("TrackedSummonersView")
        TrackedSummonersView.resize(400, 530)
        self.centralwidget = QtWidgets.QWidget(TrackedSummonersView)
        self.centralwidget.setObjectName("centralwidget")
        self.AddSummonerButton = QtWidgets.QPushButton(self.centralwidget)
        self.AddSummonerButton.setGeometry(QtCore.QRect(290, 470, 93, 28))
        self.AddSummonerButton.setObjectName("AddSummonerButton")
        self.AddSummonerButton.clicked.connect(self.OnAdd)
        self.DrawTable()
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 480, 271, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.summonerEntryLabel = QtWidgets.QLabel(self.centralwidget)
        self.summonerEntryLabel.setGeometry(QtCore.QRect(10, 460, 200, 16))
        self.summonerEntryLabel.setObjectName("summonerEntryLabel")
        self.errorLabel = QtWidgets.QLabel(self.centralwidget)
        self.errorLabel.setGeometry(QtCore.QRect(20, 500, 300, 22))
        self.errorLabel.setText("")
        self.errorLabel.setObjectName("errorLabel")
        TrackedSummonersView.setCentralWidget(self.centralwidget)

        self.RetranslateUi(TrackedSummonersView)
        QtCore.QMetaObject.connectSlotsByName(TrackedSummonersView)

    def DrawTable(self):
        summoners = self.database.SelectSummoners(DataClasses.SummonerFilter())

        self.tableWidget = QtWidgets.QTableWidget(len(summoners), 3, self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 380, 450))
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 50)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setHorizontalHeaderLabels(("Summoner Name", "Level", "Profile Icon"))
        i = 0
        for summoner in summoners:
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(summoner.name))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(summoner.level)))
            self.profileIconItem =  QtWidgets.QTableWidgetItem()
            self.profileIconItem.setData(1, QtGui.QPixmap(self.dataDragon.GetProfileIconPath(summoner.profileIconId)).scaled(100, 100, QtCore.Qt.KeepAspectRatio))
            self.tableWidget.setItem(i, 2, self.profileIconItem)
            self.tableWidget.setRowHeight(i, 100)
            i += 1

    def OnAdd(self):
        name = self.lineEdit.text()
        self.database.RequestSummoner(name)
        self.apiConnection.EmptyQueue()
        filter = DataClasses.SummonerFilter()
        filter.summonerName = name
        success = False
        for summoner in self.database.SelectSummoners(filter):
            self.summoner = summoner
            self.DrawTable()
            self.errorLabel.setText('Successfully retrieved {0}'.format(name))
            success = True
            break
        if not success:
            self.errorLabel.setText('Unable to retrieve {0}'.format(name))


    def RetranslateUi(self, TrackedSummonersView):
        _translate = QtCore.QCoreApplication.translate
        TrackedSummonersView.setWindowTitle(_translate("TrackedSummonersView", "Tracked Summoners"))
        self.AddSummonerButton.setText(_translate("TrackedSummonersView", "Request"))
        self.summonerEntryLabel.setText(_translate("TrackedSummonersView", "Summoner Name"))

