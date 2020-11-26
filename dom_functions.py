import re
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def get_element_by_inner_text(elements, inner_text, regex = False):

	found_element = False
	current_element_text = ''
	
	while (True):
		try:
			for element in elements:
				current_element_text = element.get_attribute('innerText')

				# By regex
				if (regex == True and re.search(inner_text, current_element_text)):
					found_element = element
					break

				# By text
				if current_element_text.strip() == inner_text:
					found_element = element
					break

			print('Element found: ', current_element_text)
			return found_element

		except:
			print('Try again to find element:', css_selector)
			try_again += 1
			time.sleep(1)
			
			if (try_again > 5):
				print('Failed to find elements by selector:', css_selector)
				return False

def get_elements_by_inner_text(elements, inner_text, regex = False):

	found_elements = []

	while (True):
		try:
			for element in elements:
				current_element_text = element.get_attribute('innerText')

				# By regex
				if (regex == True and re.search(inner_text, current_element_text)):
					found_elements.append(element)

				# By text
				if current_element_text.strip() == inner_text:
					found_elements.append(element)

			print(str(len(found_elements)), 'element(s) found by inner text:', inner_text)
			return found_elements

		except:
			print('Try again to find element:', css_selector)
			try_again += 1
			time.sleep(1)
			
			if (try_again > 5):
				print('Failed to find elements by selector:', css_selector)
				return False

def get_element_until_found(driver, css_selector):
	try_again = 0
	WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
	while (True):
		try:
			element = driver.find_element_by_css_selector(css_selector)
			element.get_attribute('innerText')
			return element
		except:
			print('Try again to find element:', css_selector)
			try_again += 1
			time.sleep(1)
			
			if (try_again > 5):
				print('Failed to find elements by selector:', css_selector)
				return False


def get_elements_until_found(driver, css_selector):
	try_again = 0
	WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
	while (True):
		try:
			element = driver.find_elements_by_css_selector(css_selector)
			element.get_attribute('innerText')
			return element
		except:
			print('Try again to find element:', css_selector)
			try_again += 1
			time.sleep(1)
			
			if (try_again > 5):
				print('Failed to find elements by selector:', css_selector)
				return False