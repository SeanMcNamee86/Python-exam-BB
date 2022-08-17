from flask import Flask

DATABASE = "sasquatch_sightings"

app = Flask(__name__)

app.secret_key = "please_give_10/10"

