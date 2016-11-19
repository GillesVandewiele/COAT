import thread
from flask import Flask, request, abort, jsonify
from flask.ext.restful import Resource, Api

MAX_SIZE_HEARTBEATS = 5
heartbeats = []

MAX_SIZE_ACCELERATIONS = 5
accelerations = []

SERVER_IP = '10.1.71.93'
HOST_IP = 8001

# Default Flask stuff.
app = Flask(__name__)
# Default Flask Restful stuff.
api = Api(app)

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# Start the restful server.
def start_restfulserver():
    if True:
	    # public
        app.run(host=SERVER_IP, port=HOST_IP)
    else:
        # local
        app.run(debug=True, port=HOST_IP)

def push_heartbeat(heartbeat):
    global heartbeats
    if isInt(heartbeat):
        while len(heartbeats) >= MAX_SIZE_HEARTBEATS:
            heartbeats.pop(0)
            print 'Removing heartbeat: %'
        if len(heartbeats) < MAX_SIZE_HEARTBEATS:
            heartbeats.append(int(heartbeat))
            print heartbeats

def push_acceleration(acceleration):
    global accelerations
    if isInt(acceleration):
        while len(accelerations) >= MAX_SIZE_ACCELERATIONS:
            accelerations.pop(0)
            print 'Removing acceleration: %'
        if len(accelerations) < MAX_SIZE_ACCELERATIONS:
            accelerations.append(int(acceleration))
            print accelerations

@app.route('/coat/heartbeat', methods=['POST'])
def post_heartbeat():
    global heartbeats
    print 'DATA: %s' % request.data
    push_heartbeat(request.data)
    print heartbeats
    return 'OK', 200

@app.route('/coat/acceleration', methods=['POST'])
def post_acceleration():
    global accelerations
    print 'DATA: %s' % request.data
    push_acceleration(request.data)
    print accelerations
    return 'OK', 200

@app.route('/coat/get_heartbeats', methods=['GET'])
def get_heartbeats():
    print 'Getting heartbeats.'
    return str(heartbeats), 200

@app.route('/coat/get_accelerations', methods=['GET'])
def get_accelerations():
    print 'Getting accelerations.'
    return str(accelerations), 200

# Run this only if the script is ran directly.
if __name__ == '__main__':
    try:
        print 'Starting the server...'
        start_restfulserver()
        print 'Started the server...'
    except Exception, err:
        print 'Caught FATAL exception: %s' % str(err)
