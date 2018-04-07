import json
import random

profileBase = 20
profileBulbValue = 200
profileCarValue = 500
profileWindValue = -200

class SmartMeter:
    def __init__(self, profile):
        self.profile = profile

    def updateProfile(bulb, car, wind):
        self.profile = SmartMeterProfile(bulb, car, wind)

    def get_data(self):
        bulbUsage = profileBulbValue if self.profile.bulb else 0
        usage = profileBase + bulbUsage + random.randint(0, 5)
        return SmartMeterData(usage, 301, 0, 0)

class SmartMeterProfile:
    def __init__(self, bulb, car, wind):
        self.bulb = bulb
        self.car = car
        self.wind = wind

class SmartMeterData:
    def __init__(self, usage, generation, demand, supply):
        self._usage = usage
        self._generation = generation
        self._demand = demand
        self._supply = supply

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=2)
