# -*- coding: utf-8 -*-

import json

from phe import paillier, generate_paillier_keypair

class Paillier(object):
    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self._private_key = private_key

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
        keypair_dict = {"public_key_dict":public_key_dict, "_private_key_dict":private_key_dict}
        return keypair_dict

    @staticmethod
    def _keypair_from_dict(keypair_dict):
        public_key = Paillier._public_key_from_dict(keypair_dict['public_key_dict'])
        private_key = Paillier._private_key_from_dict(**keypair_dict)
        return public_key, private_key

    @staticmethod
    def _public_key_to_dict(public_key):
        public_key_dict = {'g': public_key.g, 'n': public_key.n}
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


#        keys = ['g', 'n']
#        d = public_key.__dict__
#        public_key_dict = {k: d[k] for k in keys}



#        serialised = json.dumps(public_key)
#        return serialised


#        enc_with_one_pub_key = {}
#        enc_with_one_pub_key['public_key'] = {'g': public_key.g, 'n': public_key.n}
#        enc_with_one_pub_key['values'] = [(str(x.ciphertext()), x.exponent) for x in encrypted_number_list

def test_Paillier():
    public_key, private_key = paillier.generate_paillier_keypair()

    p = Paillier(public_key, private_key)

    #p = Paillier().from_json(keypair_dict)

    pubkd = p._public_key_to_dict(p.public_key)
    prikd = p._private_key_to_dict(p._private_key)

    #print (pubkd, prikd)

    public = p._public_key_from_dict(pubkd)
    private = p._private_key_from_dict(pubkd, prikd)

    #print(public)
    #print(private)

    keypair = p.keypair_to_dict()

    p._keypair_from_dict(keypair)
    p2 = Paillier.from_keypair_dict(keypair)
    assert(p2.public_key == p.public_key)