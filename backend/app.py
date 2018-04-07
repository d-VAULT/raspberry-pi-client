import os
import netifaces
from flask import Flask, send_from_directory, request, jsonify
from smart_meter.smart_meter import SmartMeter, SmartMeterProfile
import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta

from push_sum import PushSum

# Get LAN ip
interfaces = netifaces.interfaces()
if 'wlan0' in interfaces:
    ip = netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr'].split('.')[3]
else:
    ip = "X"

# set push sum parameters
value = 10
total_rounds = 30

def do_push_sum_cycle(value, total_rounds, start_date_sum):
    ps = PushSum(value, total_rounds=total_rounds)
    round_time_seconds = ps.round_time_seconds

    def do_push_sum():
        print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
        ps.iterate_round()

    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=do_push_sum,
        start_date=start_date_sum,
        trigger=IntervalTrigger(seconds=round_time_seconds),
        id='do_push_sum_cycle',
        name='Perform push sum work',
        replace_existing=False)

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())


def start_new_cycle(value, total_rounds, start_date_cycle):

    start_date_sum = start_date_cycle + timedelta(seconds=2)
    scheduler = BackgroundScheduler()
    scheduler.start()

    scheduler.add_job(
        func=do_push_sum_cycle,
        args=[value, total_rounds, start_date_sum],
        trigger=DateTrigger(start_date_cycle),
        id='start_new_cycle',
        name='Starts a new push sum',
        replace_existing=False)

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())


#push_sum_object = PushSum(value, total_rounds=total_rounds)
#ps = push_sum_object
#do_push_sum_cycle(value, total_rounds, ps)
start_date_cycle = datetime(2018, 4, 8, 00, 25, 1)
start_new_cycle(value, total_rounds, start_date_cycle)



meter = SmartMeter(SmartMeterProfile(True, False, False))

app = Flask(__name__, static_folder='../frontend/build')

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if(path == ""):
        return send_from_directory('../frontend/build', 'index.html')
    else:
        if(os.path.exists("../frontend/build/" + path)):
            return send_from_directory('../frontend/build', path)
        else:
            return send_from_directory('../frontend/build', 'index.html')

# Serve API backend
@app.route('/api/identity')
def identity():
    return jsonify({
        'succes': True,
        'identity': "I am meter " + ip,
        'profile': {
            'bulb': meter.profile.bulb,
            'car': meter.profile.car,
            'wind': meter.profile.wind
        }
    }), 200

@app.route('/api/update-profile', methods=['POST'])
def update_profile():
    if not request.json or not 'car' in request.json:
        abort(400)
    meter.updateProfile(request.json['bulb'], request.json['car'], request.json['wind'])
    return jsonify({
        'succes': True,
        'profile': {
            'bulb': meter.profile.bulb,
            'car': meter.profile.car,
            'wind': meter.profile.wind
        }
    }), 200

@app.route('/api/data')
def data():
    return meter.get_data().toJSON()
