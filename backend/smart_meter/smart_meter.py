import json
import random

profileBase = 20
profileBulbValue = 200
profileCarValue = 500
profileWindValue = 200

class SmartMeter:
    def __init__(self, profile):
        self.profile = profile

    def updateProfile(self, bulb, car, wind):
        self.profile = SmartMeterProfile(bulb, car, wind)

    def get_data(self):
        bulbUsage = profileBulbValue if self.profile.bulb else 0
        carUsage = profileCarValue if self.profile.car else 0
        windGeneration = profileWindValue + random.randint(-20, 20) if self.profile.wind else 0
        totalUsage = profileBase + bulbUsage + carUsage + random.randint(-10, 10)
        if (totalUsage > windGeneration):
            demand = totalUsage - windGeneration
            supply = 0
        else:
            demand = 0
            supply = windGeneration - totalUsage

        return SmartMeterData(totalUsage, windGeneration, demand, supply)

class SmartMeterProfile:
    def __init__(self, bulb, car, wind):
        self.bulb = bulb
        self.car = car
        self.wind = wind

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

class SmartMeterData:
    def __init__(self, usage, generation, demand, supply):
        self.usage = usage
        self.generation = generation
        self.demand = demand
        self.supply = supply

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)
