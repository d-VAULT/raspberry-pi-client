from push_sum import PushSum
from energy_supplier.group_member import GroupMember
from iota_client import IotaClient

provider = 'http://node01.testnet.iotatoken.nl:16265'
client = IotaClient(seed, provider)

# Random seed for tests
seed = "MPGFTSGNYSEYSCYQCXTTNWALGVKLSIYTICRRCIJBPYITUENBQESGBYOCSVGBUOWUTKLVUOEIDSZAYNXIA"


ps = PushSum(10, client)


def test_init():
    assert len(ps.group_members) == 3


def test_random_group_member():
    member = ps.get_random_group_member()
    assert isinstance(member, GroupMember)


def test_make_message():
    message = ps.make_message()
    assert message[0] == "{"
