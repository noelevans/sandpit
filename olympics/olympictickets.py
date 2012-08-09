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
    
def available_tickets():
    result = []
    sports = {
            'athletics'             : 8194,
            'basketball'            : 8198,
            'canoe slalom'          : 8202,
            'cycling - track'       : 8209,
            'diving'                : 8210,
            'gymnastics - artistic' : 8216,
            'gymnastics - rhythmic' : 8217,
            'hockey'                : 8219,
            'olympic park'          : 8269,
            'swimming'              : 8225,
            'volleyball'            : 8232,
            'waterpolo'             : 8233,
        }

    summary_template_url = 'http://www.tickets.london2012.com/browse?' + \
            'form=search&tab=oly&sport=%d&event=&venue=&fromDate=&' + \
            'toDate=&morning=1&afternoon=1&evening=1&' + \
            'show_available_events=1'
    details_template_url = 'http://www.tickets.london2012.com/' + \
            'eventdetails?id=%s'
    now = datetime.datetime.now()

    for sport, code in sports.iteritems():
        url    = summary_template_url % code
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
                        if min_cost <= 80:
                            result.append((sport, date, time, details_url))
    return result

if __name__ == "__main__":
    result = available_tickets()
    pprint.pprint(result) if result else None
    os.system('cvlc /usr/share/sounds/gnome/default/alerts/glass.ogg')
