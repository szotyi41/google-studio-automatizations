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

from google_studio import GoogleStudio

class GoogleStudioUploading(GoogleStudio):

	uploading_success_count = 0

	def upload_creatives_from_folder(self, driver, campaign_url, folder):

		# Set 0 success count
		self.uploading_success_count = 0

		# Go to google studio creatives
		driver.get(campaign_url)

		time.sleep(2)

		# Each in pages
		while True:

			# Get All Creative Names
			all_creative_names = self.get_all_creatives_in_page(driver)

			# Each in creative names
			creative_index = 0
			for creative_name in all_creative_names:

				print('Find for creative:', creative_name, str(len(all_creative_names)), '/', str(creative_index + 1), ' Success: ', str(self.uploading_success_count))

				# Creative folder where you upload from
				creative_folder = folder + '/' + creative_name

				# If creative directory exists
				if os.path.isdir(creative_folder) != True:
					print('Creative folder not exists for uploading: ', creative_folder)
					continue

				# Open creative tab
				creatives_tab = open_creative_in_new_tab(driver, creative_name)

				if upload_creative(driver, creative_folder) == True:
					print('Creative uploaded successfully:', creative_name, str(len(all_creative_names)), '/', str(creative_index + 1), ' Success: ', str(self.uploading_success_count))

				# Close current tab
				driver.close()

				# Switch back to creatives list tab
				driver.switch_to.window(creatives_tab)

				print('You are came back to Creatives tab')

				creative_index += 1

			# Success message
			print("All creatives uploading finished in page. Ready to go next page.")

			# Try to go next page
			if go_to_next_page(driver) == False:
				print("Next page button is disabled!!! - It means process finished")
				break

		return True

	def create_creatives_from_folder(self, driver, creatives_folder, account_name = 'Addressable Content', advertiser_name = 'Triumph_HK_Wavemaker', campaign_name = 'Triumph_TW'):

		creative_index = 0
		already_exists_creatives = []
		all_creative_names = os.listdir(creatives_folder)

		# Each in creatives at folder
		for folder_name in all_creative_names:

			# .DS_Store is not a folder
			if folder_name == '.DS_Store':
				continue

			print('Creative begin to create in more sizes: ', folder_name)

			for creative_size in os.listdir(creatives_folder + '/' + folder_name):

				# Creative name
				creative_name = folder_name + '_' + creative_size

				print('Find for creative:', creative_name, str(creative_index + 1), ' success:', str(self.uploading_success_count))

				# Creative folder where you upload from
				creative_folder = creatives_folder + '/' + folder_name + '/' + creative_size

				# If creative directory exists
				if os.path.isdir(creative_folder) != True:
					print('Creative folder not exists for uploading: ', creative_folder)
					continue

				# Uploading started in size
				size = creative_size.split('x')
				creative_width = size[0]
				creative_height = size[1] 

				print('Creative begin to create in size: ', creative_name, '. Go to create creative page')

				driver.get('https://www.google.com/doubleclick/studio/#creative/new:')


				# Account input
				account_input = driver.find_element_by_css_selector('#mat-input-6')
				account_input.send_keys(account_name)

				time.sleep(3)

				# Advertiser input
				advertiser_input = driver.find_element_by_css_selector('#mat-input-4')
				advertiser_input.send_keys(advertiser_name)

				time.sleep(3)

				# Campaign input
				campaign_input = driver.find_element_by_css_selector('#mat-input-5')
				campaign_input.send_keys(campaign_name)

				time.sleep(3)

				# Creative Name input
				creative_input = driver.find_element_by_css_selector('#mat-input-3')
				creative_input.send_keys(creative_name)

				time.sleep(1)

				# Format select
				format_select = driver.find_element_by_css_selector('#mat-select-2')
				ActionChains(driver).click(format_select).perform()

				time.sleep(1)

				format_select_options = driver.find_elements_by_css_selector('span.mat-option-text')
				banner_select_option = get_element_by_inner_text(format_select_options, 'Banner')
				ActionChains(driver).click(banner_select_option).perform()

				time.sleep(1)
				
				# Find select options
				format_select = driver.find_element_by_css_selector('#mat-select-4')
				ActionChains(driver).click(format_select).perform()

				time.sleep(1)

				format_select_options = driver.find_elements_by_css_selector('span.mat-option-text')
				banner_select_option = get_element_by_inner_text(format_select_options, 'User defined')
				ActionChains(driver).click(banner_select_option).perform()

				time.sleep(1)

				# Set width and height
				width_input = driver.find_element_by_css_selector('#mat-input-7')
				width_input.send_keys(creative_width)
				height_input = driver.find_element_by_css_selector('#mat-input-8')
				height_input.send_keys(creative_height)

				time.sleep(1)

				# Find submit button
				submit_button = driver.find_element_by_css_selector('button[type=submit]')
				ActionChains(driver).click(submit_button).perform()

				time.sleep(5)

				print('Creative submitted for uploading.')

				status_bar = driver.find_elements_by_css_selector('.status')
				if (status_bar and get_element_by_inner_text(status_bar, '^.*creative with this name already exists.*$', True)):
					print('Creative already exists. Continue with the next creative')
					already_exists_creatives.append(creative_name)
					continue

				# Upload creative
				self.upload_creative(driver, creatives_folder + '/' + creative_name)

				print('Creative successfully uploaded:', creative_index, '/', str(len(all_creative_names)))

				creative_index += 1

		print(self.uploading_success_count, ' creative(s) successfully uploaded')				


	def upload_creative(self, driver, creative_folder):

		print('Upload creative from folder: ', creative_folder)

		# Find delete button
		# deleteButton = get_element_by_inner_text(driver.find_elements_by_css_selector('.action-button .mat-button-wrapper'), 'Delete')

		# If delete button found
		# if deleteButton != False:

			# Click to select all checkbox
			# selectAllCheckbox = driver.find_element_by_css_selector('#mat-checkbox-3')
			# ActionChains(driver).click(selectAllCheckbox).perform()

			# Click to delete button
			# ActionChains(driver).click(deleteButton).perform()

		# Press upload assets button, and click anywhere else to open file uploader
		time.sleep(5)

		upload_assets_button = get_element_by_inner_text(driver.find_elements_by_css_selector('.action-button .mat-button-wrapper'), 'Upload assets')
		ActionChains(driver).context_click(upload_assets_button).perform()

		time.sleep(5)

		# Each in files and add to uploading list
		fileUploaderElement = driver.find_element_by_css_selector('input[type=file]')

		print('File uploader element found.')

		files = []
		lastfile = ''
		for file in os.listdir(creative_folder):
			files.append(creative_folder + '/' + file)
			print('File added to uploading list: ', file)
			lastfile = file

		# Uploading files file.txt\n file2.txt
		fileUploaderElement.send_keys('\n'.join(files))

		# Wait 120 seconds or until uploading finished
		WebDriverWait(driver, 120).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '.upload-status')))

		print('Uploading finished successfully')

		self.uploading_success_count += 1

		return True




 