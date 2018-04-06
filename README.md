# Raspberry Pi client

## Backend
Initially playground for the IOTA Python client.

Next up:

- https://trello.com/c/cVoAUhER/
- https://trello.com/c/WWLEYZDO/

### Installation

Environment variables:

Generate a seed

```
cat /dev/urandom | LC_ALL=C tr -dc 'A-Z9' | fold -w 81 | head -n 1
```
add this seed in an environment variable SEED.

```
export SEED=<yourseed>
```

## Frontend

Serves the frontend on the display of the Pi. Talks with the backend.
