from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)
users_info = {}


def display(user_info):
    return render_template("display.html", first_name=user_info["first_name"],
                           last_name=user_info["last_name"], email=user_info["email"],
                           user_name=user_info["user_name"], password=user_info["password"]
                           )


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
                return display(user_info)
            else:
                return "Password is incorrect"
        else:
            return "User name does not exist"
    if request.method == "GET":
        return render_template("login.html")


@app.route('/register', methods=['POST', "GET"])
def register():
    if request.method == "POST":
        user_info = {
            "first_name": request.form['firstname'],
            "last_name": request.form['lastname'],
            "email": request.form['email'],
            "password": request.form['password'],
            "user_name": request.form['username']
        }
        users_info[request.form["username"].lower()] = user_info
        print("the datastore dict now has these values {}\n".format(users_info))
        return display(user_info)
    if request.method == "GET":
        return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
