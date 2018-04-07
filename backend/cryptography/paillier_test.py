# -*- coding: utf-8 -*-
from cryptography.paillier import Paillier
from phe import generate_paillier_keypair

def test_from_keypair():
    public_key, private_key = generate_paillier_keypair()
    p = Paillier(public_key, private_key)

    keypair = p.keypair_to_dict()

    Paillier._keypair_from_dict(keypair)
    p2 = Paillier.from_keypair_dict(keypair)
    assert(p2.public_key == p.public_key)

def test_get_keys():
    public_key, private_key = generate_paillier_keypair()
    p = Paillier(public_key, private_key)

    public_key_dict = p._public_key_to_dict(p.public_key)
    private_key_dict = p._private_key_to_dict(p._private_key)

    public = p._public_key_from_dict(public_key_dict)
    private = p._private_key_from_dict(public_key_dict, private_key_dict)

    assert(public == p.public_key)
    assert(private == p._private_key)