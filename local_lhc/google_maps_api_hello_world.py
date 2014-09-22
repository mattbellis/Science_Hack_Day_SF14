import requests


city = "SanFrancisco"
state = "CA"

url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s,+%s&sensor=true" % (city,state)


r = requests.get(url)
print r
print
print r.json()
print
print r.json()['results']
print

coords = r.json()['results'][0]['geometry']['location']
print coords
print coords['lat']
print coords['lng']
