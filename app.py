import requests 
import pandas as pd
import json
from player import Player
from payloads import *
import seaborn as sns
import matplotlib.pyplot as plt

class Scraper:
    
    def __init__(self):
        self.players = None
        self.teams = None
        self.init_players()
        self.init_teams()


    def init_players(self):
        self.teams = {}
        url = "https://stats.nba.com/stats/leaguedashplayerstats"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
           "Referer": 'https://www.nba.com/'}
        self.players = {}
        jsonData = requests.get(url, headers=headers, params=init_players_payload).json()
        rows = jsonData['resultSets'][0]['rowSet']
        columns = jsonData['resultSets'][0]['headers']
        df = pd.DataFrame(rows, columns=columns)[['PLAYER_ID', 'PLAYER_NAME']]
        for row in rows:
            self.players[row[1]] = row[0]

    def init_teams(self):
        url = "https://stats.nba.com/stats/leaguedashteamstats"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
           "Referer": 'https://www.nba.com/'}
        self.teams = {}
        jsonData = requests.get(url, headers=headers, params=init_teams_payload).json()
        rows = jsonData['resultSets'][0]['rowSet']
        columns = jsonData['resultSets'][0]['headers']
        df = pd.DataFrame(rows, columns=columns)[['TEAM_ID', 'TEAM_NAME']]
        for row in rows:
            self.teams[row[1]] = row[0]

        print(self.teams)
            

    def get_player_stats(self, playerName):
        url = "https://stats.nba.com/stats/playerdashboardbyyearoveryearcombined"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
           "Referer": 'https://www.nba.com/'}
        
        jsonData = requests.get(url, headers=headers, params=player_payload(self.players[playerName])).json()
        rows = jsonData['resultSets'][5]['rowSet']
        columns = jsonData['resultSets'][5]['headers']

        df = pd.DataFrame(rows, columns=columns)[["GROUP_VALUE", "TEAM_ID", "TEAM_ABBREVIATION", "GP", "W", "L", "W_PCT", "MIN", "FGM", "FGA", "FG_PCT", "FG3M", "FG3A", "FG3_PCT", "FTM", "FTA", "FT_PCT", "OREB", "DREB", "REB", "AST", "TOV", "STL", "BLK", "BLKA", "PF", "PFD", "PTS", "PLUS_MINUS"]]
        # sns.set_theme()
        # # sns.lineplot( x=df['GROUP_VALUE'], y=df['PTS'])
        # sns.lineplot(data=df, x="GROUP_VALUE", y='FGM')
        # plt.show()
        return Player(df)
    
    def get_roster_info(self, team_name):
        return



scraper = Scraper()
curry = scraper.get_player_stats("Stephen Curry")
print(curry.get_season_stats(14))
