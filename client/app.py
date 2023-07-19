from predictor import Predictor
from scraper import NBAScraper
from threading import Thread
from flask import Flask, url_for, render_template, request, jsonify, make_response, redirect
import requests


# predictor = Predictor()
# scraper = NBAScraper()
# playername = input("Enter a player name: ")
# predictor.train_model('pts', scraper.get_advanced_player_stats(playername))

app = Flask(__name__)
scraper = NBAScraper()

    

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print(request.form.to_dict())
        return redirect(url_for('prediction'))
    return render_template("index.html")


@app.route("/search", methods = ['GET', 'POST'])
def search():
    if request.method == 'POST':
        print(request.form.to_dict()['query'])
        return redirect(url_for('prediction', playerID=scraper.player_to_id(request.form.to_dict()['query'].title())))
    # req = request.get_json()
    # res = make_response(jsonify({"playerID": scraper.player_to_id(req['playerName'].title())}), 200)
    return "<p> blank </p>"

@app.route("/prediction/<playerID>", methods=['POST', 'GET'])
def prediction(playerID):
    pred = Predictor()
    result = pred.train_model('pts', playerdf=scraper.get_advanced_player_stats(playerID=playerID))
    return render_template('prediction.html', player=result)



if __name__ == "__main__":
    app.run(debug=True)