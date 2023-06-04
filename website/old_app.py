from flask import Flask, render_template, request, url_for, redirect
from db import init_db, search_wheels

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/wheels")
def wheels():
    return render_template("wheels.html")

@app.route("/framesets")
def framesets():
    return render_template("framesets.html")

@app.route("/components")
def components():
    return render_template("components.html")

@app.route("/back")
def back():
    return redirect(url_for("home"))

@app.route("/results_wheels", methods=["GET", "POST"])
def results_wheels():
    if request.method == "POST":
        search_query = request.form["search"]
        results = search_wheels(search_query)
        return render_template("results_wheels.html", results=results)
    return redirect(url_for("wheels"))

if __name__ == "__main__":
    init_db(app)
    app.run(debug=True)
