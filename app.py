#Import dependencies

import numpy as np 
import datetime as dt 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session 
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Set up the Database and Engines

engine = create_engine('sqlite:///Resources/hawaii.sqlite')

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

#Set up Flask

app = Flask(__name__)

#Establish Flask routes

@app.route('/')
def welcome():
    '''List all available api routes.'''
    return(
        f'Available Routes:br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start><br/>'
        f'/api/v1.0/<start>/<end><br/>'
    )


@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    queryresults = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-24').all()

    session.close()

    prcp_data = []
    for date, prcp in queryresults:
        prcp_dictionary = {}
        prcp_dictionary['date'] = date
        prcp_dictionary['prcp'] = prcp 

        prcp_data.append(prcp_dictionary)

    return jsonify(prcp_data)


@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    queryresults = session.query(Station.station).\
        order_by(Station.station).all()

    session.close()

    station_data = list(np.ravel(queryresults))

    return jsonify(station_data)


@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    queryresults = session.query(Measurement.date, Measurement.tobs, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.station == 'USC00519281').\
        order_by(Measurement.date).all()

    session.close()

    tobs_data = []
    for prcp, date, tobs in queryresults:
        tobs_dictionary = {}
        tobs_dictionary['prcp'] = prcp
        tobs_dictionary['date'] = date
        tobs_dictionary['tobs'] = tobs

        tobs_data.append(tobs_dictionary)


@apps.route('/api/v1.0/<start>')
def Start(start):
    session = Session(engine)
    queryresults = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()

    session.close()

    start_tobs = []
    for min, avg, max in results:
        start_tobs_dictionary = {}
        start_tobs_dictionary['min_temp'] = min
        start_tobs_dictionary['avg_temp'] = avg
        start_tobs_dictionary['max_temp'] = max
        start_tobs.append(start_tobs_dictionary) 
    
    return jsonify(start_tobs)


@app.route('/api/v1.0/<start>/<end>')
def Start_end(start, end):
    session = Session(engine)
    queryresults = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()
  
    start_end_data = []
    for min, avg, max in results:
        start_end_data_dict = {}
        start_end_data_dict['min_temp'] = min
        start_end_data_dict['avg_temp'] = avg
        start_end_data_dict['max_temp'] = max
        start_end_data.append(start_end_data_dict) 
    

    return jsonify(start_end_data)

if __name__ == '__main__':
    app.run(debug=True)


