from flask import Flask, render_template, url_for, redirect, request

from website.home.home_bp import home_bp  # Import the home_bp blueprint
from website.wheels.wheels_bp import wheels_bp  # Import the wheels_bp blueprint

# Create the Flask app 
app = Flask(__name__, static_folder=None)

# Register the blueprints
app.register_blueprint(home_bp)
app.register_blueprint(wheels_bp, url_prefix="/wheels")

@app.route("/framesets")
def framesets():
    return render_template("framesets.html")

@app.route("/components")
def components():
    return render_template("components.html")

# Add a back route to redirect to the previous page
@app.route("/back")
def back():
    return redirect(request.referrer or url_for("home"))

if __name__ == "__main__":
    app.run(debug=True, port=8888)
