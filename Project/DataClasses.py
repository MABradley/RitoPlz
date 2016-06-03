from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

import datetime
from pprint import pprint
from enum import Enum

class Summoner:
    def __init__(self, record):
        self.summonerId = record[0]
        self.name = record[1]
        self.profileIconId = record[2]
        self.revisionDate = datetime.datetime.fromtimestamp(record[3] / 1000)
        self.level = record[4]
        self.lastUpdatedDate = record[5]

    def Print(self):
        pprint(vars(self))

class Player:
    def __init__(self, record):
        self.gameId = record[0]
        self.summonerId = record[1]
        self.teamId = record[2]
        self.championId = record[3]
        self.win = record[4] == "True"

    def Print(self):
        pprint(vars(self))

class Champion:
    def __init__(self, record):
        self.championId = record[0]
        self.name = record[1]
        self.key = record[2]
        self.title = record[3]

    def Print(self):
        pprint(vars(self))

class Request:
    def __init__(self, record):
        self.requestId = record[0]
        self.priority = record[1]
        self.url = record[2]
        self.callType = record[3]

    def Print(self):
        pprint(vars(self))

    class callType(Enum):
        getSummonersByName = 0
        getRecentGamesBySummoner = 1

class Game:
    def __init__(self, record):
        self.summonerId = record[0]
        self.championId = record[1]
        self.createDate = datetime.datetime.fromtimestamp(record[2] / 1000)
        self.gameId = record[3]
        self.gameMode = record[4]
        self.gameType = record[5]
        self.invalid = record[6]
        self.ipEarned = record[7]
        self.summonerLevel = record[8]
        self.mapId = record[9]
        self.spell1 = record[10]
        self.spell2 = record[11]
        self.subType = record[12]
        self.teamId = record[13]
        self.assists = record[14]
        self.barracksKilled = record[15]
        self.bountyLevel = record[16]
        self.championsKilled = record[17]
        self.combatPlayerScore = record[18]
        self.consumablesPurchased = record[19]
        self.damageDealtPlayer = record[20]
        self.doubleKills = record[21]
        self.firstBlood = record[22]
        self.gold = record[23]
        self.goldEarned = record[24]
        self.goldSpent = record[25]
        self.item0 = record[26]
        self.item1 = record[27]
        self.item2 = record[28]
        self.item3 = record[29]
        self.item4 = record[30]
        self.item5 = record[31]
        self.item6 = record[32]
        self.itemsPurchased = record[33]
        self.killingSprees = record[34]
        self.largestCriticalStrike = record[35]
        self.largestKillingSpree = record[36]
        self.largestMultiKill = record[37]
        self.legendaryItemsCreated = record[38]
        self.championLevel = record[39]
        self.magicDamageDealtPlayer = record[40]
        self.magicDamageDealtToChampions = record[41]
        self.magicDamageTaken = record[42]
        self.minionsDenied = record[43]
        self.minionsKilled = record[44]
        self.neutralMinionsKilled = record[45]
        self.neutralMinionsKilledEnemyJungle = record[46]
        self.neutralMinionsKilledYourJungle = record[47]
        self.nexusKilled = record[48]
        self.nodeCapture = record[49]
        self.nodeCaptureAssist = record[50]
        self.nodeNeutralize = record[51]
        self.nodeNeutralizeAssist = record[52]
        self.numDeaths = record[53]
        self.numItemsBought  = record[54]
        self.objectivePlayerScore = record[55]
        self.pentaKills = record[56]
        self.physicalDamageDealtPlayer = record[57]
        self.physicalDamageDealtToChampions = record[58]
        self.physicalDamageTaken = record[59]
        self.playerPosition = record[60]
        self.playerRole = record[61]
        self.playerScore0 = record[62]
        self.playerScore1 = record[63]
        self.playerScore2 = record[64]
        self.playerScore3 = record[65]
        self.playerScore4 = record[66]
        self.playerScore5 = record[67]
        self.playerScore6 = record[68]
        self.playerScore7 = record[69]
        self.playerScore8 = record[70]
        self.playerScore9 = record[71]
        self.quadraKills = record[72]
        self.sightWardsBought = record[73]
        self.spell1Cast = record[74]
        self.spell2Cast = record[75]
        self.spell3Cast = record[76]
        self.spell4Cast = record[77]
        self.summonSpell1Cast = record[78]
        self.summonSpell2Cast = record[79]
        self.superMonsterKilled = record[80]
        self.team  = record[81]
        self.teamObjective = record[82]
        self.timePlayed = record[83]
        self.totalDamageDealt = record[84]
        self.totalDamageDealtToChampions = record[85]
        self.totalDamageTaken = record[86]
        self.totalHeal  = record[87]
        self.totalPlayerScore = record[88]
        self.totalScoreRank = record[89]
        self.totalTimeCrowdControlDealt = record[90]
        self.totalUnitsHealed = record[91]
        self.tripleKills = record[92]
        self.trueDamageDealtPlayer = record[93]
        self.trueDamageDealtToChampions = record[94]
        self.trueDamageTaken = record[95]
        self.turretsKilled = record[96]
        self.unrealKills = record[97]
        self.victoryPointTotal = record[98]
        self.visionWardsBought = record[99]
        self.wardKilled = record[100]
        self.wardPlaced = record[101]
        self.win = record[102] == "True"

    def Print(self):
        pprint(vars(self))

