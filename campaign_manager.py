import os
import sys
import os.path
import time
import re 
import platform

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from dom_functions import get_element_by_inner_text, get_element_until_found

# COMMAND in OSX, CONTROL in linux or windows
if platform.system() == 'Darwin':
	key_new_tab = Keys.COMMAND
else:
	key_new_tab = Keys.CONTROL

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

	def dynamic_targeting_key_factory(self, creatives_url = '', dynamic_targeting_keys = []):

		# Go to creatives url
		self.driver.get(creatives_url)

		time.sleep(5)

		creative_index = 0
		creative_rows = self.driver.find_elements_by_css_selector('.name-col .label-box-link')

		for creative_row in creative_rows:

			dtk_index = 0
			creative_name = creative_row.get_attribute('innerText')

			print('Creative', creative_name, ' started to check. Process:', str(creative_index + 1), '/', str(len(creative_rows)))

			# If dynamic targeting key is already created, skip it
			dynamic_targeting_keys_regex = '^.*(' + '|'.join(dynamic_targeting_keys) + ').*$'

			if re.search(dynamic_targeting_keys_regex, creative_name):
				print('Dynamic Targeting key found in creative name:', creative, '.Creative skipped.')
				continue

			# Each in dynamic targeting keys
			for dynamic_targeting_key in dynamic_targeting_keys:

				print('Creative', creative_name, 'started to copy and associate with dynamic targeting key. ', dynamic_targeting_key, '. Process:', str(creative_index + 1), '/', str(len(creative_rows)))

				# Open creative properties in new tab
				creatives_tab = self.driver.current_window_handle
				self.open_creative_in_new_tab(creative_row)
				time.sleep(1)

				# Duplicate creative
				self.copy_creative(creative_name, dynamic_targeting_key)
				time.sleep(1)

				# Set dynamic targeting key
				self.set_dynamic_targeting_key(creative_name, dynamic_targeting_key)
				time.sleep(1)

				# Press to save button
				save_button = self.driver.find_element_by_css_selector('.submit-button.primary-button')
				ActionChains(self.driver).click(save_button).perform()

				# Go back to all creatives tab
				self.driver.close()
				self.driver.switch_to.window(creatives_tab)

				print('Creative successfully associated with dynamic targeting key:', dynamic_targeting_key, 'Process:', str(dtk_index + 1), '/', str(len(dynamic_targeting_keys)))

				dtk_index += 1

			creative_index += 1 

		return True



	def open_creative_in_new_tab(self, creative_row_element):

		# Open creative in new tab
		ActionChains(self.driver).key_down(key_new_tab).click(creative_row_element).key_up(key_new_tab).perform()

		# Go to the new tab
		creative_tab = self.driver.window_handles[1]
		self.driver.switch_to.window(creative_tab)
		print('You are in the opened creative tab')

		return True



	def copy_creative(self, creative_name = 'Triumph_Sculpt_Prospecting_Message_1_300x250', dynamic_targeting_key = 'Message_11'):

		new_creative_name = self.get_creative_name(creative_name, dynamic_targeting_key)

		print('Started to copy creative', creative_name, 'to name', new_creative_name)

		time.sleep(5)

		# Click to copy button
		copy_button = get_element_until_found(self.driver, '.button-copy')
		ActionChains(self.driver).click(copy_button).perform()

		time.sleep(5)

		# Wait until creative copied
		creative_name_input = get_element_until_found(self.driver, '#creativeName')
		ActionChains(self.driver).click(creative_name_input).perform()
		creative_name_input.clear()
		creative_name_input.send_keys(new_creative_name)
		print('Creative copied successfully')

		return True



	def set_dynamic_targeting_key(self, creative_name = 'Triumph_Sculpt_Prospecting_Message_1_300x250', dynamic_targeting_key = 'Message_11'):

		# Wait until collapse did not show
		WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.dfa-collapsiblepanel')))

		# Click to collapse Dynamic targeting keys
		collapses = self.driver.find_elements_by_css_selector('.dfa-collapsiblepanel')
		dynamic_targeting_key_collapse = get_element_by_inner_text(collapses, '^.*Dynamic targeting keys.*$', True)
		dynamic_targeting_key_link = dynamic_targeting_key_collapse.find_element_by_css_selector('a')
		ActionChains(self.driver).click(dynamic_targeting_key_link).perform()
		print('Dynamic targeting key section collapsed')

		time.sleep(1)

		# Click to Assign Targeting Key Button
		spans = self.driver.find_elements_by_css_selector('span')
		assign_key_button = get_element_by_inner_text(spans, 'Assign targeting key')
		ActionChains(self.driver).click(assign_key_button).perform()
		print('Assign targeting key button pressed')

		time.sleep(1)

		# Find Dynamic Targeting key input field
		dynamic_targeting_key_input = self.driver.find_element_by_css_selector('.inline-edit-container.inline-edit-dropdown.ddm-inline-edit-position-element .omnilist-search-container input')
		dynamic_targeting_key_input.click()
		dynamic_targeting_key_input.send_keys(dynamic_targeting_key)
		print('Search for', dynamic_targeting_key)

		time.sleep(1)

		# Find for create new option
		dynamic_targeting_key_options = self.driver.find_elements_by_css_selector('.omnilist-body a')
		create_new_button = get_element_by_inner_text(dynamic_targeting_key_options, '^.*create new.*$', True)

		if create_new_button != False:

			# Press to create new button
			ActionChains(self.driver).click(create_new_button).perform()
			print('Dynamic targeting key created successfully', dynamic_targeting_key)

		else:

			# Find button for add the dynamic targeting key
			dynamic_targeting_key_option = self.driver.find_element_by_css_selector('a')
			dynamic_targeting_key_option = get_element_by_inner_text(dynamic_targeting_key_options, '^.*' + dynamic_targeting_key + '.*$', True, re.IGNORECASE)
			ActionChains(self.driver).click(dynamic_targeting_key_option).perform()
			print('Dynamic targeting selected successfully', dynamic_targeting_key)

		return True


	# Get creative name with dynamic targeting key
	# Triumph_Sculpt_Prospecting_300x250 + Message_11 = Triumph_Sculpt_Prospecting_Message_11_300x250 
	def get_creative_name(self, creative_name = 'Triumph_Sculpt_Prospecting_300x250', dynamic_targeting_key = 'Message_11'):

		creative_name_array = creative_name.split('_')
		creative_dimension = creative_name_array.pop()

		creative_name_array.append(dynamic_targeting_key)
		creative_name_array.append(creative_dimension)

		return '_'.join(creative_name_array)
