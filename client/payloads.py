init_players_payload = {
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

init_teams_payload = {
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
    "TwoWay": 0,
    "GameSubtype": None
    }


def player_payload(playerID):
    payload = {
        "PerMode": "PerGame",
        "PlusMinus": "N",
        "PaceAdjust": "N",
        "Rank": "N",
        "LeagueID": "00",
        "Season": "2022-23",
        "SeasonType": "Regular Season",
        "PORound": 0,
        "PlayerID": f"{playerID}",
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
    return payload

def team_payload(playerID):
    payload = {
        "PerMode": "PerGame",
        "PlusMinus": "N",
        "PaceAdjust": "N",
        "Rank": "N",
        "LeagueID": "00",
        "Season": "2022-23",
        "SeasonType": "Regular Season",
        "PORound": 0,
        "PlayerID": f"",
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
    return payload

def team_history_payload(teamID, measure_type):
    payload = {
        "MeasureType": f"{measure_type}", #can be either Advanced, Base, Scoring, Misc, Four Factors
        "PerMode": "Totals",
        "LeagueID": "00",
        "Season": "2022-23",
        "SeasonType": "Regular Season",
        "PORound": 0,
        "TeamID": {teamID},
        "PlayerID": None,
        "Outcome": None,
        "Location": None,
        "Month": 0,
        "SeasonSegment": None,
        "DateFrom": None,
        "DateTo": None,
        "OppTeamID": 0,
        "VsConference": None,
        "VsDivision": None,
        "GameSegment": None,
        "Period": 0,
        "ShotClockRange": None,
        "LastNGames": 0
    }
    return payload

def advanced_payload(playerID, measure, season="2022-23"):
    payload = {
        "MeasureType": f"{measure}",
        "PerMode": "Totals",
        "LeagueID": "00",
        "Season": season,
        "SeasonType": "Regular Season",
        "PORound": "0",
        "TeamID": None,
        "PlayerID": f"{playerID}",
        "Outcome": None,
        "Location": None,
        "Month": "0",
        "SeasonSegment": None,
        "DateFrom": None,
        "DateTo": None,
        "OppTeamID": "0",
        "VsConference": None,
        "VsDivision": None,
        "GameSegment": None,
        "PaceAdjust": "N",
        "Rank": "N",
        "Period": "0",
        "ShotClockRange": None,
        "LastNGames": "0"
    }
    return payload

def year_played_payload(playerID):
    payload = {
        "PerMode": "PerGame",
        "PlayerID": playerID,
        "LeagueID": "00"
    }
    return payload

def league_players_payload():
    payload = {
        "LeagueID": "00",
        "Season": "2023-24",
        "Historical": 1,
        "TeamID": 0,
        "Country": None,
        "College": None,
        "DraftYear": None,
        "DraftPick": None,
        "PlayerPosition": None,
        "Height": None,
        "Weight": None,
        "Active": None,
        "AllStar": None
    }
    return payload