import time
from predictor import Predictor
from scraper import NBAScraper
from threading import Thread
from flask import Flask, url_for, render_template, request, jsonify, make_response, redirect
import requests
from turbo_flask import Turbo
from tasks import background_task

# predictor = Predictor()
# scraper = NBAScraper()
# playername = input("Enter a player name: ")
# predictor.train_model('pts', scraper.get_advanced_player_stats(playername))

app = Flask(__name__)
turbo = Turbo(app)
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


tasks = []
results = []

@app.route("/prediction/<playerID>", methods=['POST', 'GET'])
def prediction(playerID):
    # pred = Predictor()
    # result = pred.train_model('pts', playerdf=scraper.get_advanced_player_stats(playerID=playerID)) 
    new_task_id = len(tasks)
    task = Thread(target=do_work, kwargs={'playerID': playerID, 'task_id': new_task_id, 'results': results})
    task.start()
    tasks.append(task)
    results.append(None)
    return render_template('prediction.html', player=new_task_id)

def do_work(task_id, results, playerID):
    pred = Predictor()
    results[task_id] = f"finished task {pred.train_model('pts', playerdf=scraper.get_advanced_player_stats(playerID=playerID))}"

@app.route("/task/<int:task_id>", methods=["GET"])
def task_status(task_id):
    assert 0 <= task_id < len(tasks)
    if tasks[task_id].is_alive():
        return jsonify({'status': 'running'})
    try:
        tasks[task_id].join()
        return jsonify({'status': 'finished', 'result': results[task_id]})
    except RuntimeError:
        return jsonify({'status': 'not started'})



if __name__ == "__main__":
    app.run(debug=True, threaded=True)