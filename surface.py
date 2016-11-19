import requests
import json

def getSurface(lat, lon):
    call = 'http://nominatim.openstreetmap.org/reverse.php?format=json&lat=%s&lon=%s&zoom=16&extratags=1' % (lat, lon)
    r = requests.get(call)
    parsed_json = json.loads(r.text)
    extratags = parsed_json['extratags'] 
    return extratags['surface']

def getLocation():
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    return lat, lon

lat, lon = getLocation()
surface = getSurface(lat, lon)
print(surface)
