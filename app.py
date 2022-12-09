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



        book = Book.objects(name=book_name).first()
        book.update(status="read")
        book.save()


        return render_template("review.html", message="status changed to read",
                                   Authors=Author.objects, Books=Book.objects)

def generate_html_document(review):

    html_document = """
        <!DOCTYPE html>
        <html>
            <head>
                <title>Book Review: {}</title>
            </head>
            <body>
                <h1>Book Review: {}</h1>
                <p><b>Book name:</b> {}</p>
                <p><b>Date started:</b> {}</p>
                <p><b>Date finished:</b> {}</p>
                <p><b>Review:</b> {}</p>
            </body>
        </html>
    """.format(review.book_name, review.book_name, review.book_name, review.date_started, review.date_finished, review.review)

    return html_document


for review in BookReview.objects:
    html_document = generate_html_document(review)

    # Save the HTML document to a file
    with open("templates/reviews/review_{}.html".format(review.book_name), "w", encoding="utf-8") as f:
        f.write(html_document)



if __name__ == "__main__":
    app.run(debug=True)
