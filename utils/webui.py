from flask import Flask, render_template, request, jsonify
import logging

app = Flask(__name__)

app.logger.setLevel(logging.INFO)

movies = []


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


def run_flask():
    app.run(port=3000)