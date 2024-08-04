from flask import Flask, render_template, request, jsonify
import logging

app = Flask(__name__)

app.logger.setLevel(logging.INFOgit)

movies = []

# Attach null handler to Flask logger
app.logger.addHandler(logging.NullHandler())

# Disable Werkzeug logging
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.addHandler(logging.NullHandler())


@app.route("/")
def main():
    return render_template("index.html", movies=movies)


@app.route("/add-movie", methods=["POST"])
def add_movie():
    title = request.form.get("title")
    desc = request.form.get("desc")
    if title and desc:
        movies.append({"title": title, "desc": desc})
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "failure"}), 400


@app.route("/reset-requests", methods=["GET"])
def reset_requests():
    try:
        movies.clear()
        return jsonify({"status": "success"}), 200
    except:
        return jsonify({"status": "failure"}), 400


def run_flask():
    app.run(port=3000)
