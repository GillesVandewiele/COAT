from restServer import SERVER_IP, HOST_IP

def getHeartbeats():
    call = '%s:%s/coat/get_heartbeats' % (str(SERVER_IP), str(HOST_IP))
    r = requests.get(call)

def getAccelerations():
    call = '%s:%s/coat/get_accelerations' % (str(SERVER_IP), str(HOST_IP))
    r = requests.get(call)
