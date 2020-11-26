from selenium import webdriver

from google import Google
from campaign_manager import CampaignManager

# Create driver instance
driver = webdriver.Chrome()

# Log in to google first 
google = Google(driver)
google.login('me19@mediasales.hu', 'aMUNATION1')

creatives_url = 'https://campaignmanager.google.com/trafficking/#/accounts/810794/advertisers/9142492/creatives?q=1Image&status=1&archived=false'
dynamic_targeting_keys = ['Message_8', 'Message_11']

# Resolve creatives
campaign_manager = CampaignManager(driver)
campaign_manager.dynamic_targeting_key_factory(creatives_url, dynamic_targeting_keys)