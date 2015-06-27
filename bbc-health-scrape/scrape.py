import pyperclip
import re
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import postcodes


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
    browser.quit()

    copied_text = pyperclip.paste()
    occurrences = re.findall('[0-9\.]+', copied_text)
    if len(occurrences) == 2:
        residential, at_home = occurrences
        return residential, at_home
    return '?', '?'


def main():
    dist_posts = postcodes.district_postcodes('postcodes.grouped.csv')
    for district, postcode in dist_posts.itertuples():
        residential_care, at_home_care = care_costs_for_postcode(postcode)
        print 'District,Postcode,Residential care, At home care'
        print ','.join((district, postcode, residential_care, at_home_care))


if __name__ == '__main__':
    main()
