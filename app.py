import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import urllib3
from urllib.request import urlretrieve
from openpyxl import Workbook
import pandas as pd
import urllib3
from env import URL, DriverLocation
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')

# Rotate User Agent would be helpful

def get_data(driver):
    """
    this function get main text, score, name
    """
    print('get data...')
    # Click on more botton on each text reviews
    more_elemets = driver.find_elements(By.CSS_SELECTOR, '.w8nwRe.kyuRq')
    for list_more_element in more_elemets:
        list_more_element.click()
    # Find Pictures that have the expansion indicator to see the rest of the pictures under them and click it to expose them all
    more_pics = driver.find_elements(By.CLASS_NAME, 'Tya61d') 
    for list_more_pics in more_pics:
        if 'showMorePhotos' in  list_more_pics.get_attribute("jsaction") :
            print('Found extra pics')
            list_more_pics.click()
    elements = driver.find_elements(By.CLASS_NAME, 'jftiEf')
    lst_data = []
    for data in elements:
        name = data.find_element(By.CSS_SELECTOR, 'div.d4r55.YJxk2d').text 
        print ('Name of location: ',name)
        try: text = data.find_element(By.CSS_SELECTOR, 'div.MyEned').text 
        except: text = '' 
        score = data.find_element(By.CSS_SELECTOR, 'span.kvMYJc').get_attribute("aria-label")  #find_element(By.CSS_SELECTOR,'aria-label').text #)  ##QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf > div.m6QErb > div:nth-child(3) > div:nth-child(2) > div > div:nth-child(4) > div.DU9Pgb > span.kvMYJc
        more_specific_pics = data.find_elements(By.CLASS_NAME, 'Tya61d') 
        pics= [] 
        pics2 = []
        # check to see if folder for pictures and videos already exists, if not, create it
        cleanname = re.sub( r'[^a-zA-Z0-9]','', name)
        if not os.path.exists('./Output/Pics/'+cleanname):
            os.makedirs('./Output/Pics/'+cleanname)
        # Walk through all the pictures and videos for a given review
        for lmpics in more_specific_pics:  
            # Grab URL from style definiton (long multivalue string), and remove the -p-k so that it is full size 
            urlmedia = re.sub('=\S*-p-k-no', '=-no', (re.findall(r"['\"](.*?)['\"]", lmpics.get_attribute("style")))[0])
            print ('URL : ',urlmedia)
            pics.append(urlmedia)
#            time.sleep(2)
#            photoindex = str(lmpics.get_attribute("data-photo-index"))
            # Grab the name of the file and remove all spaces and special charecters to name the folder
            filename = re.sub( r'[^a-zA-Z0-9]','', str(lmpics.get_attribute("aria-label")))
#            filename = re.sub( r'[^a-zA-Z0-9]','', filename) 
            # Check to see if it has a sub div, which represents the label with the video length displayed, this will be done 
            # because videos are represented by pictures in the main dialogue, so we need to click through and grab the video URL
            if (lmpics.find_elements(By.CSS_SELECTOR,'div.fontLabelMedium.e5A3N')) :
                ext='.mp4'
                lmpics.click()
                time.sleep(2)
                # After we click the right side is rendered in an inframe, Store iframe web element
                iframe = driver.find_element(By.TAG_NAME, "iframe")
                # switch to selected iframe
                driver.switch_to.frame(iframe)
                # Now find button and click on button
                video_elements = driver.find_elements(By.XPATH ,'//video') #.get_attribute('src')
                urlmedia = str((video_elements[0]).get_attribute("src"))
                # return back away from iframe
                driver.switch_to.default_content()
            else:
                # The default path if it is not a video link
                ext='.jpg' 
            # Add the correct extension to the file name
            filename = filename+ext
            # Test to see if file already exists, and if it does not grab the media and store it in location folder
            if not os.path.isfile('./Output/Pics/'+cleanname+'/'+filename):
                urlretrieve(urlmedia, './Output/Pics/'+cleanname+'/'+filename)
            # Store the local path to be used in the excel document
            picsLocalpath = "./Output/Pics/"+cleanname+"/"+filename
            pics2.append(picsLocalpath)
        lst_data.append([name , text, score,pics,pics2,"GoogleMaps",today])
    return lst_data

# Grab a count of how far we need to scroll
def counter():
    result = driver.find_element(By.CLASS_NAME,'Qha3nb').text
    result = result.replace(',', '')
    result = result.split(' ')
    result = result[0].split('\n')
    return int(int(result[0])/10)+1

# Do the scrolling
def scrolling(counter):
    print('scrolling...')
    time.sleep(3)
    scrollable_div = driver.find_element(By.XPATH,
        '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[5]/div[2]')
#        '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[10]/div')
    for _i in range(counter):
        try:
            scrolling = driver.execute_script(
                'document.getElementsByClassName("dS8AEf")[0].scrollTop = document.getElementsByClassName("dS8AEf")[0].scrollHeight',
                scrollable_div
            )
            time.sleep(3)

        except Exception as e:
            print(f"Error while scrolling: {e}")
            break

def write_to_xlsx(data):
    print('write to excel...')
    cols = ["name", "comment", 'rating','picsURL','picsLocalpath','source','date']
    df = pd.DataFrame(data, columns=cols)
    df.to_excel('./Output/reviews.xlsx')


if __name__ == "__main__":
    print('starting...')
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-error")
    options.add_argument("--ignore-ssl-errors")
#    options.add_argument("--headless")  # show browser or not ||| HEAD =>  43.03 ||| No Head => 39 seg
    options.add_argument("--lang=en-US")
    # caps = webdriver.DesiredCapabilities.CHROME.copy()
    # caps['acceptInsecureCerts'] = True
    # caps['acceptSslCerts'] = True
    # driver = webdriver.Chrome(desired_capabilities=caps)
# options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    # DriverPath = Service(DriverLocation)
    # Adding argument to disable the AutomationControlled flag 
    options.add_argument("--disable-blink-features=AutomationControlled") 
    # Exclude the collection of enable-automation switches 
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    # Turn-off userAutomationExtension 
    options.add_experimental_option("useAutomationExtension", False) 
    # Setting the driver path and requesting a page 
    driver = webdriver.Chrome(options=options) # Firefox(options=options)  
    # Changing the property of the navigator value for webdriver to undefined 
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
    driver.get(URL)
    time.sleep(5)

#    counter = counter()
#    scrolling(counter)

    data = get_data(driver)
    driver.close()

    write_to_xlsx(data)
    print('Done!')