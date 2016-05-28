import datetime
from pprint import pprint

class Summoner:
    def __init__(self, record):
        self.SummonerId = record[0]
        self.Name = record[1]
        self.ProfileIconId = record[2]
        self.RevisionDate = datetime.datetime.fromtimestamp(record[3]/1000)
        self.Level = record[4]
        self.LastUpdatedDate = record[5]

    def Print(self):
        pprint (vars(self))

class Participant:
    def __init__(self, record):
        self.GameId = record[0]
        self.SummonerId = record[1]
        self.TeamId = record[2]
        self.ChampionId = record[3]
        self.Win = record[4]

    def Print(self):
        pprint (vars(self))

class Game:
    def __init__(self, record):
        self.SummonerId = record[0]
        self.ChampionId = record[1]
        self.CreateDate = datetime.datetime.fromtimestamp(record[2]/1000)
        self.GameId = record[3]
        self.GameMode = record[4]
        self.GameType = record[5]
        self.Invalid = record[6]
        self.IpEarned = record[7]
        self.SummonerLevel = record[8]
        self.MapId = record[9]
        self.Spell1 = record[10]
        self.Spell2 = record[11]
        self.SubType = record[12]
        self.TeamId = record[13]
        self.Assists = record[14]
        self.BarracksKilled = record[15]
        self.BountyLevel = record[16]
        self.ChampionsKilled = record[17]
        self.CombatPlayerScore = record[18]
        self.ConsumablesPurchased = record[19]
        self.DamageDealtPlayer = record[20]
        self.DoubleKills = record[21]
        self.FirstBlood = record[22]
        self.Gold = record[23]
        self.GoldEarned = record[24]
        self.GoldSpent = record[25]
        self.Item0 = record[26]
        self.Item1 = record[27]
        self.Item2 = record[28]
        self.Item3 = record[29]
        self.Item4 = record[30]
        self.Item5 = record[31]
        self.Item6 = record[32]
        self.ItemsPurchased = record[33]
        self.KillingSprees = record[34]
        self.LargestCriticalStrike = record[35]
        self.LargestKillingSpree = record[36]
        self.LargestMultiKill = record[37]
        self.LegendaryItemsCreated = record[38]
        self.ChampionLevel = record[39]
        self.MagicDamageDealtPlayer = record[40]
        self.MagicDamageDealtToChampions = record[41]
        self.MagicDamageTaken = record[42]
        self.MinionsDenied = record[43]
        self.MinionsKilled = record[44]
        self.NeutralMinionsKilled = record[45]
        self.NeutralMinionsKilledEnemyJungle = record[46]
        self.NeutralMinionsKilledYourJungle = record[47]
        self.NexusKilled = record[48]
        self.NodeCapture = record[49]
        self.NodeCaptureAssist = record[50]
        self.NodeNeutralize = record[51]
        self.NodeNeutralizeAssist = record[52]
        self.NumDeaths = record[53]
        self.NumItemsBought  = record[54]
        self.ObjectivePlayerScore = record[55]
        self.PentaKills = record[56]
        self.PhysicalDamageDealtPlayer = record[57]
        self.PhysicalDamageDealtToChampions = record[58]
        self.PhysicalDamageTaken = record[59]
        self.PlayerPosition = record[60]
        self.PlayerRole = record[61]
        self.PlayerScore0 = record[62]
        self.PlayerScore1 = record[63]
        self.PlayerScore2 = record[64]
        self.PlayerScore3 = record[65]
        self.PlayerScore4 = record[66]
        self.PlayerScore5 = record[67]
        self.PlayerScore6 = record[68]
        self.PlayerScore7 = record[69]
        self.PlayerScore8 = record[70]
        self.PlayerScore9 = record[71]
        self.QuadraKills = record[72]
        self.SightWardsBought = record[73]
        self.Spell1Cast = record[74]
        self.Spell2Cast = record[75]
        self.Spell3Cast = record[76]
        self.Spell4Cast = record[77]
        self.SummonSpell1Cast = record[78]
        self.SummonSpell2Cast = record[79]
        self.SuperMonsterKilled = record[80]
        self.Team  = record[81]
        self.TeamObjective = record[82]
        self.TimePlayed = record[83]
        self.TotalDamageDealt = record[84]
        self.TotalDamageDealtToChampions = record[85]
        self.TotalDamageTaken = record[86]
        self.TotalHeal  = record[87]
        self.TotalPlayerScore = record[88]
        self.TotalScoreRank = record[89]
        self.TotalTimeCrowdControlDealt = record[90]
        self.TotalUnitsHealed = record[91]
        self.TripleKills = record[92]
        self.TrueDamageDealtPlayer = record[93]
        self.TrueDamageDealtToChampions = record[94]
        self.TrueDamageTaken = record[95]
        self.TurretsKilled = record[96]
        self.UnrealKills = record[97]
        self.VictoryPointTotal = record[98]
        self.VisionWardsBought = record[99]
        self.WardKilled = record[100]
        self.WardPlaced = record[101]
        self.Win = record[102]

    def Print(self):
        pprint (vars(self))