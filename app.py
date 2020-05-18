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


@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    col_scope  = [Measurement.date,Measurement.prcp]
    data_scope = session.query(*col_scope).all()
    session.close()

    precipitation = []
    for date, prcp in data_scope:
        precip_data = {}
        precip_data["Date"] = date
        precip_data["Precipitation"] = prcp
        precipitation.append(precip_data)

    return jsonify(precipitation)




@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    station_cols = [Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation]
    station_data = session.query(*station_cols).all()
    session.close()

    stations = []
    for station,name,lat,lon,elev in station_data:
        station_data = {}
        station_data["Station"] = station
        station_data["Name"] = name
        station_data["Lat"] = lat
        station_data["Lon"] = lon
        station_data["Elevation"] = elev
        stations.append(station_data)

    return jsonify(stations)



@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_passengers = []
    for name, age, sex in results:
        passenger_dict = {}
        passenger_dict["name"] = name
        passenger_dict["age"] = age
        passenger_dict["sex"] = sex
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)
