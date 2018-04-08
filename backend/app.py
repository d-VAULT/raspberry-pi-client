from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
from flask import Flask, send_from_directory, request, jsonify
from iota_client import IotaClient
from push_sum import PushSum
from smart_meter.smart_meter import SmartMeter, SmartMeterProfile
from config import my_public_key, seed, provider
import atexit
import config
import json
import netifaces
import os
import random
import time

# Get LAN ip
interfaces = netifaces.interfaces()
if 'wlan0' in interfaces:
    ip = netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr'].split('.')[3]
else:
    ip = "X"

# Get my identity
print("my public key is: ", my_public_key)
print("my seed is ", seed)
print("my provider is ", provider)

# define the triggering of rounds in one push sum cycle
def do_push_sum_cycle(value, total_rounds, cycle_time):
    start_date_sum = datetime.now() + timedelta(seconds=1)
    end_date_sum = start_date_sum + timedelta(seconds=(cycle_time - 3))

    # poll local meter to get updated value:
    if not value:
        demand = meter.get_data().demand
        supply = meter.get_data().supply
        value = abs(demand) + abs(supply) # this is just for testing
        print("\n\nGOT NEW INITIAL VALUE FOR CYCLE: ", value, "\n\n")

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
        max_instances=4,
        misfire_grace_time = int(cycle_time/total_rounds)-1,
        trigger=IntervalTrigger(start_date=start_date_sum,
                                seconds=round_time_seconds,
                                end_date=end_date_sum),
        id='do_push_sum_cycle',
        name='Perform push sum work',
        replace_existing=False)

    # shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())


# define the triggering of cycles
def start_cycle_scheduler(start_date_cycle, value, total_rounds, cycle_time):
    print("\nCYCLE SCHEDULER STARTED: ", time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

    # initialize scheduler and add job
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=do_push_sum_cycle,
        max_instances=4,
        args=[value, total_rounds, cycle_time],
        misfire_grace_time = int(cycle_time/total_rounds)-1,
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

# set push sum parameters a None value means updating from
value = None
total_rounds = 12
cycle_time = 120

# real start_time = start_date_cycle + N * cycle_time
start_date_cycle = datetime(2018, 4, 8, 00, 00, 0)

# start the clocked cycles scheduler
start_cycle_scheduler(start_date_cycle, value, total_rounds, cycle_time)

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


# Energy supplier overall usage app
# Note: reuses this backend now, can later be moved to own application

@app.route('/api/aggregated-data')
def aggregated_data():
    client = IotaClient(config.seed, config.provider)
    messages = client.get_messages_from_address(
        config.aggregator_address)

    return json.dumps(messages)
