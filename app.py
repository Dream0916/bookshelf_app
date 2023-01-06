import datetime
import os
from mongoengine import *
from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, jsonify
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
connect(host="mongodb://admin:admin@mongodb:27017/my_db?authSource=admin")
#connect(host="mongodb://localhost:27017/my_db")


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



        book = Book.objects(name=book_name).first()
        book.update(status="read")
        book.save()


        return render_template("review.html", message="status changed to read",
                                   Authors=Author.objects, Books=Book.objects)

@app.route("/edit_author", methods=["POST"])
def edit_author():
  author_id = request.form["author_id"]
  author = Author.objects(id=author_id).first()
  return render_template("author.html", author=author)

@app.route("/delete_author", methods=["POST"])
def delete_author():
  author_id = request.form["author_id"]
  author = Author.objects(id=author_id).first()
  author.delete()
  return redirect(url_for("author"))

@app.route("/update_author", methods=["POST"])
def update_author():
  author_id = request.form["author_id"]
  author = Author.objects(id=author_id).first()
  author.name = request.form["name"]
  author.birth_date = request.form["birth_date"]
  author.country = request.form["country"]
  author.biography = request.form["bio"]
  author.save()
  return redirect(url_for("author"))

@app.route("/edit_book", methods=["POST"])
def edit_book():
  book_id = request.form["book_id"]
  book = Book.objects(id=book_id).first()
  return render_template("book.html", book=book)

@app.route("/delete_book", methods=["POST"])
def delete_book():
  book_id = request.form["book_id"]
  book = Book.objects(id=book_id).first()
  book.delete()
  return redirect(url_for("book"))

@app.route("/update_book", methods=["POST"])
def update_book():
  book_id = request.form["book_id"]
  book = Book.objects(id=book_id).first()
  book.name = request.form["name"]
  book.publication = request.form["publication"]
  book.author = request.form["country"]
  book.genres = request.form["bio"]
  book.status = request.form["status"]
  book.save()
  return redirect(url_for("book"))

if __name__ == "__main__":
    app.run(debug=True)

