from flask import Flask, render_template, flash, url_for, session, g
from flask.globals import request
from werkzeug.utils import redirect
from flask_session import Session
import model
import ml_mushroom as m

app = Flask(__name__)
app.secret_key = 'MingLinLi'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['IMAGE_UPLOADS'] = "C:/Users/bhish/Downloads/Pirple coursewrok/flask_assignemnt1/static/images/"
Session(app)



@app.route('/', methods=["GET","POST"])
def sign_up():
    #session.pop(username,None)
    if request.method == "GET":
        return render_template("signup.html")
    else:
        if request.form['submit_btn'] == 'register':
            created_username = request.form.get('username')
            created_password = request.form.get('password')
            message = model.insertData(created_username, created_password)
            return render_template("signup.html", message=message)

        if request.form['submit_btn'] == 'login':
            username = request.form.get('username')
            password = request.form.get('password')
            bool_user = model.checkUsernameAndPassword(username, password)

            if bool_user == True:
                login_user = model.User(username,password)
                session["username"] = login_user.getCurrentUser()
                return redirect(url_for('mushroom_home'))
            else:
                message = "User does not exist. Please register user."
                return render_template("signup.html", message=message)
        

@app.route('/home', methods=["GET","POST"])
def mushroom_home():
    if request.method == "GET":
        if session.get("username") in model.listOfAllLoginUsers():
            return render_template("home.html")
        else:
            return redirect(url_for("sign_up"))
    if request.method == "POST" and request.files and session.get("username") in model.listOfAllLoginUsers():
        import os
        image = request.files["image"]
        if len(image.filename) != 0:
            image.save(os.path.join(app.config['IMAGE_UPLOADS'], image.filename))
            isMushroom = m.identify_mushroom(image)
            if isMushroom:
                mushroom_details = m.mushroom_species(image)
                mushroom_details.append(image.filename)
                model.removeImages(image.filename)
                return render_template("home.html", mushroom_details = mushroom_details)
            else:
                model.removeImages()
                flash("There is no mushroom in the image")
                return redirect(request.url)
        else:
            flash("Please upload a new image")
            return redirect(request.url)
    else:
        return redirect(url_for("sign_up"))

@app.route("/logout")
def logout():
    model.listOfAllLoginUsers().remove(session["username"])
    model.removeImages()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True, port=7000)