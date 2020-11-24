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

from google import Google
from google_studio_uploading import GoogleStudioUploading

driver = webdriver.Chrome()

google = Google(driver)
google.login('me19@mediasales.hu', 'aMUNATION1')

creatives_url = 'https://www.google.com/doubleclick/studio/#campaign:campaignId=60230577&advertiserId=60089177&ownerId=9729573'
creatives_folder = os.getcwd() + '/Triumph' # os.path.expanduser('~') + '/Documents/Triumph'

google_studio_uploading = GoogleStudioUploading()
google_studio_uploading.create_creatives_from_folder(google.driver, creatives_folder)

