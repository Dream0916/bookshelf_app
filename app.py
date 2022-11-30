import datetime

from flask import Flask, render_template, request

from mongoengine import *

app = Flask(__name__)

db = connect(host="mongodb://localhost:27017/my_db")


class Author(Document):
    name = StringField(required=True, max_length=70)
    birthDate = StringField()
    country = StringField(required=True, max_length=70)
    biography = StringField(required=True, max_length=300)


class Book(Document):
    name = StringField(required=True, max_length=70)
    publication = StringField(required=True)
    author = ReferenceField(Author)
    genres = ListField(StringField)
    # dateAdded = DateTimeField(required=True,default=datetime.datetime)


authors = dict()


@app.route('/')
def mainpage():
    return render_template("index.html", Authors=Author.objects, Books=Book.objects)


@app.route("/author", methods=["GET", "POST"])
def author():
    if request.method == "GET":
        return render_template("author.html")
    elif request.method == "POST":
        name = request.form["name"]
        birth_date = request.form["birth_date"]
        country = request.form["country"]
        bio = request.form["bio"]

        author = Author(name=name, birthDate=birth_date, country=country, biography=bio).save()

        return render_template("autor.html", message="Author added")


@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method == "GET":
        return render_template("book.html", Authors=Author.objects)
    elif request.method == "POST":
        name = request.form["name"]
        publication = request.form["publication"]
        author = request.form["author"]
        genres = request.form["genres"]

        book = Book(name=name, publication=publication, author=author, genres=genres).save()
        return render_template("book.html", message="Book added")


if __name__ == "__main__":
    app.run(debug=True)
