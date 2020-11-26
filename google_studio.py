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

from dom_functions import get_element_by_inner_text

# COMMAND in OSX, CONTROL in linux or windows
if platform.system() == 'Darwin':
	key_new_tab = Keys.COMMAND
else:
	key_new_tab = Keys.CONTROL

class GoogleStudio:

	# Go to next page in table
	def go_to_next_page(self, driver):

		time.sleep(5)

		print("Ready to go next page")

		for next_page_icon in driver.find_elements_by_class_name('mat-paginator-navigation-next'):
			if next_page_icon.is_enabled():
				ActionChains(driver).click(next_page_icon).perform()
				print("Next page is enabled")
			else:
				print("Next page is disabled")
				return False

		time.sleep(2)

		return True

	def open_creative_in_new_tab(self, driver, creative_name):

		creatives_tab = driver.current_window_handle
		opened = False
		try_again = 0

		while (opened != True):
			try:
				creative = driver.find_element_by_css_selector("[title='" + creative_name + "'] a")

				print("Opening creative: " + creative_name)

				# Open creative in new tab
				ActionChains(driver).key_down(key_new_tab).click(creative).key_up(key_new_tab).perform()

				time.sleep(1)

				# Go to new tab
				creative_tab = driver.window_handles[1]
				driver.switch_to.window(creative_tab)
				print("You are in the opened creative tab")

				# Success
				opened = True

			except:
				print("Try again to open")
				try_again += 1
				
				if (try_again > 5):
					print("Failed to open creative in new tab")
					return creatives_tab

				time.sleep(5)

		return creatives_tab