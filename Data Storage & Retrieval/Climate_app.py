#Step 2 - Climate App
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Climate = Base.classes.climate

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

#Home page.
# List all routes that are available.
@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
# Convert the query results to a Dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation")
def prcp():
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    rain_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()
    prcp = []
    for date, prcp in rain_results:
        prcp_dict = {}
        prcp_dict["date"] = name
        prcp_dict["pcrp"] = age
        prcp.append(prcp_dict)
    
    # Return the JSON representation of your dictionary.
    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset.
    stations = session.query(Stations.station).all()
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # query for the dates and temperature observations from a year from the last data point.
    tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_ago).all()
    # Return a JSON list of Temperature Observations (tobs) for the previous year.
    return jsonify(tobs)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
@app.route("/api/v1.0/<start>")
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
def start(start_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    Args:
        start_date (string): A date string in the format %Y-%m-%d
    Returns:
        TMIN, TAVG, and TMAX
    """
    selected_start = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    return jsonify(selected_start)

@app.route("/api/v1.0/<start>/<end>")
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
def startend(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
    Returns:
        TMIN, TAVG, and TMAX
    """
    selected_start_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    return jsonify(selected_start_end)

if __name__ == "__main__":
    app.run(debug=True)