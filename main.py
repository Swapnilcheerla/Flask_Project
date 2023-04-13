
from flask import Flask, render_template, request, url_for, redirect, session, flash
import pymongo

import bcrypt
import cloudinary
import cloudinary.uploader
from bson import ObjectId
from flask_socketio import join_room, leave_room, send, SocketIO
from trans import *


from main1 import *

app = Flask(__name__)
app.secret_key = "super secret key"
socketio = SocketIO(app)
cloudinary.config(
    cloud_name="dblffpknx",
    api_key="867853825134923",
    api_secret="RsvZruUhs0VfW2qEa0KxZKXFiak"
)
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]


# client = pymongo.MongoClient("mongodb+srv://SwapnilCheerla:<password>@cluster0.8rzuemq.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
# db = client.test

conn = "mongodb+srv://SwapnilCheerla:Swapnil143@cluster0.8rzuemq.mongodb.net/?retryWrites=true&w=majority"


def MongoDB():

    client = pymongo.MongoClient(
        conn, tls=True, tlsAllowInvalidCertificates=True)
    # client = pymongo.MongoClient(conn, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)

    db = client.get_database('userDB')
    return db


db = MongoDB()


## Connect with Docker Image###
# def dockerMongoDB():
#     client = pymongo.MongoClient(host='test_mongodb',
#                                  port=27017,
#                                  username='root',
#                                  password='pass',
#                                  authSource="admin")
#     db = client.users
#     pw = "test123"
#     hashed = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
#     records = db.register
#     records.insert_one({
#         "name": "Test Test",
#         "email": "test@yahoo.com",
#         "password": hashed
#     })
#     return records


# records = dockerMongoDB()


@app.route("/gallery/", methods=['post', 'get'])
def gallery():
    if "email" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        if "update" in request.form:

            name_img = request.form.get("name")
            quant = request.form.get("quant")
            id = request.form.get("hid")

            result = db.inveImg.update_one(
                {"_id": ObjectId(id)},
                {"$set": {
                    "name": name_img.strip(),
                    "quantity": quant
                }}
            )

            if result.modified_count == 1:
                # The update was successful
                message = "Successfully updated!"
            else:
                # The update failed
                message = "Update failed"
            return render_template("inventary.html",
                                   gallery=db.inveImg.find(), message=message)

        # return render_template("inventary.html", gallery=db.inveImg.find())

        if request.form["delete"]:
            delete_id = request.form["delete"]
            result = db.inveImg.delete_one({"_id": ObjectId(delete_id)})
            if result.deleted_count == 1:
                message = "Successfully deleted"
            else:
                message = "deletion failed"
            return render_template("inventary.html",
                                   gallery=db.inveImg.find(), message=message)

    return render_template("inventary.html", gallery=db.inveImg.find())
# assign URLs to have a particular route


@app.route("/", methods=['post', 'get'])
def index():
    message = ''
    mess = ''
    # if method post in index
    print(do_translate("hello ,how are you", "te"))
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        # if found in database showcase that it's found
        user_found = db.user.find_one({"name": user})
        email_found = db.user.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('index.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('index.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('index.html', message=message)
        else:
            # hash the password and encode it
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            # assing them in a dictionary in key value pairs
            user_input = {'name': user, 'email': email, 'password': hashed}
            # insert it in the record collection
            db.user.insert_one(user_input)

            # find the new created account and its email
            user_data = db.user.find_one({"email": email})
            new_email = user_data['email']
            # if registered redirect to logged in as the registered user
            mess = 'Registerted successfully! please Login'
            return redirect(url_for('login'))
    return render_template('index.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # check if email exists in database
        email_found = db.user.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            # print(email_val)
            passwordcheck = email_found['password']
            # encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                session["name"] = email_found['name']
                print(email_found['name'])
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)


rooms = {}


@app.route('/logged_in', methods=["POST", "GET"])
def logged_in():
    if "email" not in session:

        return render_template('login.html')

    #     pass
    # return redirect(url_for("login"))

    if request.method == "POST":

        code = "143"
        # join = request.form.get("join", False)
        create = request.form.get("create", False)

        room = code
        rooms[room] = {"members": 0, "messages": []}
        # if create != False:
        #     room = generate_unique_code(4)
        #
        # elif code not in rooms:
        #     return render_template("logged_in.html", error="Room does not exist.", code=code, name=name)

        session["room"] = room

        return redirect(url_for("room"))

    return render_template("logged_in.html")


@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("login"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])


@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return

    content = {
        "name": session.get("name"),
        "message": do_translate(data["data"], "te")
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    # print(f"{session.get('name')} said: {data['data']}")


@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return

    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        return render_template('index.html')


@app.route("/upload/", methods=["GET", "POST"])
def upload():
    if "email" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        image = request.files["image"]
        name_img = request.form.get("name")
        quant = request.form.get("quant")
        if image and image.filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS:
            upload_result = cloudinary.uploader.upload(image)

            db.inveImg.insert_one({

                "url": upload_result["secure_url"],
                "name": name_img.strip(),
                "quantity": quant
            })

            flash("Successfully uploaded image to gallery!", "success")
            return redirect(url_for("upload"))
        else:
            flash("An error occurred while uploading the image!", "danger")
            return redirect(url_for("upload"))
    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)
