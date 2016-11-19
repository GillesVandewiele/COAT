import pyowm
import requests
import json

def getCurrentTemperature(owm, lat, lon):
    observation = owm.weather_at_coords(lat,lon)
    w = observation.get_weather()

    return w.get_temperature('celsius')['temp']  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

def getCurrentHumidity(owm, lat, lon):
    observation = owm.weather_at_coords(lat,lon)
    w = observation.get_weather()

    return w.get_humidity()

def getBelATMOIndex():
    call = 'http://www.irceline.be/~celinair/forecast/model/belatmo.php?lang=nl'
    r = requests.get(call)
    lines = r.content.split('\n')
    inFlanders = False
    count = 0
    for line in lines:
        if 'Vandaag (Voorspellingen)' in line and 'td' in line:
            count += 1
            if count == 2:
                prediction = line.split(">")[1].split("<")[0]
                predictionDescription = prediction.split("-")[0].strip()
                predictionNumber = prediction.split("-")[1].strip()
                return predictionDescription, predictionNumber
    return None, None

def getLocation():
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    return lat, lon

key = '4bc83e656c41b62834160b643ec0801a'
openweathermap = pyowm.OWM(key)
lat, lon = getLocation()
print 'Current temperature at lat = %s, lon = %s: %s degrees Celcius.' % (str(lat), str(lon), str(getCurrentTemperature(openweathermap, lat, lon)))
print 'Current humidity at lat = %s, lon = %s: %s%%.' % (str(lat), str(lon), str(getCurrentHumidity(openweathermap, lat, lon)))

ATMODescr, ATMONumber = getBelATMOIndex()
print 'ATMO index is: %s (%s)' % (str(ATMODescr), str(ATMONumber))
