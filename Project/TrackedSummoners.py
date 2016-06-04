from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

import sys
import os
import DataClasses
import Database
import ApiConnection
import operator
import Widgets
from pprint import pprint
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets

class TrackedSummonersView(object):
    def __init__(self, database, dataDragon, apiConnection, mainWindow):
        self.database = database
        self.dataDragon = dataDragon
        self.apiConnection = apiConnection
        self.mainWindow = mainWindow
        self.thread = None
        self.fromLineEdit = False
        for summoner in database.SelectSummoners(DataClasses.SummonerFilter()):
            self.summoner = summoner
            break
        self.GetColumnData()
        self.setupUi(mainWindow)

    def setupUi(self, TrackedSummonersView):
        TrackedSummonersView.setObjectName("TrackedSummonersView")
        self.mainWindow.setFixedSize(self.width, 560)
        self.tableWidget = None
        self.DrawTable()
        self.AddSummonerButton = QtWidgets.QPushButton(self.centralwidget)
        self.AddSummonerButton.setGeometry(QtCore.QRect(240, 475, 93, 28))
        self.AddSummonerButton.setObjectName("AddSummonerButton")
        self.AddSummonerButton.clicked.connect(self.OnRequest)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 480, 210, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.returnPressed.connect(self.AddSummonerButton.click)
        self.summonerEntryLabel = QtWidgets.QLabel(self.centralwidget)
        self.summonerEntryLabel.setGeometry(QtCore.QRect(10, 460, 200, 16))
        self.summonerEntryLabel.setObjectName("summonerEntryLabel")
        self.statusBar = QtWidgets.QStatusBar()
        self.mainWindow.setStatusBar(self.statusBar)
        self.windowIcon = QtGui.QIcon(QtGui.QPixmap(os.getcwd() + "\\resources\windowIcon.png"))
        TrackedSummonersView.setCentralWidget(self.centralwidget)
        TrackedSummonersView.setWindowIcon(self.windowIcon)
        _translate = QtCore.QCoreApplication.translate
        TrackedSummonersView.setWindowTitle(_translate("TrackedSummonersView", "Tracked Summoners"))
        self.AddSummonerButton.setText(_translate("TrackedSummonersView", "Request"))
        self.summonerEntryLabel.setText(_translate("TrackedSummonersView", "Summoner Name"))
        QtCore.QMetaObject.connectSlotsByName(TrackedSummonersView)

    def DrawTable(self):
        self.centralwidget = QtWidgets.QWidget(self.mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        summoners = self.database.SelectSummoners(DataClasses.SummonerFilter())

        if self.tableWidget is None:
            self.tableWidget = QtWidgets.QTableWidget(len(summoners), 4 + len(self.columns), self.centralwidget)
            self.tableWidget.setGeometry(QtCore.QRect(0, 0, self.width, 450))
            self.tableWidget.verticalHeader().hide()
            #self.tableWidget.horizontalHeader().hide()
            self.tableWidget.setObjectName("tableWidget")
            optionalColumns = 0
            self.columnHeaders = list()
            self.tableWidget.setColumnWidth(0, 50) # Profile Icon
            self.columnHeaders.append("")
            self.tableWidget.setColumnWidth(1, 165) # Summoner Name
            self.columnHeaders.append("Summoner Name")
            for column in self.columns:
                if column.display:
                    self.tableWidget.setColumnWidth(2 + optionalColumns, column.width)
                    self.columnHeaders.append(column.name)
                    optionalColumns += 1
            self.tableWidget.setColumnWidth(2 + optionalColumns, 50)
            self.columnHeaders.append("")
            self.tableWidget.setColumnWidth(3 + optionalColumns, 50)
            self.columnHeaders.append("")
            self.tableWidget.setHorizontalHeaderLabels(self.columnHeaders)
            self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.tableWidget.setShowGrid(False)
            self.tableWidget.setAlternatingRowColors(True)
            #print(self.columnHeaders)
        else:
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(len(summoners))
        i = 0
        for summoner in summoners.values():
            x = 0
            profileIconItem =  QtWidgets.QTableWidgetItem()
            profileIconItem.setFlags(QtCore.Qt.ItemIsEnabled)
            profileIconItem.setData(1, QtGui.QPixmap(self.dataDragon.GetProfileIconPath(summoner.profileIconId)).scaled(50, 50, QtCore.Qt.KeepAspectRatio))
            self.tableWidget.setItem(i, x, profileIconItem)
            x += 1
            summonerNameItem = QtWidgets.QTableWidgetItem(summoner.name)
            summonerNameItem.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(i, x,summonerNameItem)
            x += 1
            if self.columnHeaders.__contains__("Level"):
                summonerLevelItem = QtWidgets.QTableWidgetItem(str(summoner.level))
                summonerLevelItem.setFlags(QtCore.Qt.ItemIsEnabled)
                summonerLevelItem.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(i, x, summonerLevelItem)
                x += 1
            if self.columnHeaders.__contains__("Win %"):
                winRate = self.database.GetSummonerWinRate(summoner.summonerId)
                winRateItem = QtWidgets.QTableWidgetItem(str(winRate) + '%')
                winRateItem.setFlags(QtCore.Qt.ItemIsEnabled)
                winRateItem.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(i, x, winRateItem)
                x += 1
            if self.columnHeaders.__contains__("Games"):
                filter = DataClasses.GameFilter()
                filter.summonerId = summoner.summonerId
                games = self.database.SelectGames(filter)
                gamesItem = QtWidgets.QTableWidgetItem(str(len(games)))
                gamesItem.setFlags(QtCore.Qt.ItemIsEnabled)
                gamesItem.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(i, x, gamesItem)
                x += 1
            if self.columnHeaders.__contains__("Frequent Champions"):
                mostPlayedChampionIconItem = Widgets.MostPlayedChampions(self.dataDragon, summoner)
                self.tableWidget.setCellWidget(i, x, mostPlayedChampionIconItem)
                x += 1
            if self.columnHeaders.__contains__("Best Champions"):
                highestWinRateChampionIconItem = Widgets.HighestWinRateChampions(self.dataDragon, summoner)
                self.tableWidget.setCellWidget(i, x, highestWinRateChampionIconItem)
                x += 1
            if self.columnHeaders.__contains__("Frequent Items"):
                mostBoughtWidget = Widgets.MostBoughtItem(self.dataDragon, summoner)
                self.tableWidget.setCellWidget(i, x, mostBoughtWidget)
                x += 1
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
            self.tableWidget.setCellWidget(i, x, refreshItem)
            x += 1
            deleteItem =  QtWidgets.QWidget()
            deleteLayout = QtWidgets.QHBoxLayout(deleteItem)
            deleteButton = QtWidgets.QPushButton()
            deletePixmap = QtGui.QPixmap(os.getcwd() + "\\resources\delete.png").scaled(20, 20, QtCore.Qt.KeepAspectRatio)
            deleteIcon = QtGui.QIcon(deletePixmap)
            deleteButton.setIcon(deleteIcon)
            deleteButton.setIconSize(deletePixmap.rect().size())
            deleteButton.setStyleSheet("QPushButton{border:none;outline:none;}")
            deleteLayout.addWidget(deleteButton)
            deleteLayout.setAlignment(QtCore.Qt.AlignLeft)
            deleteLayout.setContentsMargins(0,0,0,0)
            deleteButton.clicked.connect(partial(self.DeleteSummoner, summoner))
            deleteItem.setLayout(deleteLayout)
            self.tableWidget.setCellWidget(i, x, deleteItem)
            x += 1

            self.tableWidget.setRowHeight(i, 50)
            i += 1

    def GetColumnData(self):
        width = 320 # Mandatory Column Widths
        self.columns = self.database.GetTrackedSummonerColumns()
        if len(self.columns) == 0:
            self.database.InitializeTrackedSummonerColumns()
            self.columns = self.database.GetTrackedSummonerColumns()
        tempColumns  = list()
        for column in self.columns:
            tempColumns.append(column)
        if len(self.columns) != 0:
            self.columns = sorted(tempColumns, key=lambda x: x.trackedSummonerColumnId)
        for column in self.columns:
            if column.display:
                width += column.width
        self.width = width
        if self.width < 340:
            self.width = 340

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
        self.fromLineEdit = True

    def RefreshSummoner(self, summoner):
        self.RequestSummoner(summoner.name)

    def RequestSummoner(self, name):
        if self.thread is not None:
            return
        self.statusBar.showMessage("Retrieving {0}...".format(name), 3000)
        self.pendingSummonerName = name
        self.thread = self.RequestSummonerThread(name)
        self.thread.finished.connect(self.RequestDone)
        self.thread.start()

    def RequestDone(self):
        if self.thread.success:
            self.statusBar.showMessage("Retrieved {0}".format(self.pendingSummonerName), 3000)
            self.DrawTable()
        else:
            self.statusBar.showMessage("Unable to Retrieve {0}".format(self.pendingSummonerName), 3000)
        if self.fromLineEdit:
            self.lineEdit.setText("")
            self.fromLineEdit = False
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

    def ColumnChanged(self, trackedSummonerColumn, menuAction, isChecked):
        if not isinstance(menuAction, QtWidgets.QAction):
            print("Wrong Type")
            return
        #print(str(menuAction))
        #print("ColumnChanged Called")
        #trackedSummonerColumn.Print()
        #print("isChecked: " + str(menuAction.isChecked()))
        trackedSummonerColumn.display = isChecked
        self.database.UpdateTrackedSummonerColumn(trackedSummonerColumn)
        #print("Width: " + str(self.width))
        self.GetColumnData()
        self.mainWindow.setFixedSize(self.width, 560)
        self.setupUi(self.mainWindow)

