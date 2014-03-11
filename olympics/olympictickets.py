import datetime
import os
import pprint
import re
import time
import urllib2

from   bs4 import BeautifulSoup


def make_soup(url):
    try:
        output = urllib2.urlopen(url)
        html   = ''.join(output.readlines())
    except urllib2.HTTPError as ex:
        html = ''
        print 'x ',
    return BeautifulSoup(html)
    
def available_tickets(paralympics=False):
    result = []
    sports = { 
        'olympics' : {
                'Athletics'             : 8194,
                'Basketball'            : 8198,
                'Canoe slalom'          : 8202,
                'Cycling - track'       : 8209,
                'Diving'                : 8210,
                'Gymnastics - artistic' : 8216,
                'Gymnastics - rhythmic' : 8217,
                'Hockey'                : 8219,
                'Olympic park'          : 8269,
                'Swimming'              : 8225,
                'Volleyball'            : 8232,
                'Waterpolo'             : 8233,
            },
        'paralympics' : {
                'Athletics'             : 8247,
                'Closing ceremony'      : 8267,
                'Opening ceremony'      : 8266,
            }
        }

    summary_template_url = 'http://www.tickets.london2012.com/browse?' + \
            'form=search&tab=%s&sport=%d&event=&venue=&fromDate=&' + \
            'toDate=&morning=1&afternoon=1&evening=1&' + \
            'show_available_events=1'
    details_template_url = 'http://www.tickets.london2012.com/' + \
            'eventdetails?id=%s'
    lookup = 'paralympics' if paralympics else 'olympics'
    now = datetime.datetime.now()
    tab = 'para' if paralympics else 'oly'

    for sport, code in sports[lookup].iteritems():
        url    = summary_template_url % (tab, code)
        soup   = make_soup(url)
        if soup.find('h2') and soup.find('h2').text == 'Search results':
            table = soup.find('table')
            if table:
                for elem in table.find_all('input', {'value':'Select'}):
                    row = elem.parent.parent.parent.parent
                    event_id  = row.find('input', {'name':'id'}).attrs['value']
                    details_url = details_template_url % event_id
                    details_soup = make_soup(details_url)
                    event_info = details_soup.find('table', {'title':'Ticket Summary'})
                    date_tag = details_soup.find('td', text='Date')
                    date = date_tag.nextSibling.nextSibling.text if date_tag else None
                    time_tag = details_soup.find('td', text='Time')
                    time = time_tag.nextSibling.nextSibling.text if time_tag else None
                    option_tags = details_soup.find_all('option', {'price':True})
                    if option_tags:
                        cost_texts = map(lambda x : x.text, option_tags)
                        costs = map(lambda x : re.findall('[0-9.]+', x)[0], cost_texts)
                        min_cost = min(map(lambda x : float(x), costs))
                        result.append({
                                'sport' : sport, 
                                'date'  : date, 
                                'time'  : time, 
                                'url'   : details_url, 
                                'cost'  : min_cost
                            })
    return result

if __name__ == "__main__":
    while True:
        time.sleep(2)
        print datetime.datetime.now().time()
        result = available_tickets()
        if result:
            break
        break
    pprint.pprint(result) if result else None
    os.system('cvlc /usr/share/sounds/gnome/default/alerts/glass.ogg vlc://quit')
