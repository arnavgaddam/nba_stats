from predictor import Predictor
from scraper import NBAScraper
from flask import Flask, url_for, render_template, request, jsonify, make_response
import requests


# predictor = Predictor()
# scraper = NBAScraper()
# playername = input("Enter a player name: ")
# predictor.train_model('pts', scraper.get_advanced_player_stats(playername))

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods = ['POST'])
def search():
    req = request.get_json()
    print(req)
    res = make_response(jsonify({"message": "JSON receive"}), 200)
    return res

@app.route("/prediction", methods=['POST', 'GET'])
def predict_stats():
    return 



if __name__ == "__main__":
    app.run(debug=True)