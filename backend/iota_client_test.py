from iota_client import IotaClient

provider = 'http://node01.testnet.iotatoken.nl:16265'
seed = 'RIB9XMREGTUERLVNQBEGRAMNJVKKFWWJLJ9R9RHUYOEDUR9SAEJEWFFDQLWIMBUWFNIDHXVORORNTBGPR'
client = IotaClient(seed, provider)

erwin_address = 'DGBTDPFMSOA9UEWMICRRYRPCISQWJGCOXFWCSXHMVTKDKSOVEBE9MHZCEGQDXFGHATCWICSKPSXLUUDMW'

def test_transactions_from_address_are_sorted_on_timestamp():
    transactions = client.get_transactions_on_address(erwin_address)
    assert transactions[0].timestamp > transactions[1].timestamp

def test_messages_from_address_():
    messages = client.get_messages_from_address(erwin_address)
    assert len(messages) == 2
