from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

import sys
import os
import DataClasses
import Database
import ApiConnection
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets

class TrackedSummonersView(object):
    def __init__(self, database, dataDragon, apiConnection, mainWindow):
        self.database = database
        self.dataDragon = dataDragon
        self.apiConnection = apiConnection
        self.mainWindow = mainWindow
        self.thread = None
        for summoner in database.SelectSummoners(DataClasses.SummonerFilter()):
            self.summoner = summoner
            break
        self.setupUi(mainWindow)


    def setupUi(self, TrackedSummonersView):
        TrackedSummonersView.setObjectName("TrackedSummonersView")
        TrackedSummonersView.resize(500, 530)
        self.centralwidget = QtWidgets.QWidget(TrackedSummonersView)
        self.centralwidget.setObjectName("centralwidget")
        self.AddSummonerButton = QtWidgets.QPushButton(self.centralwidget)
        self.AddSummonerButton.setGeometry(QtCore.QRect(290, 475, 93, 28))
        self.AddSummonerButton.setObjectName("AddSummonerButton")
        self.AddSummonerButton.clicked.connect(self.OnRequest)
        self.tableWidget = None
        self.DrawTable()
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 480, 271, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.returnPressed.connect(self.AddSummonerButton.click)
        self.summonerEntryLabel = QtWidgets.QLabel(self.centralwidget)
        self.summonerEntryLabel.setGeometry(QtCore.QRect(10, 460, 200, 16))
        self.summonerEntryLabel.setObjectName("summonerEntryLabel")
        self.errorLabel = QtWidgets.QLabel(self.centralwidget)
        self.errorLabel.setGeometry(QtCore.QRect(20, 500, 300, 22))
        self.errorLabel.setText("")
        self.errorLabel.setObjectName("errorLabel")
        self.windowIcon = QtGui.QIcon(QtGui.QPixmap(os.getcwd() + "\\resources\windowIcon.png"))
        TrackedSummonersView.setCentralWidget(self.centralwidget)
        TrackedSummonersView.setWindowIcon(self.windowIcon)

        self.RetranslateUi(TrackedSummonersView)
        QtCore.QMetaObject.connectSlotsByName(TrackedSummonersView)

    def DrawTable(self):
        summoners = self.database.SelectSummoners(DataClasses.SummonerFilter())

        if self.tableWidget is None:
            self.tableWidget = QtWidgets.QTableWidget(len(summoners), 7, self.centralwidget)
            self.tableWidget.setGeometry(QtCore.QRect(0, 0, 500, 450))
            self.tableWidget.verticalHeader().hide()
            #self.tableWidget.horizontalHeader().hide()
            self.tableWidget.setObjectName("tableWidget")
            self.tableWidget.setColumnWidth(0, 50)
            self.tableWidget.setColumnWidth(1, 155)
            self.tableWidget.setColumnWidth(2, 50)
            self.tableWidget.setColumnWidth(3, 60)
            self.tableWidget.setColumnWidth(4, 60)
            self.tableWidget.setColumnWidth(5, 50)
            self.tableWidget.setColumnWidth(6, 50)
            self.tableWidget.setHorizontalHeaderLabels(( "Icon", "Summoner Name", "Level","Win %", "Games", "", ""))
        else:
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(len(summoners))
        i = 0
        for summoner in summoners.values():
            profileIconItem =  QtWidgets.QTableWidgetItem()
            profileIconItem.setFlags(QtCore.Qt.ItemIsEnabled)
            profileIconItem.setData(1, QtGui.QPixmap(self.dataDragon.GetProfileIconPath(summoner.profileIconId)).scaled(50, 50, QtCore.Qt.KeepAspectRatio))
            self.tableWidget.setItem(i, 0, profileIconItem)
            summonerNameItem = QtWidgets.QTableWidgetItem(summoner.name)
            summonerNameItem.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(i, 1,summonerNameItem)
            summonerLevelItem = QtWidgets.QTableWidgetItem(str(summoner.level))
            summonerLevelItem.setFlags(QtCore.Qt.ItemIsEnabled)
            summonerLevelItem.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 2, summonerLevelItem)
            winRate = self.database.GetSummonerWinRate(summoner.summonerId)
            winRateItem = QtWidgets.QTableWidgetItem(str(winRate) + '%')
            winRateItem.setFlags(QtCore.Qt.ItemIsEnabled)
            winRateItem.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 3, winRateItem)
            filter = DataClasses.GameFilter()
            filter.summonerId = summoner.summonerId
            games = self.database.SelectGames(filter)
            gamesItem = QtWidgets.QTableWidgetItem(str(len(games)))
            gamesItem.setFlags(QtCore.Qt.ItemIsEnabled)
            gamesItem.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 4, gamesItem)
            refreshItem =  QtWidgets.QWidget()
            refreshLayout = QtWidgets.QHBoxLayout(refreshItem)
            refreshButton = QtWidgets.QPushButton()
            refreshPixmap = QtGui.QPixmap(os.getcwd() + "\\resources\\refresh.png").scaled(20, 20, QtCore.Qt.KeepAspectRatio)
            refreshIcon = QtGui.QIcon(refreshPixmap)
            refreshButton.setIcon(refreshIcon)
            refreshButton.setIconSize(refreshPixmap.rect().size())
            refreshButton.setStyleSheet("QPushButton{border:none;outline:none;}")
            refreshLayout.addWidget(refreshButton)
            refreshLayout.setAlignment(QtCore.Qt.AlignCenter)
            refreshLayout.setContentsMargins(0,0,0,0)
            refreshButton.clicked.connect(partial(self.RefreshSummoner, summoner))
            refreshItem.setLayout(refreshLayout)
            self.tableWidget.setCellWidget(i, 5, refreshItem)
            deleteItem =  QtWidgets.QWidget()
            deleteLayout = QtWidgets.QHBoxLayout(deleteItem)
            deleteButton = QtWidgets.QPushButton()
            deletePixmap = QtGui.QPixmap(os.getcwd() + "\\resources\delete.png").scaled(20, 20, QtCore.Qt.KeepAspectRatio)
            deleteIcon = QtGui.QIcon(deletePixmap)
            deleteButton.setIcon(deleteIcon)
            deleteButton.setIconSize(deletePixmap.rect().size())
            deleteButton.setStyleSheet("QPushButton{border:none;outline:none;}")
            deleteLayout.addWidget(deleteButton)
            deleteLayout.setAlignment(QtCore.Qt.AlignCenter)
            deleteLayout.setContentsMargins(0,0,0,0)
            deleteButton.clicked.connect(partial(self.DeleteSummoner, summoner))
            deleteItem.setLayout(deleteLayout)
            self.tableWidget.setCellWidget(i, 6, deleteItem)

            self.tableWidget.setRowHeight(i, 50)
            i += 1

    def DeleteSummoner(self, summoner):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText('Are you sure you want to delete {0}?'.format(summoner.name))
        msgBox.addButton(QtWidgets.QPushButton('Yes'), QtWidgets.QMessageBox.YesRole)
        msgBox.addButton(QtWidgets.QPushButton('No'), QtWidgets.QMessageBox.NoRole)
        msgBox.setWindowTitle("Confirm Delete")
        msgBox.setWindowIcon(self.windowIcon)
        ret = msgBox.exec_()
        if ret == 0: # 0 is Yes, a bit strange
            self.database.DeleteSummoner(summoner.summonerId)
            self.DrawTable()

    def OnRequest(self):
        self.RequestSummoner(self.lineEdit.text())

    def RefreshSummoner(self, summoner):
        self.RequestSummoner(summoner.name)

    def RequestSummoner(self, name):
        if self.thread is not None:
            return
        self.errorLabel.setText("Retrieving {0}...".format(name))
        self.errorLabel.setStyleSheet("QLabel {color:black}")
        self.pendingSummonerName = name
        self.thread = self.RequestSummonerThread(name)
        self.thread.finished.connect(self.RequestDone)
        self.thread.start()

    def RequestDone(self):
        if self.thread.success:
            self.errorLabel.setText("Retrieved {0}".format(self.pendingSummonerName))
            self.errorLabel.setStyleSheet("QLabel {color:green}")
            self.DrawTable()
        else:
            self.errorLabel.setText("Unable to Retrieve {0}".format(self.pendingSummonerName))
            self.errorLabel.setStyleSheet("QLabel {color:red}")
        self.thread = None

    class RequestSummonerThread(QtCore.QThread):
        def __init__(self, summonerName):
            QtCore.QThread.__init__(self)
            self.summonerName = summonerName

        def __del__(self):
            self.wait()

        def run(self):
            self.database = Database.Database('locallol.db')
            self.apiConnection = ApiConnection.ApiConnection(self.database)
            requestId = self.database.RequestSummoner(self.summonerName)
            self.apiConnection.EmptyQueue()
            self.success = self.database.GetRequestStatus(requestId)

    def RetranslateUi(self, TrackedSummonersView):
        _translate = QtCore.QCoreApplication.translate
        TrackedSummonersView.setWindowTitle(_translate("TrackedSummonersView", "Tracked Summoners"))
        self.AddSummonerButton.setText(_translate("TrackedSummonersView", "Request"))
        self.summonerEntryLabel.setText(_translate("TrackedSummonersView", "Summoner Name"))

