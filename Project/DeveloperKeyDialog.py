from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets

class DeveloperKeyDialog(object):
    def __init__(self, developerKeyDialog, apiConnection):
        self.apiConnection = apiConnection
        self.developerKeyDialog = developerKeyDialog
        self.SetupUi(developerKeyDialog)

    def SetupUi(self, developerKeyDialog):
        developerKeyDialog.setObjectName("developerKeyDialog")
        developerKeyDialog.resize(320, 240)
        self.buttonBox = QtWidgets.QDialogButtonBox(developerKeyDialog)
        self.buttonBox.setGeometry(QtCore.QRect(50, 200, 251, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.ok = QtWidgets.QPushButton(developerKeyDialog)
        self.ok.setText("Ok")
        self.ok.clicked.connect(self.OnOk)
        self.buttonBox.addButton(self.ok, QtWidgets.QDialogButtonBox.ActionRole)
        self.messageLabel = QtWidgets.QLabel(developerKeyDialog)
        self.messageLabel.setGeometry(QtCore.QRect(50, 10, 220, 32))
        self.messageLabel.setWordWrap(True)
        self.messageLabel.setObjectName("messageLabel")
        self.keyInput = QtWidgets.QLineEdit(developerKeyDialog)
        self.keyInput.setGeometry(QtCore.QRect(30, 40, 260, 22))
        self.keyInput.setObjectName("keyInput")
        self.riotApiLogo = QtWidgets.QLabel(developerKeyDialog)
        self.riotApiLogo.setGeometry(QtCore.QRect(50, 70, 60, 60))
        self.riotApiLogo.setText("")
        self.riotApiLogo.setPixmap(QtGui.QPixmap(os.getcwd() + "\\resources\\riotApiLogo.png"))
        self.riotApiLogo.setScaledContents(True)
        self.riotApiLogo.setObjectName("riotApiLogo")
        self.riotApiLink = QtWidgets.QLabel(developerKeyDialog)
        self.riotApiLink.setGeometry(QtCore.QRect(120, 90, 90, 22))
        self.riotApiLink.setScaledContents(False)
        self.riotApiLink.setOpenExternalLinks(True)
        self.riotApiLink.setObjectName("riotApiLink")
        self.secondaryMessageLabel = QtWidgets.QLabel(developerKeyDialog)
        self.secondaryMessageLabel.setGeometry(QtCore.QRect(30, 150, 200, 22))
        self.secondaryMessageLabel.setText("")
        self.secondaryMessageLabel.setObjectName("secondaryMessageLabel")

        self.RetranslateUi(developerKeyDialog)
        self.buttonBox.accepted.connect(developerKeyDialog.accept)
        self.buttonBox.rejected.connect(developerKeyDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(developerKeyDialog)

    def RetranslateUi(self, developerKeyDialog):
        _translate = QtCore.QCoreApplication.translate
        developerKeyDialog.setWindowTitle(_translate("developerKeyDialog", "Set Developer Key"))
        self.messageLabel.setText(_translate("developerKeyDialog", "Please Provide a Valid Developer Key:"))
        self.keyInput.setText(_translate("developerKeyDialog", self.apiConnection.database.GetKey()))
        self.riotApiLink.setText(_translate("developerKeyDialog", "<a href=\"https://developer.riotgames.com/\">Riot Games API</a>"))

    def OnOk(self):
        key = self.keyInput.text()
        if self.apiConnection.VerifyKey(key):
            self.apiConnection.database.SetKey(key)
            self.developerKeyDialog.accept()
        else:
            self.secondaryMessageLabel.setText("Unable to connect with given key.")

def PromptKey(apiConnection):
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = DeveloperKeyDialog(Dialog, apiConnection)
    return Dialog.exec()