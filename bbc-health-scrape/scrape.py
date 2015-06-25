from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


browser = webdriver.Firefox()
browser.get('http://www.bbc.co.uk/news/health-30990913')

# inner_frame = browser.find_elements(By.XPATH, '//iframe')[1]
inner_frame = browser.find_elements_by_xpath('//iframe')[1]
inner_frame.send_keys(Keys.ENTER)
inner_frame.send_keys(Keys.TAB)
inner_frame.send_keys(Keys.ENTER)
inner_frame.send_keys(Keys.TAB)
inner_frame.send_keys(Keys.TAB)
inner_frame.send_keys('ha1 4bj')
inner_frame.send_keys(Keys.ENTER)

browser.quit()
