import os
from pathlib import Path

from flask import Flask, render_template, send_file, request

app = Flask(__name__)
users_info = {}
file_store_path = "/home/ubuntu/file_store"


@app.route("/download/<username>/<filename>")
def download(username, filename):
    path = os.path.join(file_store_path, username, filename)
    return send_file(path, as_attachment=True, attachment_filename='')


def display(user_info, file):
    wordcount = -1
    if len(file) > 0:
        f = open(os.path.join(file_store_path, file), "r")
        data = f.read()
        dataword = data.split()
        wordcount = len(dataword)
    return render_template("display.html", first_name=user_info["first_name"],
                           last_name=user_info["last_name"], email=user_info["email"],
                           user_name=user_info["user_name"], password=user_info["password"],
                           filename=file, wordcount="NA" if wordcount == -1 else wordcount)


@app.route("/")
def index():
    return render_template("register.html")


@app.route("/login", methods=['POST', "GET"])
def login():
    if request.method == "POST":
        user_name = request.form['username']
        password = request.form['password']
        if user_name.lower() in users_info.keys():
            user_info = users_info[user_name.lower()]
            if password == user_info["password"]:
                full_file_path = None
                if user_info["file_name"] == "":
                    full_file_path = ""
                else:
                    #  file_store_path = /home/ubuntu/tanya/file1.txt
                    full_file_path = os.path.join(user_name, user_info["file_name"])
                return display(user_info, full_file_path)
            else:
                return "Password is incorrect"
        else:
            return "User name does not exist"
    if request.method == "GET":
        return render_template("login.html")


@app.route('/register', methods=['POST', "GET"])
def register():
    if request.method == "POST":
        if request.form["username"] in users_info:
            return "User exists, register with a different username"
        if ' ' in request.form["username"]:
            return "Username can't have spaces"
        file = request.files['file']
        username_dir = request.form["username"]
        if len(file.filename) > 0:
            Path(os.path.join(file_store_path, username_dir)).mkdir(exist_ok=True)
            file.save(os.path.join(file_store_path, username_dir, file.filename))
        user_info = {
            "first_name": request.form['firstname'],
            "last_name": request.form['lastname'],
            "email": request.form['email'],
            "password": request.form['password'],
            "user_name": request.form['username'],
            "file_name": file.filename
        }
        users_info[request.form["username"].lower()] = user_info
        print("the datastore dict now has these values {}\n".format(users_info))
        return display(user_info, "" if file.filename == "" else os.path.join(username_dir, file.filename))
    if request.method == "GET":
        return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
