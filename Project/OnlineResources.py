from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

import http.client
import json
import os
from pprint import pprint
import shutil
import requests
import Database


class DataDragon:
    def __init__(self, database):
        self.database = database
        self.profileIconVersion = "6.10.1" # default
        response = requests.get('https://global.api.pvp.net/api/lol/static-data/na/v1.2/realm?api_key={0}'.format(self.database.GetKey()))
        if response.status_code == 200:
            responseDict = json.loads(response.text)
            self.profileIconVersion = responseDict["n"]["profileicon"]
        else:
            print("DataDragon: Unable to Contact global.api.pvp.net")

    def GetProfileIconPath(self, profileIconId):
        response = requests.get('https://ddragon.leagueoflegends.com/cdn/{0}/img/profileicon/{1}.png'.format(self.profileIconVersion, profileIconId), stream=True)
        if response.status_code == 200:
            with open(os.getcwd() + '/resources/profileicons/icon{0}.png'.format(profileIconId), 'wb') as file:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, file)
                return os.getcwd() + '/resources/profileicons/icon{0}.png'.format(profileIconId)
        else:
            print("DataDragon: Unable to Contact ddragon.leagueoflegends.com")
            if os.path.exists(os.getcwd() + '/resources/profileicons/icon{0}.png'.format(profileIconId)):
                return os.getcwd() + '/resources/profileicons/icon{0}.png'.format(profileIconId)
        return None

