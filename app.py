import requests 
import pandas as pd
import json
from player import Player
import seaborn as sns
import matplotlib.pyplot as plt

class Scraper:
    
    def __init__(self):
        url = "https://stats.nba.com/stats/leaguedashplayerstats"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
           "Referer": 'https://www.nba.com/'}
        payload = {
            "MeasureType": "Base",
            "PerMode": "PerGame",
            "PlusMinus": "N",
            "PaceAdjust": "N",
            "Rank": "N",
            "LeagueID": "00",
            "Season": "2022-23",
            "SeasonType": "Regular Season",
            "PORound": 0,
            "Outcome": None,
            "Location": None,
            "Month": 0,
            "SeasonSegment": None,
            "DateFrom": None,
            "DateTo": None,
            "OpponentTeamID": 0,
            "VsConference": None,
            "VsDivision": None,
            "TeamID": 0,
            "Conference": None,
            "Division": None,
            "GameSegment": None,
            "Period": 0,
            "ShotClockRange": None,
            "LastNGames": 0,
            "GameScope": None,
            "PlayerExperience": None,
            "PlayerPosition": None,
            "StarterBench": None,
            "DraftYear": None,
            "DraftPick": None,
            "College": None,
            "Country": None,
            "Height": None,
            "Weight": None,
            "TwoWay": None,
            "GameSubtype": None,
            "ActiveRoster": None
        }
        self.players = {}
        jsonData = requests.get(url, headers=headers, params=payload).json()
        rows = jsonData['resultSets'][0]['rowSet']
        columns = jsonData['resultSets'][0]['headers']
        df = pd.DataFrame(rows, columns=columns)[['PLAYER_ID', 'PLAYER_NAME']]
        for row in rows:
            self.players[row[1]] = row[0]
            

    def getstats(self, playerName):
        url = "https://stats.nba.com/stats/playerdashboardbyyearoveryearcombined"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
           "Referer": 'https://www.nba.com/'}
        payload = {
        "PerMode": "PerGame",
        "PlusMinus": "N",
        "PaceAdjust": "N",
        "Rank": "N",
        "LeagueID": "00",
        "Season": "2022-23",
        "SeasonType": "Regular Season",
        "PORound": 0,
        "PlayerID": {self.players[playerName]},
        "Outcome": None,
        "Location": None,
        "Month": 0,
        "SeasonSegment": None,
        "DateFrom": None,
        "DateTo": None,
        "OpponentTeamID": 0,
        "VsConference": None,
        "VsDivision": None,
        "GameSegment": None,
        "Period": 0,
        "ShotClockRange": None,
        "LastNGames": 0
        }
        
        jsonData = requests.get(url, headers=headers, params=payload).json()

        rows = jsonData['resultSets'][5]['rowSet']
        columns = jsonData['resultSets'][5]['headers']

        df = pd.DataFrame(rows, columns=columns)[[
                "GROUP_VALUE",
                "TEAM_ID",
                "TEAM_ABBREVIATION",
                "GP",
                "W",
                "L",
                "W_PCT",
                "MIN",
                "FGM",
                "FGA",
                "FG_PCT",
                "FG3M",
                "FG3A",
                "FG3_PCT",
                "FTM",
                "FTA",
                "FT_PCT",
                "OREB",
                "DREB",
                "REB",
                "AST",
                "TOV",
                "STL",
                "BLK",
                "BLKA",
                "PF",
                "PFD",
                "PTS",
                "PLUS_MINUS"]]
        print(df)
        sns.set_theme()
        sns.lineplot( x=df['GROUP_VALUE'], y=df['PTS'])
        plt.show()
        return Player(df)



scraper = Scraper()
scraper.getstats("Stephen Curry")