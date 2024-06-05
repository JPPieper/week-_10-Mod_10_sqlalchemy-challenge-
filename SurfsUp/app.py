# Import the dependencies.
from flask import Flask, jsonify

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

if __name__ == '__main__':
    app.run(debug=True)


#################################################
# Database Setup
#################################################

from flask import Flask, jsonify
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

# Create a Flask app
app = Flask(__name__)

# Create engine and reflect the database
engine = create_engine("sqlite:///your_database_file_name_here.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Define the /api/v1.0/precipitation route
@app.route('/api/v1.0/precipitation')
def precipitation():
    # Create a session
    session = Session(engine)

    # Calculate the date 1 year ago from the last data point in the database
    last_date = session.query(func.max(Base.classes.Measurement.date)).scalar()
    last_date = dt.datetime.strptime(last_date, '%Y-%m-%d')
    one_year_ago = last_date - dt.timedelta(days=365)

    # Query the last 12 months of precipitation data
    results = session.query(Base.classes.Measurement.date, Base.classes.Measurement.prcp).\
        filter(Base.classes.Measurement.date >= one_year_ago).all()

    session.close()

    # Convert the query results to a dictionary with date as key and prcp as value
    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)

if __name__ == '__main__':
    app.run(debug=True)
# reflect an existing database into a new model

# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################




#################################################
# Flask Routes
#################################################
