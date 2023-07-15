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
        modes = ["Base", "Advanced", "Scoring", "Four Factors"]
        df = None
        for mode in modes:
            jsonData = requests.get(url, headers=self.headers, params=team_history_payload(self.teamIDs[team_name], mode)).json()
            rows = jsonData['resultSets'][0]['rowSet']
            columns = jsonData['resultSets'][0]['headers']
            if(mode == "Base"):
                df = pd.DataFrame(rows, columns=columns)
                continue
            df = df.merge(pd.DataFrame(rows, columns=columns))

        df.sort_values("GAME_DATE")
        return df.reset_index(drop=True)
    
    def get_years_played(self, player_name):
        url = "https://stats.nba.com/stats/playercareerstats"
        jsonData = requests.get(url, headers=self.headers, params=year_played_payload(self.players[player_name])).json()
        return sorted(list(set([season[1] for season in jsonData['resultSets'][0]['rowSet']])))
    
    def get_advanced_player_stats(self, player_name):
        url = 'https://stats.nba.com/stats/playergamelogs'
        # ['Base', 'Usage', 'Scoring', 'Advanced', 'Misc']
        measures = ['Base', 'Advanced', 'Usage', 'Scoring']
        seasondfs = []
        years_played = self.get_years_played(player_name)
        if(len(years_played) >= 4):
            years_played = years_played[-3:]
        for season in years_played:
            measuredfs = []
            for measure in measures:
                jsonData = requests.get(url, headers=self.headers, params=advanced_payload(self.players[player_name], measure, season)).json()
                rows = jsonData['resultSets'][0]['rowSet']
                columns = jsonData['resultSets'][0]['headers']
                measuredfs.append(pd.DataFrame(rows, columns=columns))
            seasondfs.append(pd.concat(measuredfs, axis=1))
        df = pd.concat(seasondfs, axis=0)
        df = df.loc[:,~df.columns.duplicated()].copy().drop(['PLAYER_NAME', 'PLAYER_ID', 'NICKNAME', 'TEAM_ID', 'TEAM_NAME', 'GAME_ID'], axis=1).sort_values("GAME_DATE").reset_index(drop=True)
        df['OPPONENT'] = [matchup.split()[-1] for matchup in df.MATCHUP]
        df['HOME'] = [False if "@" in x.split() else True for x in df.MATCHUP]
        return df
        


if __name__ == "__main__":
    scraper = NBAScraper()
    # curry = scraper.get_player_stats("Stephen Curry")
    # print(curry.get_season_stats(14))

    butler = scraper.get_advanced_player_stats("Jimmy Butler")
    butler.to_csv('out.csv')
    


