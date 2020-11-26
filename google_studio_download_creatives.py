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
from login import GoogleLogin

# Start process at begin or after condition satisfied
startProcess = True

# Start process from creative name
startProcessFromCreative = ''

# Process only for trafficked creatives
processOnlyTraffickedCreatives = True

uploadingSuccessCount = 0
downloadingSuccessCount = 0

# COMMAND in OSX, CONTROL in linux or windows
key_new_tab = Keys.COMMAND

# Get first creative
def getAllCreativesInPage(driver):

	global startProcess, startProcessFromCreative

	allCreatives = driver.find_elements_by_css_selector('tbody .mat-column-CREATIVE_NAME')
	allCreativeNames = []

	# Each in elements
	for creative in allCreatives:
		creativeName = creative.get_attribute('innerText')
		tableRow = creative.find_element_by_xpath('..')
		creativeStatus = tableRow.find_element_by_css_selector('.mat-column-STATUS').get_attribute('innerText')

		print('Creative status: ', creativeStatus)

		# Add creative if reach the specified creative name
		if startProcess == True:
			if processOnlyTraffickedCreatives == True:
				if creativeStatus == 'Trafficked':
					allCreativeNames.append(creativeName)
			else:
				allCreativeNames.append(creativeName)
		
		# If creative is the specified creative
		if (startProcessFromCreative != '' and creativeName.lower() == startProcessFromCreative.lower()):
			startProcess = True

	print(str(len(allCreativeNames)) + " creatives started to process")
	print(*allCreativeNames, sep = ", ")  
	
	return allCreativeNames


def downloadAllCreatives(driver, campaignUrl):

	global downloadingSuccessCount

	# Go to google studio creatives
	driver.get(campaignUrl)

	time.sleep(2)

	# Each in pages
	while True:

		# Get All Creative Names
		allCreativeNames = getAllCreativesInPage(driver)

		# Each in creative names
		creativeIndex = 0
		for creativeName in allCreativeNames:
			print("Find for creative: " + creativeName + " " + str(len(allCreativeNames)) + "/" + str(creativeIndex + 1) + " Success: " + str(downloadingSuccessCount))

			if download_creative(driver, creativeName) == True:
				print("Creative downloaded successfully: " + str(len(allCreativeNames)) + "/" + str(creativeIndex + 1) + " Success: " + str(downloadingSuccessCount))
			else: 
				print("Creative not needed to download, or failed")

			creativeIndex += 1

		print("All creatives downloading finished in page. Ready to go next page.")

		if go_to_next_page(driver) == False:
			print("Next page button is disabled!!! - It means process finished")
			break

	return True

def download_creative(driver, creativeName):

	time.sleep(2)

	print("Creative Name: " + creativeName)

	# Check file is already downloaded
	fname = os.path.expanduser('~') + "/Downloads/" + creativeName.lower() + ".zip"
	print("Check file is existing: " + fname)
	if os.path.isfile(fname):
		print("File already downloaded, so skip it: " + fname)
		return False
			
	creatives_tab = openCreativeInNewTab(driver, creativeName)

	# Wait until loading
	time.sleep(5)

	# Find download button and click it
	downloadIcon = get_element_by_inner_text(driver.find_elements_by_tag_name('mat-icon'), 'save_alt')

	# Downloading started
	if downloadIcon != False:
		ActionChains(driver).click(downloadIcon).perform()
		print("Downloading started")
	else:
		print("Download button not found, its not a problem if really there are no button")

	time.sleep(12)

	# Close current tab
	driver.close()

	# Switch to creatives list tab
	driver.switch_to.window(creatives_tab)

	print("You are in Creatives page")

	return True
