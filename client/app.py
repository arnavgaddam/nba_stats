from pts_pred import Predictor
from scraper import NBAScraper
predictor = Predictor()
scraper = NBAScraper()
playername = input("Enter a player name: ")
predictor.train_model('pts', scraper.get_advanced_player_stats("LeBron James"))
