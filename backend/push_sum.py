from energy_supplier.group import Group
from iota_client import IotaClient
from random import randint
import time
import json
import pandas as pd


class PushSum(object):

    """Helper for the push sum protocol"""
    def __init__(self, value, iota_client, cycle_time_seconds=300, total_rounds=15):

        self._iota_client = iota_client
        self._weight = 1
        self._value = value
        self._address = ps._iota_client.address
        self.group_members = self.get_group_members()
        self.group_count = len(self.group_members)
        self.cycle_time_seconds = cycle_time_seconds
        #How many rounds are there before we send the aggregated push sum
        #value to the energy supplier address?
        self.total_rounds = total_rounds
        #How long does a push sum round take in seconds(in a round we receive message
        #and we send one message to a random receiver)
        self.round_time_seconds = int(cycle_time_seconds/total_rounds)

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
        message = {'value': self._value, 'weight': self._weight}

        return json.dumps(message)

    def send(self):
        # "Send" half of our weight and value to ourselves
        self._weight *= 0.5
        self._value *= 0.5

        # Send other half of our weight and value to random receiver in group
        member = self.get_random_group_member()
        message = self.make_message()
        print(ps.get_random_group_member().public_key)
        self._iota_client.send_transaction(member.address, message, "NUON", 0)

    def _get_cycle_id(self, timestamp=None):
        if not timestamp:
            timestamp = int(time.time())
        round_id = int(timestamp/self.cycle_time_seconds)-5077050
        return round_id

    def _get_cycle_time(self, timestamp=None):
        if not timestamp:
            timestamp = int(time.time())
        round_time = int(timestamp)%self.cycle_time_seconds
        return round_time

    def _get_round_id(self, timestamp=None):
        if not timestamp:
            timestamp = int(time.time())
        round_id = int(timestamp/self.round_time_seconds)
        return round_id

    def _get_round_time(self, timestamp=None):
        if not timestamp:
            timestamp = int(time.time())
        round_time = int(timestamp%self.round_time_seconds)
        return round_time

    def get_round_messages(self, round_id):
        msg_df = self.receive()
        round_msg_df = msg_df[msg_df["round_id"]==round_id].copy()
        round_msg_df = self.parse_value_and_weight_attributes(round_msg_df)
        return round_msg_df

    def receive(self):
        messages = self._iota_client.get_messages_from_address(self._address)
        msg_df = pd.DataFrame(messages)
        msg_df = self.parse_timing_attributes(msg_df)
        return msg_df

    def parse_value_and_weight_attributes(self, round_msg_df):
        round_msg_df["value"] = round_msg_df['json_message'].apply(lambda row: row['value'])
        round_msg_df["weight"] = round_msg_df['json_message'].apply(lambda row: row['weight'])
        del round_msg_df["json_message"]
        return round_msg_df

    def parse_timing_attributes(self, msg_df):
        msg_df["cycle_id"] = msg_df["timestamp"].apply(lambda t: self._get_cycle_id(t))
        msg_df["cycle_time"] = msg_df["timestamp"].apply(lambda t: self._get_cycle_time(t))
        msg_df["round_id"] = msg_df["cycle_time"].apply(lambda t: self._get_round_id(t))
        msg_df["round_time"] = msg_df["cycle_time"].apply(lambda t: self._get_round_time(t))
        del msg_df["timestamp"]
        return msg_df


provider = 'http://node01.testnet.iotatoken.nl:16265'
seed = '9MUBGYDJKKNBESRMZUGLZOWGXLIOBRSDIHKKSLUCQBISU9FP9IYVPEUQQKRDIYYBXOPSWVSJMLTYNWUUV'
client = IotaClient(seed, provider)

ps = PushSum(10, client)
