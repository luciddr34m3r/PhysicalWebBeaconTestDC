import datetime
import time
import useragents
import config

from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

# Load system configurations
DEBUG = config.DEBUG
SQLALCHEMY_DATABASE_URI = config.SQLALCHEMY_DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = config.SQLALCHEMY_TRACK_MODIFICATIONS

# Load user agent configurations
USER_AGENTS = useragents.USER_AGENTS

# Initialize the application
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)


# Create the object we would like to display
# In this case, it's any request with the user agent
class SiteHit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(255))
    ip = db.Column(db.String(255))
    useragent = db.Column(db.String(255))
    beaconid = db.Column(db.Integer)

    def __init__(self, timestamp, ip, useragent, beaconid):
        self.timestamp = timestamp
        self.ip = ip
        self.useragent = useragent
        self.beaconid = beaconid


# Default route
@app.route('/')
def index():

    # Bounce to a nice non-commercial tourist map
    return redirect('http://washington.org/dc-map')


# Beacon target
@app.route('/<int:beacon_id>')
def log_interaction(beacon_id):
    # Log the beacon interaction
    toLog = {}

    # Get the current time
    ts = time.time()
    toLog['timestamp'] = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    # Pull the source IP
    toLog['ip'] = request.remote_addr

    # Pull the user agent
    toLog['ua'] = request.headers.get('User-Agent')

    # Create the object
    newHit = SiteHit(toLog['timestamp'], toLog['ip'], toLog['ua'], beacon_id)

    # Commit the record
    db.session.add(newHit)
    db.session.commit()

    # Now that it's logged, send them somewhere else
    return redirect(url_for('index'))


# Show results page
@app.route('/results/')
@app.route('/results/<int:beacon_id>')
def results(beacon_id=-1):
    if beacon_id == -1:
        hits = SiteHit.query.all()
    else:
        hits = SiteHit.query.filter_by(beaconid=beacon_id)

    return render_template('show_results.html', hits=hits)


# Initialize the db if it is not already
db.create_all()

if __name__ == '__main__':
    app.run(debug=DEBUG)
