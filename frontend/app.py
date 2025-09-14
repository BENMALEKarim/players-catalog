from flask import Flask, render_template, request, redirect, url_for
import requests
import os
import socket

app = Flask(__name__)

API_BASE = os.getenv("BACKEND_HOST", "http://localhost:5001/api/players")

@app.route('/')
def index():
    # Get filter parameters from request
    params = {
        "country": request.args.get("country"),
        "club": request.args.get("club"),
        "year_gt": request.args.get("year_gt"),
        "year_lt": request.args.get("year_lt"),
    }

    # Remove empty parameters
    query_params = {k: v for k, v in params.items() if v}

    # Fetch players data from the backend
    res = requests.get(API_BASE, params=query_params)
    if res.ok:
        response_data = res.json()
        players = response_data.get("data", [])
        backend_pod = response_data.get("pod", "Unknown")
    else:
        players = []
        backend_pod = "Unavailable"

    frontend_pod = socket.gethostname()

    return render_template("index.html", players=players, backend_pod=backend_pod, frontend_pod=frontend_pod, filters=params)


@app.route('/add', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        data = {
            "name": request.form["name"],
            "nationality": request.form["nationality"],
            "current_club": request.form["club"],
            "year_of_birth": int(request.form["year_of_birth"])
        }
        # Send POST request to backend to add the new player
        res = requests.post(API_BASE, json=data)
        if res.ok:
            return redirect('/')
        else:
            return "Error adding player", 500

    return render_template("add_player.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
