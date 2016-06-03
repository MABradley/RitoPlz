from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

from PyQt5 import QtCore, QtGui, QtWidgets
from pprint import pprint
import operator

class MostPlayedChampions(QtWidgets.QWidget):

    def __init__(self, dataDragon, summoner, parent=None):
        super(MostPlayedChampions,self).__init__(parent)

        # add your buttons
        layout = QtWidgets.QGridLayout()

        # adjust spacings to your needs
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)


        champ1 = None
        champ2 = None
        champ3 = None

        champions = dataDragon.database.GetMostPlayedChampionsBySummoner(summoner.summonerId)
        sortedChampions = sorted(champions.items(), key=operator.itemgetter(1), reverse=True)
        #pprint(sortedChampions)
        for champ in sortedChampions:
            #print("champ[0]:"+str(champ[0]))
            if champ1 is None:
                champ1 = dataDragon.database.GetChampion(champ[0])
                label = QtWidgets.QLabel()
                label.setPixmap(QtGui.QPixmap(dataDragon.GetChampionIconPath(champ1)).scaled(50, 50, QtCore.Qt.KeepAspectRatio))
                layout.addWidget(label, 0, 0)
            elif champ2 is None:
                champ2 = dataDragon.database.GetChampion(champ[0])
                label1 = QtWidgets.QLabel()
                label1.setPixmap(QtGui.QPixmap(dataDragon.GetChampionIconPath(champ2)).scaled(50, 50, QtCore.Qt.KeepAspectRatio))
                layout.addWidget(label1, 0, 1)
            elif champ3 is None:
                champ3 = dataDragon.database.GetChampion(champ[0])
                label2 = QtWidgets.QLabel()
                label2.setPixmap(QtGui.QPixmap(dataDragon.GetChampionIconPath(champ3)).scaled(50, 50, QtCore.Qt.KeepAspectRatio))
                layout.addWidget(label2, 0, 2)
            else:
                break

        layout.setAlignment(QtCore.Qt.AlignLeft)
        self.setLayout(layout)


class MostBoughtItem(QtWidgets.QWidget):

    def __init__(self, dataDragon, summoner, parent=None):
        super(MostBoughtItem,self).__init__(parent)

        # add your buttons
        layout = QtWidgets.QGridLayout()

        # adjust spacings to your needs
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)


        item1 = None
        item2 = None
        item3 = None

        excludedItems = (3340, 3363, 3364, 0, 1311)

        items = dataDragon.database.GetMostBoughtItemsBySummoner(summoner.summonerId)
        sortedItems = sorted(items.items(), key=operator.itemgetter(1), reverse=True)
        #pprint(sortedChampions)
        for item in sortedItems:
            if item[0] in excludedItems:
                continue
            #print("item[0]:"+str(item[0]))
            if item1 is None:
                item1 = item[0]
                label = QtWidgets.QLabel()
                label.setPixmap(QtGui.QPixmap(dataDragon.GetItemIconPath(item1)).scaled(50, 50, QtCore.Qt.KeepAspectRatio))
                layout.addWidget(label, 0, 0)
               # break # single return for now
            elif item2 is None:
                item2 = item[0]
                label1 = QtWidgets.QLabel()
                label1.setPixmap(QtGui.QPixmap(dataDragon.GetItemIconPath(item2)).scaled(50, 50, QtCore.Qt.KeepAspectRatio))
                layout.addWidget(label1, 0, 1)
            elif item3 is None:
                item3 = item[0]
                label2 = QtWidgets.QLabel()
                label2.setPixmap(QtGui.QPixmap(dataDragon.GetItemIconPath(item3)).scaled(50, 50, QtCore.Qt.KeepAspectRatio))
                layout.addWidget(label2, 0, 2)
            else:
                break

        layout.setAlignment(QtCore.Qt.AlignLeft)
        self.setLayout(layout)