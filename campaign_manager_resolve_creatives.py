from selenium import webdriver

from google import Google
from campaign_manager import CampaignManager

# Create driver instance
driver = webdriver.Chrome()

# Log in to google first 
google = Google(driver)
google.login('me19@mediasales.hu', 'aMUNATION1')

creatives_url = 'https://campaignmanager.google.com/trafficking/#/accounts/810794/advertisers/9142492/creatives?status=1&archived=false&cm=eyJwcm9maWxlSWQiOjU1OTM5MzEsImxpc3RVcmwiOiIvYWNjb3VudHMvODEwNzk0L2FkdmVydGlzZXJzP3N0YXR1cz0xIiwiY3JpdGVyaWEiOnsicSI6IiIsInNvcnQiOiJuYW1lIiwiZGVzYyI6ZmFsc2UsImFkdmVydGlzZXJHcm91cElkcyI6MCwic3ViYWNjb3VudElkIjowLCJzdGF0dXMiOiIxIiwiYXR0ciI6ImlkO25hbWU7YWR2ZXJ0aXNlckdyb3VwLm5hbWU7c3ViYWNjb3VudC5uYW1lO3N1YmFjY291bnQuaWQ7c3RhdHVzO2Zsb29kbGlnaHRDb25maWd1cmF0aW9uSWQ7c3VzcGVuZGVkIiwidHoiOiJBbWVyaWNhL05ld19Zb3JrIiwidGFrZSI6MTAwLCJza2lwIjowfX0.&co=59&cp=9300647&cn=8394072'

# Resolve creatives
campaign_manager = CampaignManager(driver)
campaign_manager.open_unresolved_creatives(creatives_url)
campaign_manager.each_in_unresolved_creatives()