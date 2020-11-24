import os
import sys
import os.path
import time
import re 

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from domfunctions import get_element_by_inner_text

class CampaignManager:

	def __init__(self, driver):
		self.driver = driver

	def open_unresolved_creatives(self, creatives_url):

		# Go to creatives url
		self.driver.get(creatives_url)

		time.sleep(3)

		# Find alert bar
		header = self.driver.find_elements_by_css_selector('span.ng-binding.ng-scope')
		alert_titlebar = get_element_by_inner_text(header, '^.*in this advertiser have alert.*$', True)

		# Check titlebar found
		if alert_titlebar == False:
			print('Alert titlebar not found. Probably you have no unresolved creatives.')
			return False

		print('Alert titlebar found: ', alert_titlebar.get_attribute('innerText'))

		# Click to alert link
		alert_link = alert_titlebar.find_element_by_css_selector('a')
		ActionChains(self.driver).click(alert_link).perform()

		# Wait until loading
		time.sleep(5)

	def each_in_unresolved_creatives(self):

		creative_number = 0

		alert_icons = self.driver.find_elements_by_css_selector('.dfa-icon.dfa-icon-alert-high-small')

		print('You have ', str(len(alert_icons)), ' unresolved creatives in this page')

		# Each in alert icons
		for alert_icon in alert_icons:

			# Find resolve updates link after hover alert icon
			resolve_update_link = False
			resolve_update_fail = 0
			while resolve_update_link == False:

				try:
					# Hover alert icon
					ActionChains(self.driver).move_to_element(alert_icon).perform()

					time.sleep(1)

					button_elements = self.driver.find_elements_by_css_selector('button')
					resolve_update_link = get_element_by_inner_text(button_elements, 'Resolve updates…')

					ActionChains(self.driver).click(resolve_update_link).perform()
				except:
					print('Try again search resolve button')
					resolve_update_link = False

					resolve_update_fail += 1

					if resolve_update_fail > 10:
						print('Resolve update button not found, skipped it')
						break

				time.sleep(1)

			# Find studio changes radio button
			studio_update_option = self.driver.find_element_by_css_selector('label[for=studio]')
			ActionChains(self.driver).click(studio_update_option).perform()

			# Find continue button
			button_elements = self.driver.find_elements_by_css_selector('button')
			continue_button = get_element_by_inner_text(button_elements, 'Continue')
			ActionChains(self.driver).click(continue_button).perform()

			time.sleep(1)

			# Find overwrite radio
			bold_elements = self.driver.find_elements_by_css_selector('b')
			overwrite_radio_button = get_element_by_inner_text(bold_elements, 'Save current creative')
			ActionChains(self.driver).click(overwrite_radio_button).perform()

			# Find continue button
			button_elements = self.driver.find_elements_by_css_selector('button')
			continue_button = get_element_by_inner_text(button_elements, 'Continue')
			ActionChains(self.driver).click(continue_button).perform()

			time.sleep(1)

			# Find continue button
			button_elements = self.driver.find_elements_by_css_selector('button')
			continue_button = get_element_by_inner_text(button_elements, 'Confirm')
			ActionChains(self.driver).click(continue_button).perform()

			time.sleep(2)

			creative_number += 1

			print(str(len(alert_icons)), '/', str(creative_number), 'creative resolved successfully.')

		print('All creatives successfully resolved')

		return True