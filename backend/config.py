import os

from iota import Iota
import random

seed = os.environ['SEED']

aggregator_address = 'XBC9JOMDXVRTS9VRLULWYBHNGK9BMYMQKKZFDNFFHTJCNCT9LQJQQIBF9PEAUZVRPCRDMXFONZLSYBVJA'

#provider = 'http://node01.testnet.iotatoken.nl:16265'
idx = random.randint(0,2)
providers = ['http://node02.iotatoken.nl:14265', 'http://node04.iotatoken.nl:14265', 'http://node06.iotatoken.nl:14265']
provider = providers[idx]

ruud = {"seed": "",
        "address": '',
        "public_key": "public key ruud"
        }

oelfier = {"seed": "",
           "address": '',
           "public_key": "public key ruud"
           }

erwin = {"seed": "",
         "address": '',
         "public_key": "public key erwin"
         }

timen = {"seed": "",
         "address": '',
         "public_key": "public key timen"
         }

pi_oelfier = {"seed": "",
              "address": '',
              "public_key": "public key oelfier"
              }

pi_dennis = {"seed": "",
             "address": '',
             "public_key": "public key dennis"
             }

pi_ruud = {"seed": "",
           "address": '',
           "public_key": "public key pi_ruud"
           }

pi_timen = {"seed": "",
            "address": '',
            "public_key": "public key pi_timen"
            }

pi_erwin = {"seed": "",
            "address": '',
            "public_key": "public key pi_erwin"
            }

# hard coded participants, group members can later be retrieved on public
seed0 = "DPPNHEJ9PGROXNPBRECSIYUOKFMSLUFRUNQYPHPHMFWKOULBD9DWYBKGCAFDSAND9QZUJWCJBWQVAAQUE"
seed1 = "JSAJXFLOAG9OYSVUMTZQPUAHOGNIMXYTOTAFFIQDFFSAGKFBQYUEKVVIX9NYSUNOZYNW9NEIW9ITKPXXC"
seed2 = "MJCK9UKUVFQNZIDHXRR9FWIRCWVMKFCANXSLUFKQXBHRW9GIAWPGLAXMNNCSVKKOQKQEPFABTHDWMCGLF"
seed3 = "RJ9VORTJMMZQULDZNQCNAWUBUXSWMEFBFPLMXPIALREFXZEWSRZ9OFULCEQPHTLIYBZTWQVZ9XEFZUHMT"
seed4 = "FQJS9VVKGQUMNOYMGNMIFFNTYX9RAAJILCANWK9QGLPNIVXC9OPOFZFAJT9JNFIOOKSCMATCURYIQPBCO"
seed5 = "OHAACETQGUN9IDOGCUPEBMBLTLXL9SSSJVWLULIOIVSTOFSIXEZSNQLBQFOFNAPGJNZMOYYSRYH9ZKVQW"
seed6 = "XXJEC9FSUOYOMSLCNWETP9XROWHMHVNZL9VRKSVNAIGQZJOBKJE9WGLABMRTTCMUX9PCMGRQPROHGNWTD"
seed7 = "CBBIAMDVIWZY9JSCOGTKOBXUQIPDAYRED9JKZIJKRRAULBMHQNZGUZQ9AASBKMZJUYGSFLNUWNKYCNHEK"
seed8 = "QLNYFKJJTW9XLHCUYYHIOSVVDILWZYBTZOOXCOFLSYCJWMX9LZJFHXZTBSA9KHOVEYN9VHVOCRSHFSWQO"

ruud["seed"] = seed0
erwin["seed"] = seed1
timen["seed"] = seed2
pi_oelfier["seed"] = seed3
pi_dennis["seed"] = seed4
pi_ruud["seed"] = seed5
pi_timen["seed"] = seed6
pi_erwin["seed"] = seed7
oelfier["seed"] = seed8

def get_addres_iota(provider, seed):
    address = Iota(provider, seed).get_new_addresses(0, 1)['addresses'][0]
    return str(address)

ruud["address"] = get_addres_iota(provider, seed0)
erwin["address"] = get_addres_iota(provider, seed1)
timen["address"] = get_addres_iota(provider, seed2)
pi_oelfier["address"] = get_addres_iota(provider, seed3)
pi_dennis["address"] = get_addres_iota(provider, seed4)
pi_ruud["address"] = get_addres_iota(provider, seed5)
pi_timen["address"] = get_addres_iota(provider, seed6)
pi_erwin["address"] = get_addres_iota(provider, seed7)
oelfier["address"] = get_addres_iota(provider, seed8)

# define participants
participants = [ruud, erwin, timen, oelfier, pi_ruud, pi_erwin, pi_timen]

# check who I am with seed from env seed = os.environ['SEED']
def who_am_I(seed):
    pubkey = [part["public_key"] for part in participants if part["seed"]==seed]
    return pubkey

# get my public key
my_public_key = who_am_I(seed)
