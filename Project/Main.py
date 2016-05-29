from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

import Database
import ApiConnection
import DeveloperKeyDialog

if __name__ == "__main__":
    database = Database.Database("locallol.db")
    apiConnection = ApiConnection.ApiConnection(database)
    if len(database.key) == 0 or not apiConnection.VerifyKey(database.key):
        if DeveloperKeyDialog.PromptKey(apiConnection):
           print('Valid Key Stored')
        else:
            print('No Key Stored')
    else:
        print("Already Have Valid Key")
    #database.RequestSummoner("ChimpanXebra")
    database.CheckForOutdatedSummoners()
    apiConnection.EmptyQueue()


