from energy_supplier.group import Group
from iota_client import IotaClient
from random import randint
import json


class PushSum(object):

    """Helper for the push sum protocol"""
    def __init__(self, value, iota_client):

        self._iota_client = iota_client
        self._weight = 1
        self._value = value
        self.group_members = self.get_group_members()
        self.group_count = len(self.group_members)

    @staticmethod
    def get_group_members():
        group = Group()
        return group.group_members

    def get_random_group_member(self):
        idx = randint(0, self.group_count-1)
        return self.group_members[idx]

    # def round():
    #     send()
    #     return None
    #     # receive()

    def make_message(self):
        """Creates a JSON message of our current value and weight"""
        message = {'VALUE': self._value, 'WEIGHT': self._weight}

        return json.dumps(message)

    def send(self):
        # "Send" half of our weight and value to ourselves
        self._weight *= 0.5
        self._value *= 0.5

        # Send other half of our weight and value to random receiver in group
        member = self.get_random_group_member()
        message = self.make_message()
        self._iota_client.send_transaction(member.address, message, "NUON", 0)




    # # def to_json():
    # #     """Convert PushSum object to JSON object"""
    # #     json.

provider = 'http://node01.testnet.iotatoken.nl:16265'
seed = 'RIB9XMREGTUERLVNQBEGRAMNJVKKFWWJLJ9R9RHUYOEDUR9SAEJEWFFDQLWIMBUWFNIDHXVORORNTBGPR'
client = IotaClient(seed, provider)

ps = PushSum(10, client)
