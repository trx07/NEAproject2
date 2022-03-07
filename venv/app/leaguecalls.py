import requests
import json
from app import routes

global matchcount
global apiKey
apiKey = "RGAPI-a864f4cb-9dfb-46cf-aa36-824a5609da17"  # make sure to update this key daily, it resets every 24hr, allows for api to work
matchcount = 5


class summonerInfo():  # player class
    def __init__(self, summonerName="null", summonerLevel=0, summonerPictureID=0, summonerRegion="euw1", summonerID="00000"):
        self.summonerName = summonerName
        self.summonerLevel = summonerLevel
        self.summonerPictureID = summonerPictureID
        self.summonerRegion = summonerRegion
        self.summonerID = summonerID

    def getSummonerName(self):
        return self.summonerName

    def getSummonerLevel(self):
        return self.summonerLevel

    def getSummonerPictureID(self):
        return self.summonerPictureID

    def getSummonerID(self):
        return self.summonerID

    def setSummonerName(self, name):
        self.summonerName = name

    def setSummonerLevel(self, sumLvl):
        self.summonerLevel = sumLvl

    def setSummonerPictureID(self, sumPicID):
        self.summonerPictureID = sumPicID

    def setSummonerID(self, sumID):
        self.summonerID = sumID


class requestSummoner():  # get smner detail
    def __init__(self, chosenSummoner):
        self.chosenSummoner = chosenSummoner
        self.responsejson = None

    def requestfunc(self):
        player_region = "euw1"
        summonerv4Base = f"https://{player_region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{self.chosenSummoner.getSummonerName()}?api_key={apiKey}"

        response = requests.get(summonerv4Base)
        response = response.json()
        self.responsejson = response

    def parseResponse(self):
        summonerName = self.responsejson['name']
        summonerLevel = self.responsejson['summonerLevel']
        summonerPictureID = self.responsejson['profileIconId']
        summonerID = self.responsejson['puuid']
        self.chosenSummoner.setSummonerName(summonerName)
        self.chosenSummoner.setSummonerLevel(summonerLevel)
        self.chosenSummoner.setSummonerPictureID(summonerPictureID)
        self.chosenSummoner.setSummonerID(summonerID)

    def getMatchHistory(self):
        print("initializing works")
        matchRegion = "europe"
        MatchV5Base = f"https://{matchRegion}.api.riotgames.com/lol/match/v5/matches/by-puuid/{self.chosenSummoner.getSummonerID()}/ids?start=0&count={matchcount}&api_key={apiKey}"
        matchList = requests.get(MatchV5Base)
        matchList = matchList.json()
        return matchList

    def getChosenSummoner(self):
        return self.chosenSummoner


class MatchInfo():
    def __init__(self, matchID):
        self.matchID = matchID
        self.matchResponse = None

    def getMatchInfo(self):
        matchRegion = "europe"
        MatchV5Base = f"https://{matchRegion}.api.riotgames.com/lol/match/v5/matches/{self.matchID}?api_key={apiKey}"
        matchResponse = requests.get(MatchV5Base)
        matchResponse = matchResponse.json()
        with open(f"{self.matchID}.json", 'w') as fp:
            json.dump(matchResponse, fp)
            print("stuff was saved")
            fp.close()
        self.matchResponse = matchResponse
        #return matchResponse

    def readMatchInfo(self):
        with open(f"{self.matchID}.json", 'r') as fp:
            data = fp.read()
            fp.close()
        matchResponse = data.json()
        matchResponse = matchResponse.dump()
        self.matchResponse = matchResponse

    def getMatchResponse(self):
        return self.matchResponse

class playerMatchData():
    def __init__(self, playerName, playerChamp, champLevel, champID, kills, deaths, assists, items, didWin, role):
        self.__playerName = playerName
        self.__playerChamp = playerChamp
        self.__champLevel = champLevel
        self.__champID = champID
        self.__kills = kills
        self.__deaths = deaths
        self.__assists = assists
        try:
            self.__KDA = (self.__kills+self.__assists)/self.__deaths
        except ZeroDivisionError:
            self.__KDA = kills
        self.__items = items
        self.__didWin = didWin
        self.__role = role

    def getPlayerName(self):
        return self.__playerName

    def getPlayerChamp(self):
        return self.__playerChamp

    def getChampLevel(self):
        return self.__champLevel

    def getChampID(self):
        return self.__champID
    
    def getKills(self):
        return self.__kills

    def getDeaths(self):
        return self.__deaths
    
    def getAssists(self):
        return self.__assists

    def getKDA(self):
        return self.__KDA

    def getItemList(self):
        return self.__items

    def getWinState(self):
        return self.__didWin

    def getRole(self):
        return self.__role

    def getItemAt(self,itemNumber):
        return self.__items[itemNumber]

    def getItemList(self):
        return self.__items
    
class PlayerManager():
    def __init__(self):
        self.__playerList = []

    def populatePlayerInfo(self,matchlist):
        for i in range(len(matchlist["info"]["participants"])):
            playerAssists = matchlist["info"]["participants"][i]["assists"]
            playerChampionLevel = matchlist["info"]["participants"][i]["champLevel"]
            playerchampion = matchlist["info"]["participants"][i]["championName"]
            playerchampionid = matchlist["info"]["participants"][i]["championId"]
            playerdeaths = matchlist["info"]["participants"][i]["deaths"]
            playerkills = matchlist["info"]["participants"][i]["kills"]
            playerrole = matchlist["info"]["participants"][i]["role"]
            playersummonername = matchlist["info"]["participants"][i]["summonerName"]
            playerwin = matchlist["info"]["participants"][i]["win"]
            items = []
            for x in range(6):
                items.append(matchlist["info"]["participants"][i]["item"+str(x)])
            
            self.__playerList.append(playerMatchData(playersummonername,playerchampion,playerChampionLevel,playerchampionid,playerkills,playerdeaths,playerAssists,items,playerwin,playerrole))

    def getPlayerAt(self, X):
        return self.__playerList[X]

    def getPlayerByName(self,Name):
        for player in self.__playerList:
            if Name == player.getPlayerName():
                return player
        return None

# keep this for later https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/l0k0oyKdYh8yVSOKobNr5iDbJ9Y9PRgKbxJOIl7YcIeihtaCzhK8HuVwhBW00wiAcrCDOaEqmVWKKQ/ids?start=0&count=20&api_key=RGAPI-5393e7e5-5fa8-495e-8fa8-07d2f9484413
