from flask import Flask
app = Flask(__name__)

@app.route('/api/identity')
def identity():
    return 'I am Pi number 5'
