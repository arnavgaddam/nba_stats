from app import NBAScraper
import pandas as pd

scraper = NBAScraper()
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

from sklearn.model_selection import TimeSeriesSplit
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.linear_model import RidgeClassifier

rr = RidgeClassifier(alpha=1)
split = TimeSeriesSplit(n_splits=3)

sfs = SequentialFeatureSelector(rr, n_features_to_select=30, direction="forward", cv=split)
removed_columns = ["SEASON_YEAR", "TEAM_ABBREVIATION", "GAME_ID", "W", "L", "MATCHUP", "GAME_DATE", "WL", "target", "ARENA"]
selected_columns = heat_log.columns[~heat_log.columns.isin(removed_columns)]

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
heat_log[selected_columns] = scaler.fit_transform(heat_log[selected_columns])

sfs.fit(heat_log[selected_columns], heat_log['target'])
predictors = list(selected_columns[sfs.get_support()])

train = heat_log.iloc[:50]
test = heat_log.iloc[50:]    

rr.fit(train[predictors], train["target"])
preds = rr.predict(test[predictors])
preds = pd.Series(preds, index=test.index)
combined = pd.concat([test["target"], preds], axis=1)
combined.columns = ['actual', 'prediction']
print(combined)

from sklearn.metrics import accuracy_score
print(accuracy_score(combined["actual"], combined['prediction']))