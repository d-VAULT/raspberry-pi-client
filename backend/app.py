import os
import netifaces
from flask import Flask, send_from_directory, request, jsonify
from smart_meter.smart_meter import SmartMeter, SmartMeterProfile

# Get LAN ip
interfaces = netifaces.interfaces()
if 'wlan0' in interfaces:
    ip = netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr'].split('.')[3]
else:
    ip = "X"

app = Flask(__name__, static_folder='../frontend/build')

meter = SmartMeter(SmartMeterProfile(True, False, False));

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
