import pandas as pd

class Player:

    def __init__(self, data):
        self.stats = data

    def get_season_stats(self, startYear):
        return self.stats.loc[self.stats['GROUP_VALUE'] == f'20{startYear}-{startYear+1}']

    