from flask import Flask
import requests


app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Dashboard</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
{contents}
</body>
</html>
"""

def journey_delay(src, dst):
    url = (
        'https://maps.googleapis.com/maps/api/distancematrix/json?' +
       'origins={src}&destinations={dst}&' +
       'departure_time=now&key=AIzaSyAtJv4e_WfKBWQdrL-G3uSImQs4TUMkV18')

    requests.packages.urllib3.disable_warnings()
    resp = requests.get(url.format(src=src, dst=dst)).json()
    times = resp['rows'][0]['elements'][0]
    duration = times['duration']['value']
    traffic_duration = times['duration_in_traffic']['value']
    seconds_delay = traffic_duration - duration
    minutes_delay = int(round(seconds_delay / 60.0))
    return minutes_delay


@app.route('/')
def commuting():
    home = '51.5852123,-0.3404418'
    nursery = '51.5758402,-0.3496415'
    outward = journey_delay(home, nursery)
    zuruch = journey_delay(nursery, home)

    text = (
        '<p>Travelling from home to nursery delay: {} mins</p>' +
        '<p>From nursery to home: {} mins</p>')
    return HTML.format(contents=text.format(outward, zuruch))
