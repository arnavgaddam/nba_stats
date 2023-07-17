import pandas as pd
import numpy as np
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.model_selection import TimeSeriesSplit
from sklearn.svm import SVR
from scraper import NBAScraper
from sklearn.preprocessing import MinMaxScaler

class Predictor:

    def __init__(self) -> None:
        self.labels = {'pts': 'next_pts',
                      'ast': 'next_ast',
                      'reb': 'next_reb',
                      'fg3m': 'next_fg3m'}
        
    def train_model(self, stat, playerdf=None):
        df = pd.read_csv('butler.csv')
        df = playerdf
        df.drop(list(df.filter(regex = 'RANK')), axis = 1, inplace = True)
        df[self.labels[stat]] = df[stat.upper()].shift(-1)
        df.dtypes[df.dtypes == "object"]
        df.drop(["WL", "SEASON_YEAR"], axis=1)
        fulldf = df.copy()
        df = df.dropna()
        df = pd.get_dummies(df, columns=['OPPONENT', 'TEAM_ABBREVIATION', 'WL'], dtype=np.uint8)
        split = TimeSeriesSplit(n_splits=3)


        svrmod = SVR(kernel="poly")
        removed_cols = [self.labels[stat], "SEASON_YEAR", "GAME_DATE"]
        selected_cols = df.columns[~df.columns.isin(removed_cols)]

        scaler = MinMaxScaler()
        df.loc[:, selected_cols] = scaler.fit_transform(df[selected_cols])
        sfs3 = SequentialFeatureSelector(svrmod, n_features_to_select=10, direction="forward", cv=split, n_jobs=6)
        sfs3.fit(df[selected_cols], df[self.labels[stat]])
        predictors3 = list(selected_cols[sfs3.get_support()])

        def backtest(data, model, predictors, start=4, step=1):
            allpreds = []
            games = sorted(data["GAME_DATE"].unique())

            for i in range(start, len(games), step):
                current_game = games[i]
                train = data[data["GAME_DATE"] < current_game]
                test = data[data["GAME_DATE"] == current_game]

                model.fit(train[predictors], train[self.labels[stat]])
                preds = model.predict(test[predictors])
                preds = pd.Series(preds, index=test.index)
                combined = pd.concat([test[self.labels[stat]], preds], axis=1)
                combined.columns = ["actual", "prediction"]
                allpreds.append(combined)

            return pd.concat(allpreds)

        predictions3 = backtest(df, svrmod, predictors3)
        print(predictions3)

        from sklearn.metrics import mean_squared_error
        from sklearn.metrics import mean_absolute_error

        print(mean_squared_error(predictions3['actual'], predictions3['prediction']))
        print(mean_absolute_error(predictions3['actual'], predictions3['prediction']))


if __name__ == "__main__":
    scraper = NBAScraper()
    butler = scraper.get_advanced_player_stats("Stephen Curry")
    pred = Predictor()
    pred.train_model("ast", playerdf=butler)
