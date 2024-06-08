# Import the dependencies.
from flask import Flask, jsonify
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

# Create engine and reflect the database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
# reflect the tables
measurement = Base.classes.measurement
Station = Base.classes.station
# Create a Flask app
app = Flask(__name__)

# Define the homepage route
@app.route('/')
def home():
    # List all the available routes
    routes = {
        "routes": [
            "/",
            "/api/v1.0/precipitation",
            "/api/v1.0/stations",
            "/api/v1.0/tobs",
            "/api/v1.0/<start>",
            "/api/v1.0/<start>/<end>"
        ]
    }
    
    return jsonify(routes)





# Define the /api/v1.0/precipitation route
@app.route('/api/v1.0/precipitation')
def precipitation():
    # Create a session
    session = Session(engine)

    # Calculate the date 1 year ago from the last data point in the database
    last_date = session.query(func.max(Base.classes.measurement.date)).scalar()
    last_date = dt.datetime.strptime(last_date, '%Y-%m-%d')
    one_year_ago = last_date - dt.timedelta(days=365)

    # Query the last 12 months of precipitation data
    results = session.query(Base.classes.measurement.date, Base.classes.measurement.prcp).\
        filter(Base.classes.measurement.date >= one_year_ago).all()

    session.close()

    # Convert the query results to a dictionary with date as key and prcp as value
    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)


# Define the /api/v1.0/stations route
@app.route('/api/v1.0/stations')
def stations():
# Create a session
    session = Session(engine)

    # Query the stations from the database
    results = session.query(Station.station).all()
    session.close()
    # Convert the query results to a JSON list of stations
    station_list = [result[0] for result in results]

    return jsonify(station_list)



# Define the /api/v1.0/tobs route
@app.route('/api/v1.0/tobs')
def tobs():
    # Create a session
    session = Session(engine)
    # Query the most active station
    most_active_station = session.query(measurement.station).\
        group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).first()[0]

    # Calculate the date 1 year ago from the last data point in the database
    last_date = session.query(func.max(measurement.date)).scalar()
    last_date = dt.datetime.strptime(last_date, '%Y-%m-%d')
    one_year_ago = last_date - dt.timedelta(days=365)

    # Query the temperature observations for the most active station for the previous year
    results = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == most_active_station).\
        filter(measurement.date >= one_year_ago).all()
    session.close()
    # Convert the query results to a JSON list of temperature observations
    tobs_list = [{"date": result[0], "tobs": result[1]} for result in results]

    return jsonify(tobs_list)


# Define the /api/v1.0/<start> route
@app.route('/api/v1.0/<start>')
def temp_start(start):
    # Create a session
    session = Session(engine)
    # Query the minimum, average, and maximum temperatures for dates greater than or equal to the start date
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()
    session.close()
    # Convert the query results to a JSON response
    temp_stats = {
        "start_date": start,
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    return jsonify(temp_stats)

# Define the /api/v1.0/<start>/<end> route
@app.route('/api/v1.0/<start>/<end>')
def temp_range(start, end):
    # Create a session
    session = Session(engine)
    # Query the minimum, average, and maximum temperatures for the date range from start to end
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()
    # Convert the query results to a JSON response
    temp_stats = {
        "start_date": start,
        "end_date": end,
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    return jsonify(temp_stats)






if __name__ == '__main__':
    app.run(debug=True)


