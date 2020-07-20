import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table (same as climate_starter notebook)
Measurement_Table = Base.classes.measurement
Station_Table = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """a.	Convert the query results to a dictionary using date as the key and prcp as the value."""
    """b.	Return the JSON representation of your dictionary"""


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """a.	Return a JSON list of stations from the dataset."""
   

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """a.	Query the dates and temperature observations of the most active station for the last year of data."""
    """b.	Return a JSON list of temperature observations (TOBS) for the previous year."""


@app.route("/api/v1.0/start")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """a.	Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    """b.	When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.""
    """c.	When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.""


if __name__ == '__main__':
    app.run(debug=True)
