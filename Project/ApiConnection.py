from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

import http.client
import json
import time
import datetime
import DataClasses

class ApiConnection:
    def __init__(self, database):
        self.database = database
        self.nextRequestTime = datetime.datetime.now()


    def EmptyQueue(self):
        while True:
            if self.database.GetNextRequest() is None:
                print("Request Queue is Empty")
                break
            if self.nextRequestTime < datetime.datetime.now():
                print('Sending Request - Request Count: ' + str(self.database.GetRequestQueueCount()))
                self.HandleNextCall()
                time.sleep(1)
            else:
                print('Sleeping - Request Count: ' + str(self.database.GetRequestQueueCount()))
                time.sleep(1)

    def VerifyKey(self, key):
        connection = http.client.HTTPSConnection('na.api.pvp.net')
        headers = {'Content-type': 'application/json'}
        connection.request('GET', '/api/lol/na/v1.2/champion/1?api_key={0}'.format(key), "", headers)
        response = connection.getresponse()
        if response.status == 200:
            return True
        else:
            return False

    def HandleNextCall(self):
        call = self.database.GetNextRequest()
        connection = http.client.HTTPSConnection(call.domain)
        headers = {'Content-type': 'application/json'}
        connection.request('GET',call.path, "", headers)
        response = connection.getresponse()
        if response.status == 200:
            responseDict = json.loads(response.read().decode('utf-8'))
            self.database.DeleteRequest(call.requestId)
            if (call.callType == DataClasses.Request.callType.getSummonersByName.value):
                for summonerName in responseDict:
                    self.database.InsertUpdateSummoner(responseDict[summonerName])
            elif (call.callType == DataClasses.Request.callType.getRecentGamesBySummoner.value):
                for game in responseDict["games"]:
                    game["summonerId"] = responseDict["summonerId"]
                    self.database.InsertGame(game)
            else:
                raise ValueError('Unknown CallType: {0}'.format(call.callType))
        if response.status == 429:
            self.nextRequestTime = datetime.datetime.now() + datetime.timedelta(0,response.getheader("Retry-After", 1))
        if response.status != 200:
            self.database.AddRequest(call.priority, call.domain, call.path, call.callType)

