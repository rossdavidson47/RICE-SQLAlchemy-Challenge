#import dependencies
import numpy as np
import pandas as pd
import datetime as dt
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

#Start a session to query the database
session = Session(engine)

#Find last twelve months with SQL
end_date = session.query(Measurement_Table.date).order_by(Measurement_Table.date.desc()).first()
end_date = dt.datetime.strptime((*end_date), '%Y-%m-%d')
year_earlier_date = end_date - dt.timedelta(days=365)

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
        f"This is the page for Ross Davidson for the Rice SQL Alchemy Challenge<br/>"
        f"Dude this took forever.<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """a.	Convert the query results to a dictionary using date as the key and prcp as the value."""
    """b.	Return the JSON representation of your dictionary"""
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #query
    query = [Measurement_Table.date, Measurement_Table.prcp]
    rainfall = session.query(*query).filter(Measurement_Table.date >= year_earlier_date).all()
    #Close the session
    session.close()
    #Jsonify
    return jsonify(rainfall)

@app.route("/api/v1.0/stations")
def stations():
    """a.	Return a JSON list of stations from the dataset."""
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #query
    List_of_Stations = session.query(Measurement_Table.station).distinct().all()
    #Close the session
    session.close()
    #Jsonify
    all_names = list(np.ravel(List_of_Stations))
    return jsonify(all_names)
   

@app.route("/api/v1.0/tobs")
def tobs():
    """a.	Query the dates and temperature observations of the most active station for the last year of data."""
    """b.	Return a JSON list of temperature observations (TOBS) for the previous year."""
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #query
    # Query Measurement_Table and save the query into results
    results = session.query(Measurement_Table.id, Measurement_Table.station, Measurement_Table.date, Measurement_Table.prcp, Measurement_Table.tobs).all()
    # Load the results into a pandas dataframe. Set the index to the `Measurement_Table.id`
    Measurement_df = pd.DataFrame(results[:], columns=['Measurement_Table.id', 'Measurement_Table.station', 'Measurement_Table.date', 'Measurement_Table.prcp', 'Measurement_Table.tobs'])
    Measurement_df.set_index('Measurement_Table.id', inplace=True, )
    # List the stations and the counts in descending order.
    Station_Counts_df = pd.DataFrame(Measurement_df['Measurement_Table.station'].value_counts())
    #Choose the most active station
    Most_Active_Station = Station_Counts_df.index[0]
   #Close the session
    session.close()
    #Jsonify
    all_names = list(np.ravel(Most_Active_Station))
    return jsonify(all_names)


@app.route("/api/v1.0/start")
def start():
    """a.	Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    """b.	When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date."""
    """c.	When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive."""
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #query
    # Load the results into a pandas dataframe. Set the index to the `Measurement_Table.id`
    results = session.query(Measurement_Table.id, Measurement_Table.station, Measurement_Table.date, Measurement_Table.prcp, Measurement_Table.tobs).all()
    Measurement_df = pd.DataFrame(results[:], columns=['Measurement_Table.id', 'Measurement_Table.station', 'Measurement_Table.date', 'Measurement_Table.prcp', 'Measurement_Table.tobs'])
    Measurement_df.set_index('Measurement_Table.id', inplace=True, )
    # List the stations and the counts in descending order.
    Station_Counts_df = pd.DataFrame(Measurement_df['Measurement_Table.station'].value_counts())
    #Choose the most active station
    Most_Active_Station = Station_Counts_df.index[0]    
    Most_Active_df = Measurement_df.loc[Measurement_df["Measurement_Table.station"] == Most_Active_Station]
    min_temp = Most_Active_df['Measurement_Table.tobs'].min()
    max_temp = Most_Active_df['Measurement_Table.tobs'].max()
    avg_temp = round(Most_Active_df['Measurement_Table.tobs'].mean(),1)

   #Close the session
    session.close()
    #Jsonify
    all_names = list(np.ravel([min_temp, max_temp, avg_temp]))
    return jsonify(all_names)

if __name__ == '__main__':
    app.run(debug=True)
