from energy_supplier.group import Group
from iota_client import IotaClient
from random import randint
import config
import time
import json
from pandas import DataFrame
from config import seed, provider, participants


class PushSum(object):
    """Helper for the push sum protocol"""

    def __init__(self, value, client=None, cycle_time_seconds=300, total_rounds=15):
        if not client:
            self._iota_client = IotaClient(seed, provider)
        else:
            self._iota_client = client
        self._weight = float(1)
        self._value = float(value)
        self._address = self._iota_client.address
        self.group_members = self.get_group_members()
        self.group_count = len(self.group_members)
        self.cycle_time_seconds = cycle_time_seconds

        # How many rounds are there before we send the aggregated push sum
        # value to the energy supplier address?
        self.total_rounds = total_rounds

        # How long does a push sum round take in seconds(in a round we receive
        # message and we send one message to a random receiver)
        self.round_time_seconds = int(cycle_time_seconds/total_rounds)

    @staticmethod
    def get_group_members():
        group = Group(participants)
        return group.group_members

    def get_random_group_member(self):
        idx = randint(0, self.group_count-1)
        member = self.group_members[idx]
        # get new member if member is self
        if member.address == self._address:
            member = self.get_random_group_member()
        return member

    def make_message(self):
        """Creates a JSON message of our current value and weight"""
        message = {'value': self._value, 'weight': self._weight}

        return json.dumps(message)

    def get_total(self):
        total = (self._value/self._weight)*self.group_count
        return total

    def send_result_to_aggregator(self):
        """Sends total result to aggregator's address"""
        total = self.get_total()
        message = json.dumps({'total_energy_usage': total})
        tag = "AGGREGATED"
        iota_val = 0

        self._iota_client.send_transaction(
            config.aggregator_address,
            message,
            tag,
            iota_val)

        # print aggregated value
        print("\n\nCYCLE COMPLETED SUCCESSFULLY\nAGGREGATED TOTAL: ", total, "\n\n")

    def iterate_round(self, tag=None):
        round_index = self._get_round_index()
        round_id = self._get_round_id()
        print("*** round index: ", round_index)

        if round_index == self.total_rounds-1:
            self.send_result_to_aggregator()
        elif round_index > 0:
            # half our weight and value
            self._weight *= 0.5
            self._value *= 0.5

            # collect all recieved data from previous round
            prev_round_data_sum = ps.get_round_messages(round_id-1).sum()

            print("\nreceived:\n",
                  "\nvalue:", round(prev_round_data_sum['value'],2),
                  "\nweight:", round(prev_round_data_sum['weight'],2))

            # add previous round data to internal data
            self._value += prev_round_data_sum['value'] * 0.5
            self._weight += prev_round_data_sum['weight'] * 0.5

        # print total
        print("\ncurrent values:\n",
              "\nvalue:", round(self._value, 2),
              "\nweight:", round(self._weight,2),
              "\nresult:", round(self.get_total(),2))

        # select random group member for sending current value pair
        member = self.get_random_group_member()

        # for backend demo purposes
        print("\n*** encrypting data")

        # compose mesage for selected group member
        message = self.make_message()

        # for backend demo purposes
        print("*** composing message")

        # send message containing value pair to selected group member
        self._iota_client.send_transaction(member.address, message, "NUON", 0)

        # print public key as a reference for testing
        print("*** sent homomorphic encrypted data to: ",
              member.public_key, "\n")

    def _get_cycle_id(self, timestamp=None):
        if not timestamp:
            timestamp = int(time.time())
        round_id = int(timestamp/self.cycle_time_seconds)-5077050
        return round_id

    def _get_cycle_time(self, timestamp=None):
        if not timestamp:
            timestamp = int(time.time())
        round_time = int(timestamp) % self.cycle_time_seconds
        return round_time

    def _get_round_id(self, timestamp=None):
        if not timestamp:
            timestamp = int(time.time())
        round_id = int(timestamp/self.round_time_seconds)
        return round_id

    def _get_round_time(self, timestamp=None):
        if not timestamp:
            timestamp = int(time.time())
        round_time = int(timestamp % self.round_time_seconds)
        return round_time

    def _get_round_index(self, round_id=None):
        if not round_id:
            round_id = self._get_round_id()
        round_index = int(round_id % self.total_rounds)
        return round_index

    def get_round_messages(self, round_id):
        msg_df = self.receive()
        round_msg_df = msg_df[msg_df["round_id"]==round_id].copy()
        round_msg_df = self.parse_value_and_weight_attributes(round_msg_df)
        return round_msg_df

    def receive(self):
        messages = self._iota_client.get_messages_from_address(self._address)
        msg_df = DataFrame(messages)
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
        msg_df["round_id"] = msg_df["timestamp"].apply(lambda t: self._get_round_id(t))
        msg_df["round_time"] = msg_df["timestamp"].apply(lambda t: self._get_round_time(t))
        msg_df["round_index"] = msg_df["round_id"].apply(lambda t: self._get_round_index(t))
        del msg_df["timestamp"]
        return msg_df


ps = PushSum(value=10, total_rounds=30)
