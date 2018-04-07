from iota_client import IotaClient

provider = 'http://node01.testnet.iotatoken.nl:16265'
seed = 'RIB9XMREGTUERLVNQBEGRAMNJVKKFWWJLJ9R9RHUYOEDUR9SAEJEWFFDQLWIMBUWFNIDHXVORORNTBGPR'
client = IotaClient(seed, provider)

ruud_address = 'VHEPYOKMNPEZRWCGI9INUHBCSDOKCKYXWAYNQAPMRZYOVETIEBFBTKAWIJPFUXLMJEJQCDHJATVRHBIBC'

def test_get_transactions_on_address_are_sorted_on_timestamp():
    transactions = client.get_transactions_on_address(ruud_address)
    assert transactions[0].timestamp > transactions[1].timestamp
