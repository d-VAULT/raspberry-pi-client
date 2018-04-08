from push_sum import PushSum
from energy_supplier.group_member import GroupMember
from iota_client import IotaClient
import config

provider = 'http://node01.testnet.iotatoken.nl:16265'
test_seed = "PXTWQRHDQLJTELGGTNUKWRSQDLMPBANCICXBZRFF9MFGWXAZJCCJMSK9XOVROC9QFEWRZHMJALTORNDZQ"
client = IotaClient(test_seed, provider)


ps = PushSum(10, client)


def test_init():
    assert len(ps.group_members) == 3


def test_random_group_member():
    member = ps.get_random_group_member()
    assert isinstance(member, GroupMember)


def test_make_message():
    message = ps.make_message()
    assert message[0] == "{"


def test_send_result_to_aggregator():
    ps.send_result_to_aggregator()
    transactions = client.get_messages_from_address(
        config.aggregator_address)

    json = dict.get(transactions[0], 'json_message')
    total_energy_usage = dict.get(json, 'total_energy_usage')

    assert isinstance(total_energy_usage, float)
