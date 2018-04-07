# -*- coding: utf-8 -*-
import json

from iota import Iota, Address, ProposedTransaction, Tag, TryteString, Transaction, Fragment


class IotaClient(object):
    """Python IOTA client wrapper"""
    def __init__(self, seed, provider, depth=5, min_weight_magnitude=9):
        self._api = Iota(provider, seed)
        self._depth = depth
        self._min_weight_magnitude = min_weight_magnitude
        self.address = self._get_address()

    @staticmethod
    def _compose_transaction(address, msg, tag, val):
        txn = \
            ProposedTransaction(
                address=Address(address),
                message=TryteString.from_unicode(msg),
                tag=Tag(tag),
                value=val
            )
        return txn

    def _get_address(self):
        address = self._api.get_new_addresses(0, 1)['addresses'][0]
        return str(address)

    def get_transactions_from_address(self, address):
        """
        Gets transaction object from address sorted on timestamp (from latest
        to earliest).

        :param address:
           Address to fetch transaction from

        """
        transactions = self._api.find_transactions(addresses=[address])
        transaction_hashes = transactions['hashes']

        if not transaction_hashes:
            raise ValueError("No transactions on address")

        trytes = self._api.get_trytes(transaction_hashes)['trytes']

        trytes_and_hashes = list(zip(trytes, transaction_hashes))

        transactions = list(map(lambda pair:
                                Transaction.from_tryte_string(
                                    pair[0],
                                    pair[1]
                                ),
                                trytes_and_hashes))

        sorted_transactions = sorted(transactions,
                                     key=lambda t: t.timestamp,
                                     reverse=True)

        return sorted_transactions

    def get_messages_from_address(self, address):
        """
        Gets messages (sorted by timestamp).
        Returns a dict with 'json_message' and 'timestamp keys'

        :param address:
           Address to fetch messages from

        """
        sorted_transactions = self.get_transactions_from_address(address)
        messages = list(map(lambda t: {'json_message': json.loads(Fragment.as_string(t.signature_message_fragment)),
                                       'timestamp': t.timestamp},
                            sorted_transactions))

        return messages

    @staticmethod
    def get_message(transaction):
        message = transaction['signature_message_fragment'].decode()
        json_message = json.loads(message)
        return json_message

    def send_transaction(self, address, msg, tag, val):
        txn = self._compose_transaction(Address(address), msg, tag, val)
        mwm = self._min_weight_magnitude
        depth = self._depth
        self._api.send_transfer(depth, [txn], None, None, mwm)
