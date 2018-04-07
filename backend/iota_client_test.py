from iota_client import IotaClient
from iota import Address
import json
import time


# Setup

provider = 'http://node01.testnet.iotatoken.nl:16265'
seed = 'FFIPZLAYGDOLJJESXAJNJFBOVJLAIEQDTJXNCLBVRMZVQYRDHIQGZJHBNKY9QSRJSB9ESKNVE9HHIYBKF'
client = IotaClient(seed, provider)
iota_api = client._api

iota_address = iota_api.get_new_addresses(0, 1)['addresses'][0]
address = str(iota_address)


messages_count = 3
messages = [{'value': 0, 'weight': i} for i in range(messages_count)]

for message in messages:
    json_message = json.dumps(message)
    client.send_transaction(address, json_message, 'NUON', 0)


# Test

def test_transactions_from_address_are_sorted_on_timestamp():
    transactions = client.get_transactions_from_address(address)
    assert transactions[0].timestamp >= transactions[1].timestamp


def test_messages_from_address_():
    messages = client.get_messages_from_address(address)
    assert len(messages) > 100


def test_get_messages_contains_timestamp():

    retrieved_messages = client.get_messages_from_address(address)
    timestamp = dict.get(retrieved_messages[0], 'timestamp')

    current_time = int(time.time())

    assert timestamp < current_time
