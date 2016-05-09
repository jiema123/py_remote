
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

'''
http://stackoverflow.com/questions/25214473/disable-images-in-selenium-python

from selenium import webdriver
firefox_profile = webdriver.FirefoxProfile()

firefox_profile.add_extension(folder_xpi_file_saved_in + "\\quickjava-2.0.6-fx.xpi")
firefox_profile.set_preference("thatoneguydotnet.QuickJava.curVersion", "2.0.6.1") ## Prevents loading the 'thank you for installing screen'
firefox_profile.set_preference("thatoneguydotnet.QuickJava.startupStatus.Images", 2)  ## Turns images off
firefox_profile.set_preference("thatoneguydotnet.QuickJava.startupStatus.AnimatedImage", 2)  ## Turns animated images off

driver = webdriver.Firefox(firefox_profile)
driver.get(web_address_desired)
'''


# driver = webdriver.Chrome('/Users/lijian/Downloads/chromedriver')
chromeOptions = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome('/Users/lijian/Downloads/chromedriver', chrome_options=chromeOptions)

driver.get('http://www.ecloud-zj.com:88/enterprises/Login')
# driver.get('http://www.ecloud-zj.com:88/web/')
driver.find_element(By.CSS_SELECTOR, 'a[href=/enterprises/Login]').click()

#91330203MA28111B2 4124bc0a
driver.find_element(By.CSS_SELECTOR, '#UserName').send_keys('91330203MA28111B2')
driver.find_element(By.CSS_SELECTOR, '#Password').send_keys('4124bc0a')
driver.find_element(By.CSS_SELECTOR, 'input[type=submit]').click()


