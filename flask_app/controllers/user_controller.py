
from flask_app import app
from flask import render_template,redirect,request, session, flash
from flask_app.models import model_user, model_sighting



@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    if not model_user.User.validate_user(request.form):
        return redirect('/')
    data = {
        **request.form
    }
    data["pw"] = model_user.bcrypt.generate_password_hash(data["pw"])
    user = model_user.User.create_one(data)
    return redirect('/')

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    sightings = model_sighting.Sighting.get_all_sightings_with_users()
    return render_template("dashboard.html", sightings = sightings)

@app.route("/login", methods = ["post"])
def login():
    data = {
        "email" : request.form["email"],
        }
    if not model_user.User.validate_login(request.form):
        return redirect("/")
    user_in_db = model_user.User.get_user_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not model_user.bcrypt.check_password_hash(user_in_db.password, request.form['pw']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    session["full_name"] = user_in_db.full_name
    return redirect("/dashboard")

@app.route("/skeptic/<int:sight_id>/<int:user_id>")
def skeptical(sight_id, user_id):
    data = {
        "sighting_id" : sight_id,
        "user_id" : user_id
    }
    model_user.User.make_skeptic(data)
    return redirect(f"/sighting/{sight_id}/show")

@app.route("/skeptic/<int:sight_id>/<int:user_id>/delete")
def beleiver(sight_id, user_id):
    data = {
        "sighting_id" : sight_id,
        "user_id" : user_id
    }
    model_user.User.delete_skeptic(data)
    return redirect(f"/sighting/{sight_id}/show")


@app.route("/logout")
def logout():
    del session["user_id"]
    del session["full_name"]
    return redirect("/")




