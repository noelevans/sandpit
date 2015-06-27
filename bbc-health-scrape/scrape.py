import pyperclip
import re
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


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

    copied_text = pyperclip.paste()
    residential_care, at_home_care = re.findall('[0-9\.]+', copied_text)
    browser.quit()
    return residential_care, at_home_care


def main():
    residential_care, at_home_care = care_costs_for_postcode('ha1 4bj')
    print 'Residential care =', residential_care
    print 'At home care =    ', at_home_care


if __name__ == '__main__':
    main()

