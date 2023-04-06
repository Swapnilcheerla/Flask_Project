from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
# from flask_bcrypt import Bcrypt
import cloudinary
import cloudinary.uploader
app = Flask(__name__)

# client = pymongo.MongoClient("mongodb+srv://SwapnilCheerla:<password>@cluster0.8rzuemq.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
# db = client.test

conn = "mongodb+srv://SwapnilCheerla:Swapnil143@cluster0.8rzuemq.mongodb.net/?retryWrites=true&w=majority"


@app.route("/")
def MongoDB():
    client = pymongo.MongoClient(conn)

    db = client.get_database('userDB')
    records = db.user

    return "success"


# records = MongoDB()


if __name__ == "__main__":
    app.run(debug=True)
