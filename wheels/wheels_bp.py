from flask import Blueprint, render_template, request, url_for, redirect
from wheels.db import search_wheels  # Updated the import statement

wheels_bp = Blueprint("wheels_bp", __name__, template_folder="templates", static_folder="static")


@wheels_bp.route("/")
def wheels():
    print("wheels() function called")  # add this line    
    return render_template("wheels.html")

@wheels_bp.route("/results_wheels", methods=["GET", "POST"])
def results_wheels():
    if request.method == "POST":
        search_query = request.form["search"]
        results = search_wheels(search_query)
        return render_template("results_wheels.html", results=results)
    return redirect(url_for("wheels"))


@wheels_bp.route("/test")
def test():
    return render_template("wheels.html")