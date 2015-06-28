import pandas as pd
import pyperclip
import random
import re
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


random.seed(101)

def care_costs_for_postcode(postcode):
    browser = webdriver.Firefox()
    actions = ActionChains(browser)
    browser.get('http://www.bbc.co.uk/news/health-30990913')

    inner_frame = browser.find_elements_by_xpath('//iframe')[1]
    inner_frame.send_keys(Keys.ENTER)
    inner_frame.send_keys(Keys.TAB)
    inner_frame.send_keys(Keys.ENTER)
    inner_frame.send_keys(Keys.TAB)
    inner_frame.send_keys(Keys.TAB)
    inner_frame.send_keys(postcode)
    inner_frame.send_keys(Keys.ENTER)

    time.sleep(2)

    actions.send_keys(Keys.CONTROL, 'f')
    actions.send_keys(Keys.CONTROL, 'weekly average rate')
    actions.send_keys(Keys.ESCAPE).perform()

    actions.move_to_element(inner_frame)
    actions.click()
    actions.perform()

    time.sleep(2)

    for i in range(100):
        actions.send_keys(Keys.SHIFT, Keys.ARROW_RIGHT)

    actions.perform()

    actions.send_keys(Keys.CONTROL, 'c').perform()
    copied_text = pyperclip.paste() or ''
    browser.quit()

    occurrences = re.findall('[0-9\.]+', copied_text)
    if len(occurrences) == 2:
        residential, at_home = occurrences
        return residential, at_home


def randomised(ol):
    random.shuffle(ol)
    return iter(ol)


def care_costs_for_postcodes(postcodes):
    for p in randomised(postcodes):
        res = care_costs_for_postcode(p)
        if res:
            return res + (p,)
    return (-1, -1, p)


def district_postcodes(filename):
    # read csv file
    df = pd.read_csv(filename, sep=',')[['Postcode', 'District']]
    district_to_postcodes = {}
    for i, postcode, district in df.itertuples():
        district_to_postcodes.setdefault(district, []).append(postcode)
    return district_to_postcodes


def main():
    dist_posts = district_postcodes('postcodes.simple.ew.csv')
    print 'District,Postcode,Residential care,At home care'
    for district, postcodes in dist_posts.iteritems():
        residential, at_home, postcode = care_costs_for_postcodes(postcodes)
        print ','.join((district, postcode, residential, at_home))


if __name__ == '__main__':
    main()
