#Used ChatGPT help

from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm  # Ensure FlaskForm is imported
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import random  # For simulating finding the nearest MBTA station.

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Secret key for WTForms

# Simulated data for MBTA stations (name, wheelchair accessible)
mbta_stations = [
    ("South Station", True),
    ("Back Bay", False),
    ("North Station", True),
    ("Kenmore", False),
    ("Alewife", True)
]

# Create the form using WTForms (now inheriting from FlaskForm)
class PlaceForm(FlaskForm):  # Use FlaskForm instead of Form
    place = StringField('Enter a place name', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Home Page - Display the form
@app.route("/", methods=["GET", "POST"])
def hello():
    form = PlaceForm()  # Create the form
    if request.method == "POST" and form.validate():
        place_name = form.place.data
        return redirect(url_for('nearest_mbta', place_name=place_name))
    return render_template('index.html', form=form)

# Nearest MBTA Station - Handle form submission
@app.route("/nearest_mbta", methods=["GET"])
def nearest_mbta():
    place_name = request.args.get('place_name')
    if not place_name:
        return render_template("error.html", error="No place name provided.")

    # For the sake of this example, we'll randomly choose a station
    station_name, is_wheelchair_accessible = random.choice(mbta_stations)
    return render_template('mbta_station.html', place_name=place_name, 
                           station_name=station_name, 
                           is_wheelchair_accessible=is_wheelchair_accessible)

# Error page - Render error if something goes wrong
@app.route("/error")
def error():
    return render_template("error.html", error="There was an error processing your request.")

if __name__ == "__main__":
    app.run(debug=True)




