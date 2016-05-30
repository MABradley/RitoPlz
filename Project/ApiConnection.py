from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

import requests
import json
import time
import datetime
import DataClasses

class ApiConnection:
    def __init__(self, database):
        self.database = database
        self.nextRequestTime = datetime.datetime.now()


    def EmptyQueue(self):
        # loose assumption that 5 calls will be timing free:
        i = 0
        while True:
            if self.database.GetNextRequest() is None:
                print("Request Queue is Empty")
                break
            if self.nextRequestTime < datetime.datetime.now():
                print('Sending Request - Request Count: ' + str(self.database.GetRequestQueueCount()))
                self.HandleNextCall()
                if (i > 5):
                    time.sleep(1)
            else:
                print('Sleeping - Request Count: ' + str(self.database.GetRequestQueueCount()))
                time.sleep(1)
            i += 1

    def VerifyKey(self, key):
        response = requests.get('https://na.api.pvp.net/api/lol/na/v1.2/champion/1?api_key={0}'.format(key))
        if response.status_code == 200:
            return True
        else:
            return False

    def HandleNextCall(self):
        request = self.database.GetNextRequest()
        response = requests.get(request.url)
        if response.status_code == 200:
            responseDict = json.loads(response.text)
            self.database.DeleteRequest(request.requestId)
            if (request.callType == DataClasses.Request.callType.getSummonersByName.value):
                self.database.AddRequestStatus(request.requestId, 1)
                for summonerName in responseDict:
                    self.database.InsertUpdateSummoner(responseDict[summonerName])
            elif (request.callType == DataClasses.Request.callType.getRecentGamesBySummoner.value):
                self.database.AddRequestStatus(request.requestId, 1)
                for game in responseDict["games"]:
                    game["summonerId"] = responseDict["summonerId"]
                    self.database.InsertGame(game)
            else:
                raise ValueError('Unknown CallType: {0}'.format(request.callType))
        elif response.status_code == 429:
            self.nextRequestTime = datetime.datetime.now() + datetime.timedelta(0,response.headers.get("Retry-After", 1))
        elif response.status_code == 404:
            self.database.AddRequestStatus(request.requestId, 0)
            print('ApiConnection: 404 from Riot API (probably specified invalid summoner name) deleting request')
            self.database.DeleteRequest(request.requestId)
        else:
            self.database.AddRequestStatus(request.requestId, 0)
            print('ApiConnection: Unhandled Status Code ({0}) from Riot API, deleting the following request to continue execution:'.format(response.status_code))
            request.Print()



