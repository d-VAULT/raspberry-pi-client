import atexit
import netifaces
import os
import random
import time
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask, send_from_directory, request, jsonify
from push_sum import PushSum
from smart_meter.smart_meter import SmartMeter, SmartMeterProfile

# Get LAN ip
interfaces = netifaces.interfaces()
if 'wlan0' in interfaces:
    ip = netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr'].split('.')[3]
else:
    ip = "X"


# define the triggering of rounds in one push sum cycle
def do_push_sum_cycle(value, total_rounds, cycle_time):
    start_date_sum = datetime.now()
    end_date_sum = start_date_sum + timedelta(seconds=cycle_time - 2)

    # report start of new cycle to console
    print("NEW CYCLE STARTED: ", start_date_sum.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    print("CYCLE WILL END AT: ", end_date_sum.strftime("%A, %d. %B %Y %I:%M:%S %p"))

    # initialise push sum object
    ps = PushSum(value,
                 total_rounds=total_rounds,
                 cycle_time_seconds=cycle_time)
    round_time_seconds = ps.round_time_seconds

    # define triggering function and report to console
    def do_push_sum():
        print("PUSH SUM ITERATION: ", time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
        ps.iterate_round()

    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=do_push_sum,
        trigger=IntervalTrigger(start_date=start_date_sum,
                                seconds=round_time_seconds,
                                end_date=end_date_sum),
        id='do_push_sum_cycle',
        name='Perform push sum work',
        replace_existing=False)

    # shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())


# define the triggering of cycles
def start_clocked_cycles(start_date_cycle, value, total_rounds, cycle_time):
    print("CYCLE SCHEDULER STARTED: ", time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

    # initialize scheduler and add job
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=do_push_sum_cycle,
        args=[value, total_rounds, cycle_time],
        trigger=IntervalTrigger(start_date=start_date_cycle,
                                seconds=cycle_time),
        id='start_new_cycle',
        name='Starts a new push sum',
        replace_existing=True)

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())


# set random profile of meter and get value
random_profile = [bool(random.getrandbits(i)) for i in [1, 1, 1]]
meter = SmartMeter(SmartMeterProfile(*random_profile))
value = meter.get_data().demand - meter.get_data().supply

# set push sum parameters
total_rounds = 30
cycle_time = 300

# real start_time = start_date_cycle + N * cycle_time
start_date_cycle = datetime(2018, 4, 8, 00, 00, 1)

# start the clocked cycles scheduler
start_clocked_cycles(start_date_cycle, value, total_rounds, cycle_time)

# initialise the Flask app
app = Flask(__name__, static_folder='../frontend/build')


# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if (path == ""):
        return send_from_directory('../frontend/build', 'index.html')
    else:
        if (os.path.exists("../frontend/build/" + path)):
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
