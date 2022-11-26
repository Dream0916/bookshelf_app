from flask import Flask

app = Flask(__name__)

@app.route('/')
def uvodni_stranka():
    return '<h1>Muj NoSQL projekt</h1>'

if __name__ == "__main__":
    app.run(debug=True)