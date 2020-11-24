import os
import sys
import os.path
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from domfunctions import get_element_by_inner_text

class GoogleStudio:

	# Go to next page in table
	def go_to_next_page(self, driver):

		time.sleep(5)

		print("Ready to go next page")

		for nextPageIcon in driver.find_elements_by_class_name('mat-paginator-navigation-next'):
			if nextPageIcon.is_enabled():
				ActionChains(driver).click(nextPageIcon).perform()
				print("Next page is enabled")
			else:
				print("Next page is disabled")
				return False

		time.sleep(2)

		return True

	def open_creative_in_new_tab(self, driver, creativeName):

		creatives_tab = driver.current_window_handle
		opened = False
		try_again = 0

		while (opened != True):
			try:
				creative = driver.find_element_by_css_selector("[title='" + creativeName + "'] a")

				print("Opening creative: " + creativeName)

				# Clicked
				ActionChains(driver).key_down(keyWhichNeededToPressWhenClickToUrlInNewTab).click(creative).key_up(keyWhichNeededToPressWhenClickToUrlInNewTab).perform()

				time.sleep(1)

				# Go to new tab
				creative_tab = driver.window_handles[1]
				driver.switch_to.window(creative_tab)
				print("You are clicked to creative")

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