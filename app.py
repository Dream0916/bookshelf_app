import datetime
import os
from mongoengine import *
from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, jsonify
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
# connect(host="mongodb://admin:admin@mongodb:27017/my_db?authSource=admin")
connect(host="mongodb://localhost:27017/my_db")


class Author(Document):
    name = StringField(required=True, max_length=70)
    birthDate = StringField(default="---")
    country = StringField(default="---", max_length=70)
    biography = StringField(default="---", max_length=300)


class Book(Document):
    name = StringField(required=True, max_length=70)
    publication = StringField(default="---")
    author = (StringField(default="---"))
    genres = StringField(default="---")

    status = StringField(required=True, default="want to read")


class BookReview(Document):
    book_name = StringField(required=True)
    date_started = StringField()
    date_finished = StringField()
    review = StringField()


@app.route('/')
def mainpage():
    return render_template("index.html", Authors=Author.objects, Books=Book.objects)


@app.route("/author", methods=["GET", "POST"])
def author():
    if request.method == "GET":
        return render_template("author.html", Authors=Author.objects, Books=Book.objects)
    elif request.method == "POST":
        name = request.form["name"]
        birth_date = request.form["birth_date"]
        country = request.form["country"]
        bio = request.form["bio"]

        Author(name=name, birthDate=birth_date, country=country, biography=bio).save()

        return render_template("author.html", message="Author added", Authors=Author.objects)


@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method == "GET":
        return render_template("book.html", Authors=Author.objects)
    elif request.method == "POST":
        name = request.form["name"]
        publication = request.form["publication"]
        author = request.form["author"]
        genres = request.form["genres"]

        status = request.form["status"]

        Book(name=name, publication=publication, author=author, genres=genres, status=status).save()

        if status == "read":
            return redirect(url_for("review"))
        else:
            return render_template("book.html", message="Book added", Authors=Author.objects, Books=Book.objects)


@app.route("/review", methods=["GET", "POST"])
def review():
    if request.method == "GET":
        return render_template("review.html", Authors=Author.objects, Books=Book.objects,
                               BookReviews=BookReview.objects)
    elif request.method == "POST":
        book_name = request.form["book_name"]
        date_started = request.form["started"]
        date_finished = request.form["finished"]
        review = request.form["review"]

        BookReview(book_name=book_name, date_started=date_started, date_finished=date_finished, review=review).save()

        if Book.objects == BookReview.objects.book_name:

            Book.objects.status = "read"

            return render_template("review.html", message="status changed to read",
                                   Authors=Author.objects, Books=Book.objects)

        return render_template("review.html", message="Review added", Authors=Author.objects, Books=Book.objects)


if __name__ == "__main__":
    app.run(debug=True)
