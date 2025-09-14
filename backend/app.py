from flask import Flask, jsonify, request
from models import Player
import socket

app = Flask(__name__)

def with_pod_info(data):
    return {
        "pod": socket.gethostname(),
        "data": data
    }

@app.route('/api/players', methods=['GET'])
def get_players():
    country = request.args.get('country')
    club = request.args.get('club')
    year_gt = request.args.get('year_gt', type=int)
    year_lt = request.args.get('year_lt', type=int)

    players = Player.get_by_parameters(country, club, year_gt, year_lt)
    return jsonify(with_pod_info([player.to_dict() for player in players]))

@app.route('/api/players', methods=['POST'])
def add_player():
    data = request.json
    if not all(k in data for k in ("name", "nationality", "current_club", "year_of_birth")):
        return jsonify({"error": "Missing data"}), 400
    player = Player(data["name"], data["nationality"], data["current_club"], data["year_of_birth"])
    player_id = Player.save(player)
    return jsonify(with_pod_info({"id": player_id, **player.to_dict()})), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
