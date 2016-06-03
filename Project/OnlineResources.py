from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

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
        self.championVersion = "6.10.1"
        response = requests.get('https://global.api.pvp.net/api/lol/static-data/na/v1.2/realm?api_key={0}'.format(self.database.GetKey()))
        if response.status_code == 200:
            responseDict = json.loads(response.text)
            self.profileIconVersion = responseDict["n"]["profileicon"]
            if not os.path.exists(os.getcwd() + '/resources/profileicons/'):
                os.makedirs(os.getcwd() + '/resources/profileicons/')
            self.profileIconDirectory = os.getcwd() + '/resources/profileicons/' + self.profileIconVersion + '/'
            if not os.path.exists(self.profileIconDirectory):
                os.makedirs(self.profileIconDirectory)
            self.championVersion = responseDict["n"]["champion"]
            if not os.path.exists(os.getcwd() + '/resources/championicons/'):
                os.makedirs(os.getcwd() + '/resources/championicons/')
            self.championIconDirectory = os.getcwd() + '/resources/championicons/' + self.championVersion + '/'
            if not os.path.exists(self.championIconDirectory):
                os.makedirs(self.championIconDirectory)
            self.itemVersion = responseDict["n"]["item"]
            if not os.path.exists(os.getcwd() + '/resources/itemicons/'):
                os.makedirs(os.getcwd() + '/resources/itemicons/')
            self.itemIconDirectory = os.getcwd() + '/resources/itemicons/' + self.itemVersion + '/'
            if not os.path.exists(self.itemIconDirectory):
                os.makedirs(self.itemIconDirectory)
        else:
            print("DataDragon: Unable to retrieve static data, response:")
            print(response.text)

    def GetProfileIconPath(self, profileIconId):
        if os.path.exists(self.profileIconDirectory + 'icon{0}.png'.format(profileIconId)):
            return self.profileIconDirectory + 'icon{0}.png'.format(profileIconId)
        response = requests.get('https://ddragon.leagueoflegends.com/cdn/{0}/img/profileicon/{1}.png'.format(self.profileIconVersion, profileIconId), stream=True)
        if response.status_code == 200:
            with open(self.profileIconDirectory + 'icon{0}.png'.format(profileIconId), 'wb') as file:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, file)
                return self.profileIconDirectory + 'icon{0}.png'.format(profileIconId)
        else:
            print("DataDragon: Unable to retrieve profile icon, response:")
            print(response.text)
        return None

    def GetChampionIconPath(self, champion):
        if os.path.exists(self.championIconDirectory + 'championicon{0}.png'.format(champion.championId)):
            return self.championIconDirectory + 'championicon{0}.png'.format(champion.championId)
        response = requests.get("https://ddragon.leagueoflegends.com/cdn/{0}/img/champion/{1}.png".format(self.championVersion, champion.key), stream=True)
        if response.status_code == 200:
            with open(self.championIconDirectory + 'championicon{0}.png'.format(champion.championId), 'wb') as file:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, file)
                return self.championIconDirectory + 'championicon{0}.png'.format(champion.championId)
        else:
            print("DataDragon: Unable to retrieve Champion Icon, Champion:")
            champion.Print()
            print("Response:")
            print(response.text)
        return None

    def GetItemIconPath(self, itemId):
        if os.path.exists(self.itemIconDirectory + 'item{0}.png'.format(itemId)):
            return self.itemIconDirectory + 'item{0}.png'.format(itemId)
        response = requests.get("https://ddragon.leagueoflegends.com/cdn/{0}/img/item/{1}.png".format(self.itemVersion, itemId), stream=True)
        if response.status_code == 200:
            with open(self.itemIconDirectory + 'item{0}.png'.format(itemId), 'wb') as file:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, file)
                return self.itemIconDirectory + 'item{0}.png'.format(itemId)
        else:
            print("DataDragon: Unable to retrieve Item Icon, response:")
            print(itemId)
            print(response.text)
        return None