class GameFilter:
    def __init__(self):
        # Ints
        self.summonerId = None
        self.championId = None
        self.gameId = None
        # Bools
        self.win = None
        # Formatted strings representing int collections ie. '(123, 456)'
        self.summonerIdsStr = None
        self.championIdsStr = None
        self.gameIdsStr = None

    # Only called by GetWhereClause, helper for formatting
    def AndOrSpace(self):
        if self.hasFirstCondition:
            return " AND "
        else:
            self.hasFirstCondition = True
            return " "
    
    def GetWhereClause(self):
        whereClause = "WHERE"
        self.hasFirstCondition = False
        if self.summonerId is not None:
            whereClause += self.AndOrSpace() + "summonerId = {0}".format(self.summonerId)
        if self.championId is not None:
            whereClause += self.AndOrSpace() + "championId = {0}".format(self.championId)
        if self.gameId is not None:
            whereClause += self.AndOrSpace() + "gameId = {0}".format(self.gameId)
        if self.win is not None:
            whereClause += self.AndOrSpace() + "win = {0}".format(self.win)
        if self.summonerIdsStr is not None:
            whereClause += self.AndOrSpace() + "summonerId in {0}".format(self.summonerIdsStr)
        if self.championIdsStr is not None:
            whereClause += self.AndOrSpace() + "championId in {0}".format(self.championIdsStr)
        if self.gameIdsStr is not None:
            whereClause += self.AndOrSpace() + "gameId in {0}".format(self.gameIdsStr)
        if not self.hasFirstCondition:
            return ""
        return whereClause

class SummonerFilter:
    def __init__(self):
        # Ints
        self.summonerId = None
        # Strings
        self.summonerName = None
        # Formatted strings representing collections ie. '(123, 456)'
        self.summonerIdsStr = None
        self.summonerNamesStr = None

    # Only called by GetWhereClause, helper for formatting
    def AndOrSpace(self):
        if self.hasFirstCondition:
            return " AND "
        else:
            self.hasFirstCondition = True
            return " "

    def GetWhereClause(self):
        whereClause = "WHERE"
        self.hasFirstCondition = False
        if self.summonerId is not None:
            whereClause += self.AndOrSpace() + "summonerId = {0}".format(self.summonerId)
        if self.summonerIdsStr is not None:
            whereClause += self.AndOrSpace() + "summonerId in {0}".format(self.summonerIdsStr)
        if self.summonerNamesStr is not None:
            whereClause += self.AndOrSpace() + "name in {0} COLLATE NOCASE".format(self.summonerNamesStr)
        if self.summonerName is not None:
            whereClause += self.AndOrSpace() + "name = '{0}' COLLATE NOCASE".format(self.summonerName)
        if not self.hasFirstCondition:
            return ""
        #print("WhereClause: " + whereClause)
        return whereClause
            