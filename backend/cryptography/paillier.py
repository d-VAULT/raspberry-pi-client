# -*- coding: utf-8 -*-

from phe import paillier
from config import participants


class Paillier(object):
    """Python public key encryption and partial homomorphic encryption via paillier"""
    def __init__(self, public_key, private_key):
        if not public_key and not private_key:
            public_key, private_key = paillier.generate_paillier_keypair()
        self.public_key = public_key
        self._private_key = private_key

    def encrypt(self, value, public_key=None):
        if not public_key:
            public_key=self.public_key
        return public_key.encrypt(value)

    def decrypt(self, value, private_key=None):
        if not private_key:
            private_key=self._private_key
        return private_key.decrypt(value)

    def decryptcipher(self, cipher, public_key=None, private_key=None):
        if not public_key:
            public_key=self.public_key
        if not private_key:
            private_key=self._private_key
        value = paillier.EncryptedNumber(public_key, cipher)
        return self.decrypt(value, private_key)

    @classmethod
    def from_keypair_dict(cls, keypair_dict):
        public_key, private_key = Paillier._keypair_from_dict(keypair_dict)
        return cls(public_key, private_key)

    def keypair_to_dict(self):
        keypair_dict = self._keypair_to_dict(**self.__dict__)
        return keypair_dict

    @staticmethod
    def _keypair_to_dict(public_key, _private_key):
        public_key_dict = Paillier._public_key_to_dict(public_key)
        private_key_dict = Paillier._private_key_to_dict(_private_key)
        keypair_dict = {"public_key_dict": public_key_dict, "_private_key_dict": private_key_dict}
        return keypair_dict

    @staticmethod
    def _keypair_from_dict(keypair_dict):
        public_key = Paillier._public_key_from_dict(keypair_dict['public_key_dict'])
        private_key = Paillier._private_key_from_dict(**keypair_dict)
        return public_key, private_key

    @staticmethod
    def _public_key_to_dict(public_key):
        public_key_dict = {'n': public_key.n}
        return public_key_dict

    @staticmethod
    def _private_key_to_dict(_private_key):
        private_key_dict = {'p': _private_key.p, 'q': _private_key.q}
        return private_key_dict

    @staticmethod
    def _private_key_from_dict(public_key_dict, _private_key_dict):
        public_key = paillier.PaillierPublicKey(public_key_dict['n'])
        return paillier.PaillierPrivateKey(public_key, **_private_key_dict)

    @staticmethod
    def _public_key_from_dict(public_key_dict):
        return paillier.PaillierPublicKey(public_key_dict['n'])


#for i in range(len(participants)):
#    print("\n\n\n\nkeypair_%s ="%i, Paillier(None, None).keypair_to_dict())
