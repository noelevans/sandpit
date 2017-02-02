import numpy as np
import requests
import unicornhat as hat
 
 
URL = 'https://api.tfl.gov.uk/Line/Mode/tube,overground,dlr/Status'
 
LINES = [
    'bakerloo', #
    'central',  #
    'circle',   #
    'district',
    'dlr',
    'hammersmith-city',
    'jubilee',  #
    'metropolitan', #
    'northern',  #
    'london-overground', #
    'piccadilly',  #
    'victoria', #
    'waterloo-city',
    ]
 
STATUSES = {'Good Service': 'GOOD',
            'Minor Delays': 'OK'}   # Otherwise status is 'BAD'
 
def update():
    requests.packages.urllib3.disable_warnings()
    resp = requests.get(URL).json()
 
    statuses = {el['id']: el['lineStatuses'][0]['statusSeverityDescription']
                for el in resp}
    return {k: STATUSES.get(statuses[k], 'BAD') for k in statuses.keys()}
 
 
def reset():
    hat.off()
 
 
def reset_for_coloring():
    hat.brightness(0.1)
    hat.set_pixel(x, y, r, g, b)
    hat.show()
 
 
def main():
    status = update()
    met_status = status.pop('metropolitan')
 
 
if __name__ == '__main__':
    main()