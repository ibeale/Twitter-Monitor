from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json


driver = webdriver.Firefox()
driver.get("https://mobile.twitter.com/login?hide_message=true&redirect_after_login=https%3A%2F%2Ftweetdeck.twitter.com%2F%3Fvia_twitter_login%3Dtrue")
email = driver.find_element_by_name("session[username_or_email]")
password = driver.find_element_by_name("session[password]")
submit = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/form/div/div[3]/div/div')
email.send_keys("IsaacBeale2")
password.send_keys("allstar")
submit.click()
cookieDict = {}
cookieDict["cookie"] = {}
for cookie in driver.get_cookies():
	cookieDict["cookie"][cookie["name"]] = cookie["value"]
with open("cookie.json", "w") as f:
	json.dump(cookieDict, f)

driver.close()