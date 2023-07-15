import requests 
import pandas as pd
import json
from player import Player
from payloads import *
import seaborn as sns
import matplotlib.pyplot as plt

class NBAScraper:
    
    def __init__(self):
        self.players = None
        self.teamIDs = None
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
           "Referer": 'https://www.nba.com/'}
        self.init_players()
        self.init_teams()
        


    def init_players(self):
        url = "https://stats.nba.com/stats/leaguedashplayerstats"
        self.players = {}
        jsonData = requests.get(url, headers=self.headers, params=init_players_payload).json()
        rows = jsonData['resultSets'][0]['rowSet']
        columns = jsonData['resultSets'][0]['headers']
        df = pd.DataFrame(rows, columns=columns)[['PLAYER_ID', 'PLAYER_NAME']]
        for row in rows:
            self.players[row[1]] = row[0]

    def init_teams(self):
        url = "https://stats.nba.com/stats/leaguedashteamstats"
        self.teamIDs = {}
        jsonData = requests.get(url, headers=self.headers, params=init_teams_payload).json()
        rows = jsonData['resultSets'][0]['rowSet']
        columns = jsonData['resultSets'][0]['headers']
        df = pd.DataFrame(rows, columns=columns)[['TEAM_ID', 'TEAM_NAME']]
        for row in rows:
            self.teamIDs[row[1]] = row[0]            

    def get_player_stats(self, playerName):
        url = "https://stats.nba.com/stats/playerdashboardbyyearoveryearcombined"
        jsonData = requests.get(url, headers=self.headers, params=player_payload(self.players[playerName])).json()
        rows = jsonData['resultSets'][5]['rowSet']
        columns = jsonData['resultSets'][5]['headers']

        df = pd.DataFrame(rows, columns=columns)[["GROUP_VALUE", "TEAM_ID", "TEAM_ABBREVIATION", "GP", "W", "L", "W_PCT", "MIN", "FGM", "FGA", "FG_PCT", "FG3M", "FG3A", "FG3_PCT", "FTM", "FTA", "FT_PCT", "OREB", "DREB", "REB", "AST", "TOV", "STL", "BLK", "BLKA", "PF", "PFD", "PTS", "PLUS_MINUS"]]
        # sns.set_theme()
        # # sns.lineplot( x=df['GROUP_VALUE'], y=df['PTS'])
        # sns.lineplot(data=df, x="GROUP_VALUE", y='FGM')
        # plt.show()
        return Player(df)
    
    def get_gamelog(self, team_name):
        url = "https://stats.nba.com/stats/teamgamelogs"
        jsonData = requests.get(url, headers=self.headers, params=team_history_payload(self.teamIDs[team_name], "Base")).json()
        rows = jsonData['resultSets'][0]['rowSet']
        columns = jsonData['resultSets'][0]['headers']
        df = pd.DataFrame(rows, columns=columns)

        jsonData = requests.get(url, headers=self.headers, params=team_history_payload(self.teamIDs[team_name], "Advanced")).json()
        rows = jsonData['resultSets'][0]['rowSet']
        columns = jsonData['resultSets'][0]['headers']
        df2 = pd.DataFrame(rows, columns=columns)

        jsonData = requests.get(url, headers=self.headers, params=team_history_payload(self.teamIDs[team_name], "Scoring")).json()
        rows = jsonData['resultSets'][0]['rowSet']
        columns = jsonData['resultSets'][0]['headers']
        df3 = pd.DataFrame(rows, columns=columns)

        jsonData = requests.get(url, headers=self.headers, params=team_history_payload(self.teamIDs[team_name], "Four Factors")).json()
        rows = jsonData['resultSets'][0]['rowSet']
        columns = jsonData['resultSets'][0]['headers']
        df4 = pd.DataFrame(rows, columns=columns)

        jsonData = requests.get(url, headers=self.headers, params=team_history_payload(self.teamIDs[team_name], "Misc")).json()
        rows = jsonData['resultSets'][0]['rowSet']
        columns = jsonData['resultSets'][0]['headers']
        df4 = pd.DataFrame(rows, columns=columns)
        game_data = df.merge(df2.merge(df3.merge(df4))).sort_values("GAME_DATE")

        return game_data.reset_index(drop=True)
        



scraper = NBAScraper()
curry = scraper.get_player_stats("Stephen Curry")
# print(curry.get_season_stats(14))
heat_log = scraper.get_gamelog("Miami Heat")


opponents = []
arena = []
for matchup in heat_log.MATCHUP:
    data = matchup.split()
    opponents.append(data[-1])
    if '@' in data:
        arena.append(data[-1])
        # print("Away Game")
    else:
        arena.append(data[0])
        # print("Home Game")
heat_log['MATCHUP'] = opponents
heat_log['ARENA'] = arena


heat_log['target'] = heat_log['WL'].shift(-1)
heat_log['target'][pd.isnull(heat_log['target'])] = "-"
heat_log['target'] = heat_log['target'].astype('category').cat.codes
heat_log = heat_log.drop(['TEAM_ID', 'TEAM_NAME'], axis=1)
print(heat_log)
