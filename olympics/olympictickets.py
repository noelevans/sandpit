import datetime
import pickle
import urllib2

from   bs4 import BeautifulSoup


def main():
    sports = {
            'athletics'             : 8194,
            'basketball'            : 8198,
            'canoe slalom'          : 8202,
            'cycling - track'       : 8209,
            'diving'                : 8210,
            'gymnastics - artistic' : 8216,
            'gymnastics - rhythmic' : 8217,
            'handball'              : 8218,
            'hockey'                : 8219,
            'swimming'              : 8225,
            'volleyball'            : 8232,
            'waterpolo'             : 8233,
        }

    templateUrl = 'http://www.tickets.london2012.com/browse?' + \
            'form=search&tab=oly&sport=%d&event=&venue=&fromDate=&' + \
            'toDate=&morning=1&afternoon=1&evening=1&' + \
            'show_available_events=1'

    pickle_file = 'results.pikl'
    now = datetime.datetime.now()

    try:
        results = pickle.load(open(pickle_file))
    except IOError:
        results = dict(
                    map(
                        lambda x : (x, [(0, datetime.datetime.min)] * 5), 
                        sports
                        )
                )

    for sport, code in sports.iteritems():
        url    = templateUrl % code
        output = urllib2.urlopen(url)
        html   = ''.join(output.readlines())
        soup   = BeautifulSoup(html)
        temp   = results[sport][:-1]
        count  = 0
        if soup.find('h2') and soup.find('h2').text == 'Search results':
            table = soup.find('table')
            if table:
                count = len(table.find_all('td', {'headers':'session'}))
                return table
        results[sport] = [(count, now)] + temp

    pickle.dump(results, open(pickle_file, 'w'))

    return results

if __name__ == "__main__":
    results = main()
    for sport, counts in results.iteritems():
		print sport
