import os
import sys
import os.path
import time
import platform

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# COMMAND in OSX, CONTROL in linux or windows
if platform.system() == 'Darwin':
	key_new_tab = Keys.COMMAND
else:
	key_new_tab = Keys.CONTROL

class Google:

	def __init__(self, driver):
		self.driver = driver

	# Login to google
	def login(self, username, password):
		self.driver.get('https://accounts.google.com/login')

		# Type email
		email = self.driver.find_element_by_id('identifierId')
		email.send_keys(username)

		# Button Next
		for element in self.driver.find_elements_by_class_name('VfPpkd-LgbsSe'):
			ActionChains(self.driver).click(element).perform()
			break

		# Wait after click
		time.sleep(2)

		# Password
		for element in self.driver.find_elements_by_class_name('whsOnd'):
			element.send_keys(password)
			break

		# Button Next
		for element in self.driver.find_elements_by_class_name('VfPpkd-LgbsSe'):
			ActionChains(self.driver).click(element).perform()
			break

		# Wait after click
		time.sleep(2)

		print("You are logged in")