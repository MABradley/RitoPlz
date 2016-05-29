from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

import sqlite3
import datetime
import DataClasses

class Database:
    def __init__(self, databaseName):
        self.conn = sqlite3.connect(databaseName)
        self.cursor = self.conn.cursor()
        
        # Drop Table for Schema Changes
        self.cursor.execute('''DROP TABLE Requests''')
    
        # Create Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Summoners
                     (summonerId int unique, name text, profileIconId int, revisionDate date, summonerLevel int, lastUpdated date)''')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Keys (key text unique)')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Games
                      (summonerId int, championId int, createDate date, gameId int, gameMode text, gameType text, invalid bit, ipEarned int, summonerLevel int, mapId int, spell1 int, spell2 int, subType text, teamId int,\
                      assists int, barracksKilled int, bountyLevel int, championsKilled int, combatPlayerScore int, consumablesPurchased int, damageDealtPlayer int, doubleKills int, firstBlood int, gold int, goldEarned int, goldSpent int, item0 int, item1 int, item2 int, item3 int, item4 int, item5 int, item6 int,\
                      itemsPurchased int, killingSprees int, largestCriticalStrike int, largestKillingSpree int, largestMultiKill int, legendaryItemsCreated int, championLevel int, magicDamageDealtPlayer int,\
                      magicDamageDealtToChampions int, magicDamageTaken int, minionsDenied int, minionsKilled int, neutralMinionsKilled int, neutralMinionsKilledEnemyJungle int, neutralMinionsKilledYourJungle int, nexusKilled bit,\
                      nodeCapture int, nodeCaptureAssist int, nodeNeutralize int, nodeNeutralizeAssist int, numDeaths int, numItemsBought int, objectivePlayerScore int, pentaKills int, physicalDamageDealtPlayer int, physicalDamageDealtToChampions int,\
                      physicalDamageTaken int, playerPosition int, playerRole int, playerScore0 int, playerScore1 int, playerScore2 int, playerScore3 int, playerScore4 int, playerScore5 int, playerScore6 int, playerScore7 int, playerScore8 int, playerScore9 int,\
                      quadraKills int, sightWardsBought int, spell1Cast int, spell2Cast int, spell3Cast int, spell4Cast int, summonSpell1Cast int, summonSpell2Cast int, superMonsterKilled int, team int, teamObjective int, timePlayed int, totalDamageDealt int, totalDamageDealtToChampions int, totalDamageTaken int,\
                      totalHeal int, totalPlayerScore int, totalScoreRank int, totalTimeCrowdControlDealt int, totalUnitsHealed int, tripleKills int, trueDamageDealtPlayer int, trueDamageDealtToChampions int, trueDamageTaken int,\
                      turretsKilled int, unrealKills int, victoryPointTotal int, visionWardsBought int, wardKilled int, wardPlaced int, win bit)''')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Requests (requestId INTEGER PRIMARY KEY NOT NULL, priority int, domain text, path text, callType int)')
    
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Players (gameId int, summonerId int, teamId int, championId int, win bit, PRIMARY KEY (gameId, summonerId))')
    
        # Save (commit) the changes
        self.Commit()
        self.key = self.GetKey()

    def Commit(self):
        self.conn.commit()
        self.cursor = self.conn.cursor()
    
    def PrintSummoners(self):
        for row in self.cursor.execute('SELECT * FROM summoners ORDER BY summonerid'):
            DataClasses.Summoner(row).Print()
            
    def PrintSummoner(self, summonerId):
        for row in self.cursor.execute('SELECT * FROM summoners WHERE summonerId = {0}'.format(summonerId)):
            DataClasses.Summoner(row).Print()
            
    def PrintKey(self):
        for row in self.conn.execute('SELECT * FROM keys'):
            print(row)
            
    def PrintGames(self):
        for row in self.cursor.execute('Select * from games'):
            DataClasses.Game(row).Print()
            
    def PrintGame(self, gameId):
        for row in self.cursor.execute('SELECT * FROM games WHERE gameId = {0}'.format(gameId)):
            DataClasses.Game(row).Print()
            
    def PrintPlayers(self):
        for row in self.cursor.execute('select * from Players'):
            DataClasses.Player(row).Print()
            
    def PrintPlayer(self, gameId, summonerId):
         for row in self.cursor.execute('SELECT * FROM Players WHERE gameId = {0} AND summonerId = {1}'.format(gameId, summonerId)):
            DataClasses.Player(row).Print()

    def PrintRequests(self):
        for row in self.cursor.execute('SELECT * FROM Requests ORDER BY priority DESC'):
            DataClasses.Request(row).Print()

    def SetKey(self, developerKey):
        self.cursor.execute('DELETE FROM keys')
        self.cursor.execute('''INSERT INTO keys (key) VALUES ('{0}')'''.format(developerKey))
        self.Commit()

    def GetKey(self):
        for row in self.cursor.execute('SELECT key FROM keys'):
            return row[0]
        return ""
    
    def DeleteSummoner(self, summonerId):
        self.cursor.execute('DELETE FROM summoners WHERE summonerId = {0}'.format(summonerId))
        self.Commit()
        
    def InsertGame(self, dict):
        stats = dict["stats"]
        self.cursor.execute('''INSERT OR REPLACE INTO Players (gameId, summonerId, championId, teamId, win) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')'''.format(dict["gameId"], dict["summonerId"], dict["championId"], dict["teamId"], stats["win"]))
        for row in dict["fellowPlayers"]:
            if row["teamId"] == dict["teamId"]:
                self.cursor.execute('''INSERT OR REPLACE INTO Players (gameId, summonerId, championId, teamId, win) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')'''.format(dict["gameId"], row["summonerId"], row["championId"], row["teamId"], stats["win"]))
            else:
                self.cursor.execute('''INSERT OR REPLACE INTO Players (gameId, summonerId, championId, teamId, win) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')'''.format(dict["gameId"], row["summonerId"], row["championId"], row["teamId"], not stats["win"]))
        #return if record exists, there won't be updates to these records
        for row in self.cursor.execute('''SELECT summonerId FROM games WHERE summonerId = {0} AND gameId = {1}'''.format(dict["summonerId"], dict["gameId"])):
            #print("Returned, GameId: {0}, SummonerId: {1}".format(dict["gameId"], summonerId))
            self.Commit()
            return
        #print("Didn't Return, GameId: {0}, SummonerId: {1}".format(dict["gameId"], summonerId))
        self.cursor.execute('''INSERT INTO games\
                      (summonerId, championId, createDate, gameId, gameMode, gameType, invalid, ipEarned, summonerLevel, mapId, spell1, spell2, subType, teamId,\
                      assists, barracksKilled, bountyLevel, championsKilled, combatPlayerScore, consumablesPurchased, damageDealtPlayer, doubleKills, firstBlood, gold, goldEarned, goldSpent, item0, item1, item2, item3, item4, item5, item6,\
                      itemsPurchased, killingSprees, largestCriticalStrike, largestKillingSpree, largestMultiKill, legendaryItemsCreated, championLevel, magicDamageDealtPlayer,\
                      magicDamageDealtToChampions, magicDamageTaken, minionsDenied, minionsKilled, neutralMinionsKilled, neutralMinionsKilledEnemyJungle, neutralMinionsKilledYourJungle, nexusKilled,\
                      nodeCapture, nodeCaptureAssist, nodeNeutralize, nodeNeutralizeAssist, numDeaths, numItemsBought, objectivePlayerScore, pentaKills, physicalDamageDealtPlayer, physicalDamageDealtToChampions,\
                      physicalDamageTaken, playerPosition, playerRole, playerScore0, playerScore1, playerScore2, playerScore3, playerScore4, playerScore5, playerScore6, playerScore7, playerScore8, playerScore9,\
                      quadraKills, sightWardsBought, spell1Cast, spell2Cast, spell3Cast, spell4Cast, summonSpell1Cast, summonSpell2Cast, superMonsterKilled, team, teamObjective, timePlayed, totalDamageDealt, totalDamageDealtToChampions, totalDamageTaken,\
                      totalHeal, totalPlayerScore, totalScoreRank, totalTimeCrowdControlDealt, totalUnitsHealed, tripleKills, trueDamageDealtPlayer, trueDamageDealtToChampions, trueDamageTaken,\
                      turretsKilled, unrealKills, victoryPointTotal, visionWardsBought, wardKilled, wardPlaced, win) values\
                      ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}',\
                      '{14}','{15}','{16}','{17}','{18}','{19}','{20}','{21}','{22}','{23}','{24}','{25}','{26}','{27}','{28}','{29}','{30}','{31}','{32}',\
                      '{33}','{34}','{35}','{36}','{37}','{38}','{39}','{40}',\
                      '{41}','{42}','{43}','{44}','{45}','{46}','{47}','{48}',\
                      '{49}','{50}','{51}','{52}','{53}','{54}','{55}','{56}','{57}','{58}',\
                      '{59}','{60}','{61}','{62}','{63}','{64}','{65}','{66}','{67}','{68}','{69}','{70}','{71}',\
                      '{72}','{73}','{74}','{75}','{76}','{77}','{78}','{79}','{80}','{81}','{82}','{83}','{84}','{85}','{86}',\
                      '{87}','{88}','{89}','{90}','{91}','{92}','{93}','{94}','{95}',\
                      '{96}','{97}','{98}','{99}','{100}','{101}','{102}')'''.format(\
                      dict["summonerId"], dict["championId"],dict["createDate"],dict["gameId"],dict["gameMode"],dict["gameType"],dict["invalid"],dict["ipEarned"],dict["level"],dict["mapId"],dict["spell1"],dict["spell2"],dict["subType"],dict["teamId"],\
                      stats.get("assists", '0'),stats.get("barracksKilled", '0'),stats.get("bountyLevel", '0'),stats.get("championsKilled", '0'),stats.get("combatPlayerScore", '0'),stats.get("consumablesPurchased", '0'),stats.get("damageDealtPlayer", '0'),stats.get("doubleKills", '0'),stats.get("firstBlood", '0'),stats.get("gold", '0'),stats.get("goldEarned", '0'),stats.get("goldSpent", '0'),stats.get("item0", '0'),stats.get("item1", '0') ,stats.get("item2", '0'),stats.get("item3", '0'),stats.get("item4", '0'),stats.get("item5", '0'),stats.get("item6", '0'),\
                      stats.get("itemsPurchased", '0'),stats.get("killingSprees", '0'),stats.get("largestCriticalStrike", '0'),stats.get("largestKillingSpree", '0'),stats.get("largestMultiKill", '0'),stats.get("legendaryItemsCreated", '0'),stats.get("level", '0'),stats.get("magicDamageDealtPlayer", '0'),\
                      stats.get("magicDamageDealtToChampions", '0'),stats.get("magicDamageTaken", '0'),stats.get("minionsDenied", '0'),stats.get("minionsKilled", '0'),stats.get("neutralMinionsKilled", '0'),stats.get("neutralMinionsKilledEnemyJungle", '0'),stats.get("neutralMinionsKilledYourJungle", '0'),stats.get("nexusKilled", '0'),\
                      stats.get("nodeCapture", '0'),stats.get("nodeCaptureAssist", '0'),stats.get("nodeNeutralize", '0'),stats.get("nodeNeutralizeAssist", '0'),stats.get("numDeaths", '0'),stats.get("numItemsBought", '0'),stats.get("objectivePlayerScore", '0'),stats.get("pentaKills", '0'),stats.get("physicalDamageDealtPlayer", '0'),stats.get("physicalDamageDealtToChampions", '0'),\
                      stats.get("physicalDamageTaken", '0'),stats.get("playerPosition", '0'),stats.get("playerRole", '0'),stats.get("playerScore0", '0'),stats.get("playerScore1", '0'),stats.get("playerScore2", '0'),stats.get("playerScore3", '0'),stats.get("playerScore4", '0'),stats.get("playerScore5", '0'),stats.get("playerScore6", '0'),stats.get("playerScore7", '0'),stats.get("playerScore8", '0'),stats.get("playerScore9", '0'),\
                      stats.get("quadraKills", '0'),stats.get("sightWardsBought", '0'),stats.get("spell1Cast", '0'),stats.get("spell2Cast", '0'),stats.get("spell3Cast", '0'),stats.get("spell4Cast", '0'),stats.get("summonSpell1Cast", '0'),stats.get("summonSpell2Cast", '0'),stats.get("superMonsterKilled", '0'),stats.get("team", '0'),stats.get("teamObjective", '0'),stats.get("timePlayed", '0'),stats.get("totalDamageDealt", '0'),stats.get("totalDamageDealtToChampions", '0'),stats.get("totalDamageTaken", '0'),\
                      stats.get("totalHeal", '0'),stats.get("totalPlayerScore", '0'),stats.get("totalScoreRank", '0'),stats.get("totalTimeCrowdControlDealt", '0'),stats.get("totalUnitsHealed", '0'),stats.get("tripleKills", '0'),stats.get("trueDamageDealtPlayer", '0'),stats.get("trueDamageDealtToChampions", '0'),stats.get("trueDamageTaken", '0'),\
                      stats.get("turretsKilled", '0'),stats.get("unrealKills", '0'),stats.get("victoryPointTotal", '0'),stats.get("visionWardsBought", '0'),stats.get("wardKilled", '0'),stats.get("wardPlaced", '0'),stats.get("win", '0')))
        self.Commit()

    # Inserts a new summoner with the data provided in dict, or replaces the old record if existing
    def InsertUpdateSummoner(self, dict):
        #print("InsertUpdateSummoner: SummonerId: {0}".format(dict["summonerId"]))
        # Debug loop
        #for i in dict:
        #    print(i, str(dict[i]))
        self.cursor.execute('''INSERT OR REPLACE INTO Summoners (summonerId, name, profileIconId, revisionDate, summonerLevel, lastUpdated) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}')'''.format(dict["id"], dict["name"], dict["profileIconId"], dict["revisionDate"], dict["summonerLevel"], datetime.datetime.now()))
        self.AddRequest(None, 'na.api.pvp.net','/api/lol/na/v1.3/game/by-summoner/{0}/recent?api_key={1}'.format(dict["id"], self.key), DataClasses.Request.callType.getRecentGamesBySummoner.value)
        self.Commit()

    def AddRequest(self, priority, name, path, callType):
        if priority is None:
            if self.GetNextRequest() is None:
                self.cursor.execute('''INSERT INTO Requests (priority, domain, path, callType) VALUES ({0},'{1}','{2}',{3})'''.format(1, name, path, callType))
            else:
                self.cursor.execute('''INSERT INTO Requests (priority, domain, path, callType) VALUES ({0},'{1}','{2}',{3})'''.format(self.GetNextRequest().priority + 1, name, path, callType))
        else:
            self.cursor.execute('''INSERT INTO Requests (priority, domain, path, callType) VALUES ({0},'{1}','{2}',{3})'''.format(priority, name, path, callType))

    def GetNextRequest(self):
        for row in self.cursor.execute('SELECT * FROM Requests ORDER BY priority DESC'):
            return DataClasses.Request(row)
        return None

    def GetRequestQueueCount(self):
        return len(self.cursor.execute('SELECT * FROM Requests').fetchall())

    def DeleteRequest(self, requestId):
        self.cursor.execute('DELETE FROM Requests WHERE requestId = {0}'.format(requestId))
        self.Commit()

    # Add a call for each summoner outdated by 1 day or more
    def CheckForOutdatedSummoners(self):
        names = ""
        for row in self.cursor.execute('''SELECT name, summonerId FROM summoners WHERE lastUpdated <= (SELECT DATE( 'now','-1 day'))'''):
            if len(names) < 1:
                names = row[0]
            else:
                names += "," + row[0]
        if len(names) > 0:
            print('Updating Summoners: ' + names)
            self.AddRequest(2, 'na.api.pvp.net', '/api/lol/na/v1.4/summoner/by-name/{0}?api_key={1}'.format(names, self.key), DataClasses.Request.callType.getSummonersByName.value)
        else:
            print('All Summoners Up To Date')

    def RequestSummoner(self, summonerName):
        self.AddRequest(None, 'na.api.pvp.net', '/api/lol/na/v1.4/summoner/by-name/{0}?api_key={1}'.format(summonerName, self.key), DataClasses.Request.callType.getSummonersByName.value)

    def RequestRecentGames(self, summonerId):
        self.AddRequest(None, 'na.api.pvp.net','/api/lol/na/v1.3/game/by-summoner/{0}/recent?api_key={1}'.format(summonerId, self.key), DataClasses.Request.callType.getRecentGamesBySummoner.value)