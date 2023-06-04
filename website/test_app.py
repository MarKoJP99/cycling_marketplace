from flask import Flask, render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Set the template directories explicitly
app.template_folder = '/Users/marko/data_science/cycling_marketplace'
app.add_template_folder('home/templates')
app.add_template_folder('wheels/templates')

@app.route("/")
def home():
    return render_template("test_home.html")

@app.route("/wheels")
def wheels():
    return render_template("test_wheels.html")

if __name__ == "__main__":
    app.run(debug=True, port=8080)
