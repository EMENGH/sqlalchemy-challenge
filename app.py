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
        f"Home: /api/v1.0/<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of Stations: /api/v1.0/stations<br/>"
        f"Temperature for one year: /api/v1.0/tobs<br/>"
        f"Temperature stat from start to end dates(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )


@app.route('/api/v1.0/<start>')
def get_t_start(start):
    session = Session(engine)
    act_station_stats  = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
                         func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    tobs_array = []
    for date, tobs in data_scope:
        data_tobs = {}
        data_tobs["Date"] = date
        data_tobs["Tobs"] = tobs
        tobs_array.append(data_tobs)

    return jsonify(tobs_array)



@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    col_scope  = [Measurement.date,Measurement.prcp]
    data_scope = session.query(*col_scope).all()
    session.close()
    precipitation = []
    for date, prcp in data_scope:
        data_precip = {}
        data_precip["Date"] = date
        data_precip["Precipitation"] = prcp
        precipitation.append(data_precip)
    return jsonify(precipitation)



@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    station_cols = [Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation]
    station_data = session.query(*station_cols).all()
    session.close()
    stations = []
    for station,name,lat,lon,elev in station_data:
        data_station = {}
        data_station["Station"] = station
        data_station["Name"] = name
        data_station["Lat"] = lat
        data_station["Lon"] = lon
        data_station["Elevation"] = elev
        stations.append(data_station)
    return jsonify(stations)



@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    latest_date_fixed = dt.datetime.strptime(latest_date, '%Y-%m-%d')
    first_date = dt.date(latest_date_fixed.year -1, latest_date_fixed.month, latest_date_fixed.day)
    col_scope = [Measurement.date,Measurement.tobs]
    data_scope = session.query(*col_scope).filter(Measurement.date >= first_date).all()
    session.close()

    tobs_array = []
    for date, tobs in data_scope:
        data_tobs = {}
        data_tobs["Date"] = date
        data_tobs["Tobs"] = tobs
        tobs_array.append(data_tobs)

    return jsonify(tobs_array)


if __name__ == '__main__':
    app.run(debug=True)
