import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create path to access and query SQLite database file
engine = create_engine(f"sqlite:///Resource/hawaii.sqlite")

# Create baseline 
Base = automap_base()
# reflect our tables
Base.prepare(engine, reflect=True)

# save references to each table
# create a variable for each of the classes 
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database
session = Session(engine)

# create a Flask application called "app."
app = Flask(__name__)

# Create new route welcome
@app.route("/")
# Create welcome function 
def welcome():
    return(
    # Add routes we'll need 
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Create new route percipitation
@app.route("/api/v1.0/precipitation")
# Create precipitation function
def precipitation():
    # Add code to the function
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Add query to fucntion to get date and percipitation
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    # jsonify dictionary: convert dictionary to a json file
    precip = {date: prcp for date, prcp in precipitation}  
    return jsonify(precip)

# Create new route stations
@app.route("/api/v1.0/stations")
# create dtations function
def stations():
    # Create query to get all stations from our database 
    results = session.query(Station.station).all()
    # 1. unravel results (np.ravel()) 
    # 2. convert unraveled results to list (list())
    stations = list(np.ravel(results))
    # 3. jsonify list (jsonify()) ==> stations=staions to format lists into JSON
    return jsonify(stations=stations)

# Create new route temperature
@app.route("/api/v1.0/tobs")
# create temperature function
def temp_monthly():
    # calculate date from one year ago
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # query primary station for all temp observations from previous year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    # unravel and convert to list
    temps = list(np.ravel(results))
    #jsonify list
    return jsonify(temps=temps)

# Create new routes statistics 
# starting date route
@app.route("/api/v1.0/temp/<start>")
# ending date route
@app.route("/api/v1.0/temp/<start>/<end>")
# Create stats function
# Add start and end paramaters
def stats(start=None, end=None):
    # query select min, avg, max temps
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    # Add if-not statment to determine starting amd ending date
    if not end: 
        # (*sel) indicates we will multiple results for our query 
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)
    
    # query to calculate tmep min, avg, max with start and end dates
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)