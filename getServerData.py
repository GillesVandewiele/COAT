import requests
from restServer import SERVER_IP, HOST_IP

def getHeartbeats():
    call = 'http://%s:%s/coat/get_heartbeats' % (str(SERVER_IP), str(HOST_IP))
    r = requests.get(call)
    return r.text

def getAccelerations():
    call = 'http://%s:%s/coat/get_accelerations' % (str(SERVER_IP), str(HOST_IP))
    r = requests.get(call)
    return r.text

print getHeartbeats()
print getAccelerations()
