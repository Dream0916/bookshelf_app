from flask import Flask, render_template, request

app = Flask(__name__)

db = dict()

@app.route('/')
def uvodni_stranka():
    return render_template("index.html", databaze=db)

@app.route("/kontakt", methods=["GET", "POST"])
def kontakt():
    if request.method == "GET":
        return render_template("kontakt.html")
    elif request.method == "POST":
        email = request.form["email"]
        dotaz = request.form["dotaz"]
        db[email] = dotaz

        return render_template("kontakt.html", vzkaz="Dotaz byl nahran")

if __name__ == "__main__":
    app.run(debug=True)