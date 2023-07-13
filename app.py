import requests 
import pandas as pd
import json



class Scraper:
    
    def __init__(self):
        self.url = "https://stats.nba.com/stats/playerdashboardbyyearoveryearcombined"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
           "Referer": 'https://www.nba.com/'}
        self.payload = {
        "PerMode": "PerGame",
        "PlusMinus": "N",
        "PaceAdjust": "N",
        "Rank": "N",
        "LeagueID": "00",
        "Season": "2022-23",
        "SeasonType": "Regular Season",
        "PORound": 0,
        "PlayerID": 201939,
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

    def getstats(self):
        jsonData = requests.get(self.url, headers=self.headers, params=self.payload).json()

        rows = jsonData['resultSets'][0]['rowSet']
        columns = jsonData['resultSets'][0]['headers']

        df = pd.DataFrame(rows, columns=columns)
        print(df['GP'])


scraper = Scraper()
scraper.getstats()