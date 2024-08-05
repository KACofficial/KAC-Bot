from flask import Flask, render_template, request, jsonify
import logging

app = Flask(__name__)

app.logger.setLevel(logging.INFO)

movies = []

# Attach null handler to Flask logger
app.logger.addHandler(logging.NullHandler())

# Disable Werkzeug logging
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.addHandler(logging.NullHandler())
global_key = None


def setup_global_api_key(key):
    global global_key
    global_key = key


@app.route("/")
def main():
    return render_template("index.html", movies=movies)


@app.route("/add-movie", methods=["POST"])
def add_movie():
    key = request.headers.get('Authorization')

    if key != global_key:
        return jsonify({"status": "unauthorized"}), 401

    title = request.form.get("title")
    desc = request.form.get("desc")
    movie_id = request.form.get("id")
    if title and desc:
        movies.append({"title": title, "desc": desc, "id": movie_id})
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "failure"}), 400


@app.route("/reset-requests", methods=["GET"])
def reset_requests():
    key = request.headers.get('Authorization')

    if key != global_key:
        return jsonify({"status": "unauthorized"}), 401

    try:
        movies.clear()
        return jsonify({"status": "success"}), 200
    except Exception:
        return jsonify({"status": "failure"}), 400


@app.route("/get-movies", methods=["GET"])
def return_movies():
    complete_data = {
        "movies": movies,
        "count": len(movies)
    }
    return jsonify(complete_data), 200


def run_flask():
    app.run(port=3000)
