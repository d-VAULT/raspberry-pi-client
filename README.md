# Raspberry Pi client [![BCH compliance](https://bettercodehub.com/edge/badge/Blockchaingers/raspberry-pi-client?branch=master)](https://bettercodehub.com/)

## Backend
Performs a push sum algorithm via smart meters connected with the IOTA Tangle to determine the aggregate energy usage in a group belonging to an energy supplier.

Communications between the meters is encrypted so that the energy supplier cannot see individual usage. Weight in the push sum is homomorphically encrypted with the public key of the energy supplier so that only the energy supplier can see the total sum.

Next up:

- https://trello.com/c/cVoAUhER/
- https://trello.com/c/WWLEYZDO/

### Installation

Install [the Python](https://conda.io/docs/user-guide/install/index.html).

Install dependencies on Raspberry Pi:
```

# brew install libmpc mpfr gmp

# for windows only
# get wheel files https://www.lfd.uci.edu/~gohlke/pythonlibs/
pip install gmpy2-2.0.8-cp36-cp36m-win_amd64.whl
pip install netifaces‑0.10.6‑cp36‑cp36m‑win_amd64.whl

# for linux only
sudo apt-get install python3-pandas

pip install -r requirements.txt
pip install pyota[ccurl]
```

Set time zone to Europe/Amsterdam:
```
sudo dpkg-reconfigure tzdata
```

Environment variables:

Generate a seed

```
cat /dev/urandom | LC_ALL=C tr -dc 'A-Z9' | fold -w 81 | head -n 1
```
add this seed in an environment variable SEED.

```
export SEED=<yourseed>
```

### Tests

Install dependencies:

```
pip install pytest
```

Run tests with:

```
pytest
```

## Frontend

Serves the frontend on the display of the Pi. Talks with the backend.

- Install NodeJS
- `cd frontend`
- `yarn install`
- `yarn start` (to run the development version that proxies the backend)
- `yarn build` (to generate production version for the Pi)
