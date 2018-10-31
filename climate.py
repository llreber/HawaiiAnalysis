import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"/api/v1.0/start_date (date format YYYY-MM-DD)<br/>"
        f"/api/v1.0/start_date/end_date (date format YYYY-MM-DD)"
    )


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of precip by date"""

    #latest_date = '2017-08-23'
    one_year_ago = '2016-08-23'

    # Query all dates
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > one_year_ago).all()

    # Create a dictionary from the row data and append to a list of all_dates
    all_dates = []
    for item in results:
        precip_dict = {}
        precip_dict["date"] = item.date
        precip_dict["prcp"] = item.prcp
        all_dates.append(precip_dict)

    return jsonify(all_dates)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temps by date"""

    #latest_date = '2017-08-23'
    one_year_ago = '2016-08-23'

    # Query all dates
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > one_year_ago).all()

    # Create a dictionary from the row data and append to a list of all_dates
    all_temps = []
    for item in results:
        temp_dict = {}
        temp_dict["date"] = item.date
        temp_dict["tobs"] = item.tobs
        all_temps.append(temp_dict)

    return jsonify(all_temps)

@app.route("/api/v1.0/<start_date>")
def start_date(start_date):
    """Return a list of temps by date"""

    # Query all dates
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    # Create a dictionary from the row data and append to a list of all_temp_data
    all_temp_data = list(np.ravel(results))

    return jsonify(all_temp_data)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
    """Return a list of temps by date"""

    # Query all dates
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    # Create a dictionary from the row data and append to a list of all_temp_data
    all_temp_data2 = list(np.ravel(results))

    return jsonify(all_temp_data2)

if __name__ == '__main__':
    app.run(debug=True)
