from flask_app import app
from flask import render_template,redirect,request, session
from flask_app.models import model_sighting


@app.route("/sighting/create")
def create_new_sighting():
    return render_template("add_sighting.html")

@app.route("/sighting/create/process", methods=["post"])
def process_new_sighting():
    print(request.form)
    data = {
        **request.form,
        "users_id" : session["user_id"]
    }
    if not model_sighting.Sighting.validate_sighting(data):
        return redirect('/sighting/create')

    model_sighting.Sighting.create_one(data)
    return redirect("/dashboard")

@app.route("/sighting/<int:id>/show") 
def get_one_sighting(id):
    sighting = model_sighting.Sighting.get_one({"id" : id})
    data = {
        "user_id" : session["user_id"],
        "sighting_id" : id
    }
    return render_template("show_sighting.html", sighting = sighting, is_skeptic = model_sighting.Sighting.user_is_skeptic(data))

@app.route("/sighting/<int:id>/update")
def update_form_sighting(id):
    sighting = model_sighting.Sighting.get_one({"id" : id})
    if session["user_id"] != sighting.users_id:
        return redirect("/dashboard")
    return render_template("edit_sighting.html", sighting=sighting)

@app.route("/sighting/<int:id>/update/process", methods=["post"])
def update_one_sighting(id):
    sighting = model_sighting.Sighting.get_one({"id" : id})
    if session["user_id"] != sighting.users_id:
        return redirect("/dashboard")
    sighting = model_sighting.Sighting.get_one({"id" : id})
    data = {
        **request.form,
        "id" : id
    }
    if not model_sighting.Sighting.validate_sighting(data):
        return redirect(f"/sighting/{sighting.id}/update")
    model_sighting.Sighting.update_one(data)
    return redirect("/dashboard")

@app.route("/sighting/<int:id>/destroy")
def destroy_one(id):
    sighting = model_sighting.Sighting.get_one({"id": id})
    if session["user_id"] != sighting.users_id:
        return redirect("/dashboard")
    model_sighting.Sighting.delete_one({"id" : id})
    return redirect("/dashboard")