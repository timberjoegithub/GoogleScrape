import time
import os
from pathlib import Path
#from selenium.webdriver.chrome.webdriver import WebDriver
#from selenium.webdriver.chrome.service import Service

import re
from urllib.request import urlretrieve
import urllib3

#from openpyxl import Workbook, load_workbook
from openpyxl import load_workbook
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import ast
import base64
import requests
import datetime as dt
#import json
import jsonpickle

#Instgram
#from instapy import InstaPy
#import instapy
#from instabot import Bot
import pathlib
import instagrapi
#from instagrapi.types import StoryMention, StoryMedia, StoryLink, StoryHashtag
#from instagrapi.story import StoryBuilder
from moviepy.editor import VideoFileClip, concatenate_videoclips
#import moviepy
from selenium import webdriver
#from selenium.webdriver.chrome.webdriver import WebDriver
#from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
#twitter
import tweepy
from selenium.common.exceptions import NoSuchElementException

#import asyncio
#import aiohttp


import sqlalchemy
#from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import null
#from selenium import webdriver
#from selenium.webdriver.common.by import By
import googlemaps
#import mysqlclient
#import mysql-connector-python
import env
Base = declarative_base()

##################################################################################################

class Users(Base):
    """Class representing a user config"""
    __tablename__ = 'userConfig'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user = sqlalchemy.Column(sqlalchemy.String(length=11, collation="utf8"))
    instagram = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    web = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    facebook = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    tiktok = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    xtwitter = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    threads = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    yelp = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    google = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    data = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    postsperrun = sqlalchemy.Column(sqlalchemy.String(length=11, collation="utf8"))
    needreversed = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    wpAPI = sqlalchemy.Column(sqlalchemy.String(length=256, collation="utf8"))
    platform = sqlalchemy.Column(sqlalchemy.String(length=128, collation="utf8"))
    LinuxDriverLocation = sqlalchemy.Column(sqlalchemy.String(length=256, collation="utf8"))
    WindowsDriverLocation = sqlalchemy.Column(sqlalchemy.String(length=256, collation="utf8"))
    xls = sqlalchemy.Column(sqlalchemy.String(length=128, collation="utf8"))
    googleurl = sqlalchemy.Column(sqlalchemy.String(length=128, collation="utf8"))
    instagramuser = sqlalchemy.Column(sqlalchemy.String(length=32, collation="utf8"))
    instagrampass = sqlalchemy.Column(sqlalchemy.String(length=32, collation="utf8"))
    #active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

##################################################################################################

class Posts(Base):
    """Class representing the attributes of a post"""
    __tablename__ = 'posts'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=256, collation="utf8"))
    comment = sqlalchemy.Column(sqlalchemy.String(length=4096, collation="utf8"))
    rating = sqlalchemy.Column(sqlalchemy.String(length=128, collation="utf8"))
    picsURL = sqlalchemy.Column(sqlalchemy.String(length=4096, collation="utf8"))
    picsLocalpath = sqlalchemy.Column(sqlalchemy.String(length=4096, collation="utf8"))
    source = sqlalchemy.Column(sqlalchemy.String(length=64, collation="utf8"))
    date = sqlalchemy.Column(sqlalchemy.String(length=64, collation="utf8"))
    address = sqlalchemy.Column(sqlalchemy.String(length=256, collation="utf8"))
    dictPostComplete = sqlalchemy.Column(sqlalchemy.String(length=128, collation="utf8"))
    #googleurl = sqlalchemy.Column(sqlalchemy.String(length=128, collation="utf8"))
    wpurl = sqlalchemy.Column(sqlalchemy.String(length=512, collation="utf8"))
    businessurl = sqlalchemy.Column(sqlalchemy.String(length=2048, collation="utf8"))
    longitude = sqlalchemy.Column(sqlalchemy.Float())
    latitude = sqlalchemy.Column(sqlalchemy.Float())
    google = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    facebook = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    instagram = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    xtwitter = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    threads = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    yelp = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    web = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    tiktok = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    #active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    place_id = sqlalchemy.Column(sqlalchemy.String(length=126, collation="utf8"))
    googledetails = sqlalchemy.Column(sqlalchemy.String(length=4096, collation="utf8"))
    #businessurl = sqlalchemy.Column(sqlalchemy.String(length=512, collation="utf8"))
    pluscode = sqlalchemy.Column(sqlalchemy.String(length=64, collation="utf8"))
    googleurl = sqlalchemy.Column(sqlalchemy.String(length=512, collation="utf8"))


##################################################################################################

def preload():
    """
    Removes a specific file if it exists.

    Returns:
        None
    """

    file=pathlib.Path("./config/joeteststeele_uuid_and_cookie.json")
    if pathlib.Path.exists(file):
        pathlib.Path.unlink(file)
#    today = datetime.today().strftime('%Y-%m-%d')
    return

##################################################################################################

def clearlist(my_list):
    """
    Clears all elements in a list.

    Args:
        my_list (list): The list to be cleared.

    Returns:
        list: The input list with all elements cleared.
    """

    for listelement in my_list:
        listelement.clear
    return my_list

##################################################################################################

def get_auth_connect():
    """Make all connections to socials and DB, etec.."""
    connections = {}
    if env.mariadb:
        print('Connecting to MariaDB for configuration and storage')
        #from sqlalchemy import create_engine
        engine = sqlalchemy.create_engine("mysql+mysqldb://"+env.mariadbuser+":"+env.mariadbpass+
            "@"+env.mariadbserver+"/"+env.mariadbdb+"?charset=utf8mb4", echo=False)
        session = sqlalchemy.orm.sessionmaker()
        session.configure(bind=engine)
#        session = Session()
        usersession = session.query(Users).filter(Users.user=='joesteele')
        dbuser = usersession[0]
        #for userloop in usersession:
        print("- " + dbuser.user + ' ' + dbuser.googleurl)
        connections['user'] =dbuser
        posts = session.query(Posts).all()
        connections['posts'] = posts
        connections['postssession'] = session
    if env.data:
        print('  loading XLS content data source ...')
        if os.path.exists(env.xls):
            wb = load_workbook(filename = env.xls)
            xlswbDF = pd.read_excel(env.xls)
        else:
            if os.path.exists('./GoogleScrape/'+ env.xls):
                wb = load_workbook(filename = './GoogleScrape/'+ env.xls)
                xlswbDF = pd.read_excel('./GoogleScrape/'+ env.xls)
            else:
                input("Not able to find xls file Press any key to continue...")
        ws = wb['Sheet1']
        #xlswbDF = pd.read_excel(xls)
        connections.update({'xlsdf':xlswbDF,'data':ws,'datawb':wb})
#        connections.update({'data':ws})
#        connections.update({'datawb':wb})
    if env.instagram :
        print('  Connecting to Instagram ...')
        instasessionclient = instagrapi.Client()
        instasessionclient.login(env.instagramuser, env.instagrampass)
        connections.update({'instagram':instasessionclient})
    if env.facebook :
        print('  Connecting to facebook ...')
        # page_id_1 = facebookpageID
        # facebook_access_token = 'paste-your-page-access-token-here'
        # image_url = 'https://graph.facebook.com/{}/photos'.formatting(page_id_1)
        # image_location = 'http://image.careers-portal.co.za/f_output.jpg'
        # img_payload = {
        # 'message': msg,
        # 'url': image_location,
        # 'access_token': facebook_access_token
        # }
        # #Send the POST request
        # r = requests.post(image_url, data=img_payload)
        # print(r.text)
        connections.update({'facebook':posts})
    if env.yelp :
        print('  Connecting to yelp ...')
    if env.xtwitter :
        print('  Connecting to xtwitter ...')
    if env.threads :
        print('  Connecting to threads ...')
        threadssessionclient = instagrapi.Client()
        threadssessionclient.login(env.instagramuser, env.instagrampass)
        connections.update({'threads':threadssessionclient})
    if env.web :
        print('  Connecting to joeeatswhat.com ...')
        data_string = f"{env.user}:{env.password}"
        token = base64.b64encode(data_string.encode()).decode("utf-8")
        headers = {"Authorization": f"Basic {token}"}
        connections.update({'web' : headers})
    if env.tiktok :
        print('  Connecting to Instagram ...')
    return connections

##################################################################################################

def get_twitter_conn_v1(api_key, api_secret, access_token, access_token_secret) -> tweepy.API:
    """Get twitter conn 1.1"""
    auth = tweepy.OAuth1UserHandler(api_key, api_secret)
    auth.set_access_token(
        access_token,
        access_token_secret,
    )
    return tweepy.API(auth)

##################################################################################################

def get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret) -> tweepy.Client:
    """Get twitter conn 2.0"""
    return tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

##################################################################################################

def get_hastags(address, name, hashtype):
    """
    Generates hashtags based on the address, name, and type provided.

    Args:
        address (str): The address related to the content.
        name (str): The name associated with the content.
        hashtype (str): The type of hashtags to generate.

    Returns:
        str: The generated hashtags based on the input parameters.
    """

    nameNoSpaces = re.sub( r'[^a-zA-Z]','',name)
    addressdict = address.rsplit(r' ',3)
    zip_code = addressdict[3]
    state = addressdict[2]
    city =  re.sub( r'[^a-zA-Z]','',addressdict[1])
    if 'short' in hashtype:
        defaulttags = '#'+nameNoSpaces+' #foodie #food #joeeatswhat @timberjoe'
    else:
        defaulttags = "\n\n\n#"+nameNoSpaces+" #foodie #music #food #travel #drinks #instagood #feedme #joeeatswhat @timberjoe"
    citytag = "#"+city
    statetag = "#"+state
    ziptag = "#"+zip_code
    if statetag == 'FL':
        statetag += ' #Florida'
    return defaulttags+" "+citytag+" "+statetag+" "+ziptag+" "

##################################################################################################

# Grab a count of how far we need to scroll
def counter_google(driver):
    """
    Counts the number of Google search results pages.

    Args:
        driver: The Selenium WebDriver instance.

    Returns:
        int: The total number of search result pages.
    """

    result = driver.find_element(By.CLASS_NAME,'Qha3nb').text
    result = result.replace(',', '')
    result = result.split(' ')
    result = result[0].split('\n')
    return int(result[0]) // 10 + 1

##################################################################################################

def make_montage_video_from_google(inphotos):
    """
    Creates a montage video from a list of input photos.

    Args:
        inphotos (list): List of paths to input photo files.

    Returns:
        tuple: A tuple containing the path to the output video file and a boolean indicating success.
    """

# Load the photos from the folder
# Set the duration of each photo to 2 seconds
    if not inphotos:
        return False, False
    directory = inphotos[0].rsplit(r'/', 1)
    folder = directory[0]
    output = folder+"/montage.mp4"
    if not os.path.exists(output) and len(inphotos) >1:
        video = VideoFileClip(inphotos[0])
        for photo in inphotos :
            #clip = VideoFileClip("myHolidays.mp4").subclip(50,60)
            clip = VideoFileClip(photo)
            # Concatenate the photos into a clip
            if ".jpg" in photo:
                clip.duration = 2
            try:
                video = concatenate_videoclips([video, clip], method="compose")
            except AttributeError as error:
                print("  An error occurred :", type(error).__name__) # An error occurred:
        # Load the audio file
        #    audio = AudioFileClip("audio.mp3")
        # Set the audio as the soundtrack of the montage
        #    montage = montage.set_audio(audio)
        # Write the final montage to a file
        outputvideo = video.write_videofile(folder+"/montage.mp4", fps=24)
    else:
        outputvideo = False
    return outputvideo, output

##################################################################################################

def is_docker():
    """
    Checks if the code is running in a Docker container.

    Returns:
        bool: True if running in a Docker container, False otherwise.
    """
    cgroup = Path('/proc/self/cgroup')
    #print (cgroup.read_text())
    return Path('/.dockerenv').is_file() or cgroup.is_file() and 'docker' in cgroup.read_text()

##################################################################################################

def post_facebook_video(group_id, video_path, auth_token, title, content, date, rating, address):
    """
    Posts a video to a Facebook group with specified details.

    Args:
        group_id (str): The ID of the Facebook group.
        video_path (list): List of paths to the video files to be uploaded.
        auth_token (str): The authentication token for posting to Facebook.
        title (str): The title of the video.
        content (str): Additional content to be included in the post.
        date (str): The date of the post.
        rating (str): The rating associated with the post.
        address (str): The address related to the post.

    Returns:
        dict or bool: The response JSON if successful, False if an error occurs.
    """

    url = f"https://graph-video.facebook.com/{group_id}/videos?access_token=" + auth_token
    addresshtml = re.sub(" ", ".",address)
    files = {eachfile: open(eachfile, 'rb') for eachfile in video_path}
    data = { "title":title,"description" : title + "\n"+ address+"\nGoogle map to destination: "
            r"https://www.google.com/maps/dir/?api=1&destination="+addresshtml +"\n\n"+ content +
            "\n"+rating+"\n"+date+"\n\n"+ get_hastags(address, title, 'long')+
            "\n\nhttps://www.joeeatswhat.com"+"\n\n","published" : True,
            "alt_text" : title
    }
    try:
        r = requests.post(url, files=files, data=data,timeout=40).json()
    except AttributeError as error:
        print("    An error getting date occurred:", error) # An error occurred:
        r = False
    time.sleep(env.facebooksleep)
    return r

##################################################################################################

def get_google_data(driver,outputs ):
# curl -X GET -H 'Content-Type: application/json' -H "X-Goog-Api-Key: API_KEY" -H
#   "X-Goog-FieldMask: id,displayName,formattingtedAddress,plusCode"
#   https://places.googleapis.com/v1/places/ChIJj61dQgK6j4AR4GeTYWZsKWw #placeId #websiteUri
    """
    this function gets main text, score, name
    """
    print('get data...')
    # Click on more botton on each text reviews
    more_elemets = driver.find_elements(By.CSS_SELECTOR, '.w8nwRe.kyuRq')
    for list_more_element in more_elemets:
        list_more_element.click()
    # Find Pictures that have the expansion indicator to see the rest of the pictures under
    #    them and click it to expose them all
    more_pics = driver.find_elements(By.CLASS_NAME, 'Tya61d')
    for list_more_pics in more_pics:
        if 'showMorePhotos' in  list_more_pics.get_attribute("jsaction") :
            print('    Found extra pics')
            list_more_pics.click()
    elements = driver.find_elements(By.CLASS_NAME, 'jftiEf')

    lst_data = []
    for data in elements:
        name = data.find_element(By.CSS_SELECTOR, 'div.d4r55.YJxk2d').text
        try:
            address = data.find_element(By.CSS_SELECTOR, 'div.RfnDt.xJVozb').text
        except NoSuchElementException :
            address = 'Unknonwn'
        print ('Name of location: ',name, '   Address:',address)
        try:
            visitdate = data.find_element(By.CSS_SELECTOR, 'span.rsqaWe').text
        except NoSuchElementException :
            visitdate = "Unknown"
        print('  Visited: ',visitdate)
        try:
            text = data.find_element(By.CSS_SELECTOR, 'div.MyEned').text
        except NoSuchElementException :
            text = ''
        try:
            score = data.find_element(By.CSS_SELECTOR, 'span.kvMYJc').get_attribute("aria-label")
        #find_element(By.CSS_SELECTOR,'aria-label').text #)  ##QA0Szd > div > div > div.w6VYqd >
        #  div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf
        #  > div.m6QErb > div:nth-child(3) > div:nth-child(2) > div > div:nth-child(4) > div.DU9Pgb
        #  > span.kvMYJc
        except NoSuchElementException  as error:
            score = "Unknown"
            print ('Error: ',error)
        more_specific_pics = data.find_elements(By.CLASS_NAME, 'Tya61d')
    #  Grab more info from google maps entry on this particular review
        if outputs['postssession'].query(Posts).filter(Posts.name == name,Posts.google is not True) or env.forcegoogleupdate:
            gmaps = googlemaps.Client(env.googleapipass)
            place_ids = gmaps.find_place(name+address, input_type = 'textquery', fields='')
            if len(place_ids['candidates']) == 1 :
                place_id = place_ids['candidates'][0]['place_id']
                details = gmaps.place(place_id)
            # Get place details
                try:
                    businessurl = details['result']['website']
                    latitude = details['result']['geometry']['location']['lat']
                    longitude = details['result']['geometry']['location']['lng']
                    pluscode = details['result']['plus_code']['compound_code']
                    googleurl = details['result']['url']
                    database_update_row(name,"businessurl",businessurl,"onlyempty",outputs)
                    database_update_row(name,"latitude",latitude,"onlyempty",outputs)
                    database_update_row(name,"longitude",longitude,"onlyempty",outputs)
                    database_update_row(name,"pluscode",pluscode,"onlyempty",outputs)
                    database_update_row(name,"googleurl",googleurl,"onlyempty",outputs)
                    database_update_row(name,"place_id",place_id,"onlyempty",outputs)
                    database_update_row(name,"googledetails",details,"onlyempty",outputs)
                    database_update_row(name,"google",True,"onlyempty",outputs)
                except KeyError as error:
                    print('Error writing business details from google maps : ',error)
        else:
            print ('  Post was already in database, skipping update unless you activate override')
        pics= []
        pics2 = []
        # check to see if folder for pictures and videos already exists, if not, create it
        cleanname = re.sub( r'[^a-zA-Z0-9]','', name)
        if not os.path.exists('./Output/Pics/'+cleanname):
            os.makedirs('./Output/Pics/'+cleanname)
        # Walk through all the pictures and videos for a given review
        for lmpics in more_specific_pics:
            # Grab URL from style definiton (long multivalue string), and remove the -p-k so that
            #   it is full size
            urlmedia = re.sub(r'=\S*-p-k-no', '=-no', (re.findall(r"['\"](.*?)['\"]",
                lmpics.get_attribute("style")))[0])
            print ('    Pic URL : ',urlmedia)
            pics.append(urlmedia)
            # Grab the name of the file and remove all spaces and special charecters to name the
            #    folder
            filename = re.sub( r'[^a-zA-Z0-9]','', str(lmpics.get_attribute("aria-label")))
            if lmpics == more_specific_pics[0]:
                lmpics.click()
                time.sleep(2)
                #iframe = driver.find_element(By.TAG_NAME, "iframe")
                tempdate = str((driver.find_element(By.CLASS_NAME,'mqX5ad')).text).rsplit("-",1)
                visitdate = re.sub( r'[^a-zA-Z0-9]','',tempdate[1])
                #print ('  Visited: ',visitdate)
            # Check to see if it has a sub div, which represents the label with the video length
            # displayed, this will be done
            # because videos are represented by pictures in the main dialogue, so we need to click
            # through and grab the video URL
            if lmpics.find_elements(By.CSS_SELECTOR,'div.fontLabelMedium.e5A3N') :
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
            # Test to see if file already exists, and if it does not grab the media and store it
            #   in location folder
            if not os.path.exists('./Output/Pics/'+cleanname+'/'+visitdate):
                os.makedirs('./Output/Pics/'+cleanname+'/'+visitdate)
            if not os.path.isfile('./Output/Pics/'+cleanname+'/'+visitdate+'/'+filename):
                urlretrieve(urlmedia, './Output/Pics/'+cleanname+'/'+visitdate+'/'+filename)
            # Store the local path to be used in the excel document
            picsLocalpath = "./Output/Pics/"+cleanname+"/"+visitdate+'/'+filename
            pics2.append(picsLocalpath)
        if pics2:
            make_montage_video_from_google(pics2)
            pics2.append("./Output/Pics/"+cleanname+"/"+visitdate+'/'+'montage.mp4')
        dictPostComplete= {'google':1,'web':0,'yelp':0,'facebook':0,'xtwitter':0,
            'instagram':0,'tiktok':0}
        lst_data.append([name , text, score,pics,pics2,"GoogleMaps",visitdate,address,
            dictPostComplete])
    return lst_data

##################################################################################################

# Do the google_scroll
def google_scroll(counter_google_scroll,driver):
    """
    Scrolls down a Google search results page a specified number of times.

    Args:
        counter_google_scroll (int): The number of times to scroll down the page.
        driver: The Selenium WebDriver instance.

    Returns:
        int: The result of the last scroll operation.

    Raises:
        AttributeError: If an error occurs during scrolling.
    """
    print('google_scroll...')
    time.sleep(3)
    scrollable_div = driver.find_element(By.XPATH,
        '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[5]/div[2]')
#        '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[10]/div')
    for _i in range(counter_google_scroll):
        try:
            google_scroll = driver.execute_script(
                'document.getElementsByClassName("dS8AEf")[0].\
                    scrollTop=document.getElementsByClassName("dS8AEf")[0].scrollHeight',
                    scrollable_div
            )
            time.sleep(3)
        except AttributeError  as e:
            print(f"Error while google_scroll: {e}")
            break
    return google_scroll

##################################################################################################

def write_to_xlsx2(data, outputs):
    print('write to excel...')
    sqlalchemy.null()
    cols = ["name", "comment", 'rating','picsURL','picsLocalpath','source','date','address',
        'dictPostComplete']
    cols2 = ["num","name", "comment", 'rating','picsURL','picsLocalpath','source','date',
        'address','dictPostComplete']
    df = pd.DataFrame(data, columns=cols)
    df2 = pd.DataFrame(outputs['xlsdf'].values, columns=cols2)
    #df2 = df1.where((pd.notnull(df)), None)  # take out NAN problems
    #df3.astype(object).where(pd.notnull(df2), None)
    print ('Dropped items not included in sync to database: ',df2.dropna(inplace=True))
    rows = list(data)
    if env.needreversed:
        rows = reversed(rows)
    #jsonposts = json.dumps(outputs['posts'], default=Posts)
    print("Encode Object into JSON formatted Data using jsonpickle")
    jsonposts = jsonpickle.encode(outputs['posts'], unpicklable=False)
    for processrow in df2.values:
        if (processrow[1] in df.values):
            print ('  Row ',processrow[0],' ', processrow[1],'  already in XLS sheet')
            d2_row = Posts(name=processrow[1],comment=processrow[2],rating=processrow[3],
                picsURL=processrow[4],picsLocalpath=processrow[5],source=processrow[6],
                date=processrow[7],address=processrow[8],dictPostComplete=processrow[9])
        elif processrow[1] is not None:
            # Create a Python dictionary object with all the column values
            # d_row = {'name':processrow[1],'comment':processrow[2],'rating':processrow[3],
            #     'picsURL':processrow[4],'picsLocalpath':processrow[5], 'source':processrow[6],
            #     'date':processrow[7],'address':processrow[8],'dictPostComplete':processrow[9]}
            d2_row = Posts(name=processrow[1],comment=processrow[2],rating=processrow[3],
                picsURL=processrow[4],picsLocalpath=processrow[5],source=processrow[6],
                date=processrow[7],address=processrow[8],dictPostComplete=processrow[9])
            print ('  Row ',processrow[0],' ', processrow[1],'  added to XLS sheet')
        # Append the above Python dictionary object as a row to the existing pandas DataFrame
        # Using the DataFrame.append() function
        try:
            if processrow[1] in jsonposts : #outputs['posts']):
                print ('  Row ',processrow[0],' ', processrow[1],'  already in Database')
            else:
                outputs['postssession'].add(d2_row)
                outputs['postssession'].commit()
                print ('  Row ',processrow[0],' ', processrow[1],'  added to Database')
        except AttributeError as error:
            print('    Not able to write to post data table: ' , type(error))
            outputs['postssession'].rollback()
            raise
    df.to_excel(env.xls)
    return data

##################################################################################################

def write_to_database(data, outputs):
    print('write to database ...')
    sqlalchemy.null()
    cols = ["name", "comment", 'rating','picsURL','picsLocalpath','source','date','address',
        'dictPostComplete']
    # cols2 = ["num","name", "comment", 'rating','picsURL','picsLocalpath','source','date',
    #     'address','dictPostComplete']
    df = pd.DataFrame(data, columns=cols)
    # df2 = pd.DataFrame(outputs['xlsdf'].values, columns=cols2)
    # print ('Dropped items not included in sync to database: ',df2.dropna(inplace=True))
    rows = list(data)
    if env.needreversed:
        rows = reversed(rows)
    #jsonposts = json.dumps(outputs['posts'], default=Posts)
    print("Encode Object into JSON formatted Data using jsonpickle")
    jsonposts = jsonpickle.encode(outputs['posts'], unpicklable=False)
    for processrow in outputs['postssession']:
        if (processrow[1] in df.values):
            print ('  Row ',processrow[0],' ', processrow[1],'  already in database')
            d2_row = Posts(name=processrow[1],comment=processrow[2],rating=processrow[3],
                picsURL=processrow[4],picsLocalpath=processrow[5],source=processrow[6],
                date=processrow[7],address=processrow[8],dictPostComplete=processrow[9])
        elif processrow[1] is not None:
            # Create a Python dictionary object with all the column values
            # d_row = {'name':processrow[1],'comment':processrow[2],'rating':processrow[3],
            #     'picsURL':processrow[4],'picsLocalpath':processrow[5], 'source':processrow[6],
            #     'date':processrow[7],'address':processrow[8],'dictPostComplete':processrow[9]}
            d2_row = Posts(name=processrow[1],comment=processrow[2],rating=processrow[3],
                picsURL=processrow[4],picsLocalpath=processrow[5],source=processrow[6],
                date=processrow[7],address=processrow[8],dictPostComplete=processrow[9])
            print ('  Row ',processrow[0],' ', processrow[1],'  added to XLS sheet')
        # Append the above Python dictionary object as a row to the existing pandas DataFrame
        # Using the DataFrame.append() function
        try:
            if processrow[1] in jsonposts : #outputs['posts']):
                print ('  Row ',processrow[0],' ', processrow[1],'  already in Database')
            else:
                outputs['postssession'].add(d2_row)
                outputs['postssession'].commit()
                print ('  Row ',processrow[0],' ', processrow[1],'  added to Database')
        except AttributeError as error:
            print('    Not able to write to post data table: ' , type(error))
            outputs['postssession'].rollback()
            raise
    df.to_excel(env.xls)
    return data

##################################################################################################

def database_update_row(review_name,column_name,column_value,update_style,outputs):
    try:
        if update_style == "forceall" and column_value != False:
            outputs['postssession'].query(Posts).filter(Posts.name == review_name).update\
                        ({column_name : column_value})
            print ('    Force Updated ',column_name, ' to: ',column_value)
        elif update_style == "onlyempty"  and column_value != False:
            postval = outputs['postssession'].query(Posts).filter(Posts.name == review_name,\
                            getattr(Posts,column_name).is_not(null())).all()
            if len(postval) == 0 :
                outputs['postssession'].query(Posts).filter(Posts.name == review_name).update\
                    ({column_name : column_value})
                print ('    Updated blank ',postval ,' on value',column_name, ' to: ',column_value)
        elif update_style == "toggletrue":
            postval = outputs['postssession'].query(Posts).filter(Posts.name == review_name,\
                            getattr(Posts,column_name).is_not(1)).all()
            outputs['postssession'].query(Posts).filter(Posts.name == review_name).update\
                    ({column_name : "1"})
            print ('    Updated ',column_name, ' on value: ',postval[0].column_value, ' to: ',\
                column_value)
    except AttributeError as error:
        print("    Not able to write to post data table to update ",review_name," ",column_name,"\
            to: ",column_value , type(error), error)
        outputs['postssession'].rollback()
        raise
    else:
        outputs['postssession'].commit()
    return True

##################################################################################################

def check_wordpress_media(filename,headers):
    file_name_minus_extension = filename
    response = requests.get(env.wpAPI + "/media?search="+file_name_minus_extension,\
                        headers=headers,timeout=40)
    try:
        result = response.json()
        file_id = int(result[0]['id'])
        link = result[0]['guid']['rendered']
        return file_id, link
    except AttributeError:
        print('    No existing media with same name in Wordpress media folder: '+filename)
        return (False, False)

##################################################################################################

def check_is_port_open(host, port):
    """_summary_

    Args:
        host (_type_): _description_
        port (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        is_web_up = urllib3.request("GET", host)
        if is_web_up.status == 200:
            return True
    except AttributeError as error:
        print ('Could not open port to website: ', host,  type(error))
        return False

##################################################################################################

def get_wordpress_post_id_and_link(postname,headers2):
    """_summary_

    Args:
        postname (_type_): _description_
        headers2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    response = requests.get(env.wpAPI+"/posts?search="+postname, headers=headers2,timeout=40)
    result = response.json()
    if len(result) > 0:
        return int(result[0]['id']), result[0]['link']
    print('No existing post with same name: ' + postname)
    return False, False

##################################################################################################

def check_wordpress_post(postname,postdate,headers2):
    """ Checks workpress website to see if a post already exists

    Args:
        postname (_type_): _description_
        postdate (_type_): _description_
        headers2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    response = requests.get(env.wpAPI+"/posts?search="+postname, headers=headers2,timeout=40)
    result = response.json()
    if len(result) > 0 and postdate == result[0]['date']:
        return int(result[0]['id']), result[0]['link']
    print('No existing post with same name: ' + postname)
    return False, False

##################################################################################################

# Function to get the featured photo ID of a WordPress post
def get_wordpress_featured_photo_id(post_id):
    """ Get photoid from featured photo

    Args:
        post_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Make a GET request to the WordPress REST API to retrieve media details
    response = requests.get(f"{env.wpAPI}?parent={post_id}",timeout=50)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        media_items = response.json()

        # Loop through the media items associated with the post
        for item in media_items:
            # Check if the media item is the featured image
            if item.get('post', None) == int(post_id):
                # Return the ID of the featured image
                return item['id']
    # If the request failed or the featured image was not found, return None
    return None
# # Example usage
# featured_photo_id = get_featured_photo_id(POST_ID)
# print(f"The featured photo ID for post {POST_ID} is: {featured_photo_id}")

##################################################################################################

def post_to_x2(title, content, date, rating, address, picslist, instasession,outputs): 
    """
    Post to x2.

    This function posts content to a social media platform using the provided data.

    Args:
        title (str): The title of the post.
        content (str): The content of the post.
        date (str): The date of the post.
        rating (int): The rating of the post.
        address (str): The address associated with the post.
        picslist (list): A list of pictures for the post.
        instasession: The Instagram session for posting.

    Returns:
        str: The media ID of the posted content.
    """
    pics = ((picslist[1:-1]).replace("'","")).split(",")
    # Replace the following strings with your own keys and secrets
    CONSUMER_KEY = env.x_consumer_key
    CONSUMER_SECRET = env.x_consumer_secret
    ACCESS_TOKEN = env.x_access_token
    ACCESS_TOKEN_SECRET = env.x_access_token_secret
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    # Create an API object to use the Twitter API
    #api = tweepy.API(auth)
    img_list = pics
    imgs_vid = []
    imgs_pic = []
    client_v1 = get_twitter_conn_v1(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    client_v2 = get_twitter_conn_v2(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    for img in img_list:
        if 'montage.mp4' in img:
            imgs_vid.append(img.strip())
        else:
            imgs_pic.append(img.strip())
    if imgs_vid:
        try:
            video_path = imgs_vid[0]
            # Message to post along with the video
            attrib_list = outputs['postssession'].query(Posts).filter(Posts.name == title).all()
            business_url = attrib_list[0].businessurl
            if business_url:
                wpurl = attrib_list[0].wpurl
                status_message = str(title) + ': My Review - '+ wpurl + '\n Business website: '+ \
                    business_url + '  s\n'
                status_message2  = status_message +' '+str(get_hastags(address, title, 'short'))+' '
                status_message_short = status_message2[:279]
                # Upload video
                media = client_v1.media_upload(filename=video_path)
                # Post tweet with video
                tweetlat = (outputs['postssession'].query(Posts).filter(Posts.name == title).all())[0].latitude
                tweetlong = (outputs['postssession'].query(Posts).filter(Posts.name == title).all())[0].longitude
                if media.processing_info['state'] != 'failed':
                    client_v2.create_tweet(text=status_message_short,media_ids=[media.media_id])
#                    client_v2.create_tweet(text=status_message_short, lat=tweetlat , long=tweetlong ,media_ids=[media.media_id])
                else:
                    print ('Problem uploading video to twitter: ',media.processing_info['error'])
                    return False
        except AttributeError  as error:
            print("AttributeError     An error occurred:",error) # An error occurred:
    time.sleep(env.facebooksleep)
    return True

##################################################################################################

def post_facebook3(title, content, date, rating, address, picslist, outputs):
    """
    Post to Facebook3.

    This function posts content to Facebook using the provided data.

    Args:
        title (str): The title of the post.
        content (str): The content of the post.
        date (str): The date of the post.
        rating (int): The rating of the post.
        address (str): The address associated with the post.
        picslist (list): A list of pictures for the post.
        instasession: The Instagram session for posting.

    Returns:
        bool: Indicates if the post was successfully made.
    """
    pics = ((picslist[1:-1]).replace("'","")).split(",")
    group_id = env.facebookpageID
    auth_token = env.facebookpass
    imgs_id = []
    imgs_vid = []
    imgs_pic = []
    img_list = pics
    attrib_list = outputs['postssession'].query(Posts).filter(Posts.name == title).all()
    business_url = attrib_list[0].businessurl
    wpurl = attrib_list[0].wpurl
    status_message = str(title) + ': My Review - '+ wpurl + '\n Business website: '+ \
        business_url+' \n\n'+ content
    for img in img_list:
        if 'montage.mp4' in img:
            imgs_vid.append(img.strip())
        else:
            imgs_pic.append(img.strip())
    if imgs_vid:
        try:
            post_id = post_facebook_video(group_id, imgs_vid,auth_token,title, status_message,
                date, rating, address)
            imgs_id.append(post_id['id'])
        except AttributeError  as error:
            print("    An error occurred:",error)
            return False
    time.sleep(env.facebooksleep)
    print('    Facebook response: ',post_id)
    return  (True)

##################################################################################################

def post_to_threads (title, content, date, rating, address, picslist, instasession):
    if picslist != '[]' and "montage.mp4" in picslist:
        outputmontage = ''
        addresshtml = re.sub(" ", ".",address)
        #content = content + get_hastags(address, title)
        pics = ((picslist[1:-1].replace(",","")).replace("'","")).split(" ")
        video, outputmontage = make_montage_video_from_google(pics)
        try:
            data =  title + "\n"+ address+"\nGoogle map to destination: " \
                r"https://www.google.com/maps/dir/?api=1&destination="+addresshtml +"\n\n" \
                + content + "\n"+rating+"\n"+date+"\n\n"+ get_hastags(address, title,'long')+ \
                "\n\nhttps://www.joeeatswhat.com "+"\n\n"
            instasession.video_upload(outputmontage, data)
#           video2 = instasession.video_upload(outputmontage, data)
        except AttributeError  as error:
            print("  An error occurred uploading video to Threads:", type(error).__name__) 
            return False
        return True
    else:
        return False

def post_to_threads2 (title, content, date, rating, address, picslist, instasession):
    if picslist != '[]' and "montage.mp4" in picslist:
        outputmontage = ''
        addresshtml = re.sub(" ", ".",address)
        pics = ((picslist[1:-1].replace(",","")).replace("'","")).split(" ")
        video, outputmontage = make_montage_video_from_google(pics)
        try:
            data =  title + "\n"+ address+"\nGoogle map to destination: " r"https://www.google.com/maps/dir/?api=1&destination="+addresshtml +"\n\n"+ content + "\n"+rating+"\n"+date+"\n\n"+ get_hastags(address, title,'long')+"\n\nhttps://www.joeeatswhat.com"+"\n\n"
            instasession.video_upload(outputmontage, data)
#           video2 = instasession.video_upload(outputmontage, data)
        except AttributeError  as error:
            print("  An error occurred uploading video to Instagram:", type(error).__name__)
            return False
        #media_pk = instasession.media_pk_from_url('https://www.instagram.com/p/CGgDsi7JQdS/')
        #media_path = instasession.video_download(media_pk)
        # joeeatswhat = instasession.user_info_by_username('timberjoe')
        # try: buildout = instagrapi.story.StoryBuilder(outputmontage,'Credits @timberjoe',[StoryMention(user=joeeatswhat)]).video(40)  # seconds
        # except AttributeError as error:
        #     print("  An error occurred uploading video to Instagram:", type(error).__name__) # An error occurred:
        # try: instasession.video_upload_to_story(buildout.path,"Credits @example",mentions=buildout.mentions,links=[StoryLink(webUri='https://www.joeeatswhat.com')],medias=[StoryMedia(media_pk=outputmontage)])
#         try:
#             instasession.video_upload_to_story(
#             outputmontage,
#             "Credits @joeeatswhat",
#  #           mentions=[StoryMention(user='timberjoe', x=0.49892962, y=0.703125, width=0.8333333333333334, height=0.125)],
#             links=[StoryLink(webUri='https://www.joeeatswhat.com')],
#   #          hashtags=[StoryHashtag(hashtag=get_hastags(address,title), x=0.23, y=0.32, width=0.5, height=0.22)],
#             #medias=[StoryMedia(media_pk=media_pk, x=0.5, y=0.5, width=0.6, height=0.8)],
#         )
#             story = instasession.story_photo("path/to/photo.jpg")
#             instasession.video_elements.add_link("https://www.joeeatswhat.com")
#             #story.add_link("https://www.joeeatswhat.com")
#             instasession.video_elements.add_hashtags(get_hastags)
#             story = instasession.video_upload_to_story(outputmontage)
#             story.upload()
#             #instasession.video_upload_to_story(path:outputmontage,caption:content, mentions:r'@timberjoe',links:'https://www.joeeatswhat.com',hashtags: hastag) ( path: outputmontage, caption: content, mentions:['@timberjoe'], links: ['https://www.joeeatswhat.com'], hashtags: get_hastags )
#             # temp = dict()
#             # temp = instasession.video_upload_to_story(path=outputmontage,caption=content,mentions=r'@timberjoe',links='https://www.joeeatswhat.com',hashtags=get_hastags)
#         except AttributeError as error:
#             print("  An error occurred uploading video to Instagram:", type(error).__name__) # An error occurred:
#             return False
        return True
    else:
        return False

#######################################################################################################

def post_to_tiktok(title, content, date, rating, address, picslist, instasession):

    # Replace 'your_sessionid_cookie' with your actual TikTok sessionid cookie.
    session_id = 'your_sessionid_cookie'

    # Replace 'path_to_video.mp4' with the path to your video file.
    file_path = 'path_to_video.mp4'

    # Replace 'Your video title' with the title of your video.
    #title = 'Your video title'

    # Replace the following list with the hashtags you want to add to your post.
    tags = ['hashtag1', 'hashtag2', 'hashtag3']

    # If you want to schedule your video, replace 'schedule_timestamp' with the Unix timestamp.
    # Leave it as None if you want to upload immediately.
    schedule_time = None  # or Unix timestamp (e.g., 1672592400)

    return

# def upload_video(session_id, file_path, title, tags, schedule_time=None):
#     url = 'https://www.tiktok.com/api/upload/video/'
#     headers = {
#         'Cookie': f'sessionid={session_id}'
#     }
#     data = {
#         'title': title,
#         'tags': ','.join(tags),
#         'schedule_time': schedule_time
#     }
#     files = {
#         'video': open(file_path, 'rb')
#     }
#     response = requests.post(url, headers=headers, data=data, files=files)
#     return response.json()

# # Call the function to upload the video
# response = upload_video(session_id, file_path, title, tags, schedule_time)
# print(response)

#######################################################################################################

def post_to_instagram2 (title, content, date, rating, address, picslist, instasession,outputs):
    #post_to_instagram2(processrow[1].value, processrow[2].value ,processrow[7].value,processrow[3].
    #   value, processrow[8].value, processrow[5].value,outputs['instagram'])
    #montageexists = "montage.mp4" in picslist
    if picslist != '[]' and "montage.mp4" in picslist:
        outputmontage = ''
        addresshtml = re.sub(" ", ".",address)
        #content = content + get_hastags(address, title)
        pics = ((picslist[1:-1].replace(",","")).replace("'","")).split(" ")
        video, outputmontage = make_montage_video_from_google(pics)
        attrib_list = outputs['postssession'].query(Posts).filter(Posts.name == title).all()
        business_url = attrib_list[0].businessurl
        if business_url:
            wpurl = attrib_list[0].wpurl
            try:
                data =  title + "\n"+ address+"\nGoogle map to destination: " r"https://www.google.com/maps/dir/?api=1&destination="+addresshtml +"\n"+business_url+"\n"+"Review: "+wpurl+"\n\n"+ content + "\n"+rating+"\n"+date+"\n\n"+ get_hastags(address, title,'long')+"\n\nhttps://www.joeeatswhat.com"+"\n\n"
                instasession.video_upload(outputmontage, data)
    #           video2 = instasession.video_upload(outputmontage, data)
            except AttributeError  as error:
                print("  An error occurred uploading video to Instagram:", type(error).__name__)
                return False
        #media_pk = instasession.media_pk_from_url('https://www.instagram.com/p/CGgDsi7JQdS/')
        #media_path = instasession.video_download(media_pk)
        # joeeatswhat = instasession.user_info_by_username('timberjoe')
        # try: buildout = instagrapi.story.StoryBuilder(outputmontage,'Credits @timberjoe',[StoryMention(user=joeeatswhat)]).video(40)  # seconds
        # except AttributeError as error:
        #     print("  An error occurred uploading video to Instagram:", type(error).__name__) # An error occurred:
        # try: instasession.video_upload_to_story(buildout.path,"Credits @example",mentions=buildout.mentions,links=[StoryLink(webUri='https://www.joeeatswhat.com')],medias=[StoryMedia(media_pk=outputmontage)])
#         try:
#             instasession.video_upload_to_story(
#             outputmontage,
#             "Credits @joeeatswhat",
#  #           mentions=[StoryMention(user='timberjoe', x=0.49892962, y=0.703125, width=0.8333333333333334, height=0.125)],
#             links=[StoryLink(webUri='https://www.joeeatswhat.com')],
#   #          hashtags=[StoryHashtag(hashtag=get_hastags(address,title), x=0.23, y=0.32, width=0.5, height=0.22)],
#             #medias=[StoryMedia(media_pk=media_pk, x=0.5, y=0.5, width=0.6, height=0.8)],
#         )
#             story = instasession.story_photo("path/to/photo.jpg")
#             instasession.video_elements.add_link("https://www.joeeatswhat.com")
#             #story.add_link("https://www.joeeatswhat.com")
#             instasession.video_elements.add_hashtags(get_hastags)
#             story = instasession.video_upload_to_story(outputmontage)
#             story.upload()
#             #instasession.video_upload_to_story(path:outputmontage,caption:content, mentions:r'@timberjoe',links:'https://www.joeeatswhat.com',hashtags: hastag) ( path: outputmontage, caption: content, mentions:['@timberjoe'], links: ['https://www.joeeatswhat.com'], hashtags: get_hastags )
#             # temp = dict()
#             # temp = instasession.video_upload_to_story(path=outputmontage,caption=content,mentions=r'@timberjoe',links='https://www.joeeatswhat.com',hashtags=get_hastags)
#         except AttributeError as error:
#             print("  An error occurred uploading video to Instagram:", type(error).__name__) # An error occurred:
#             return False
        return True
    else:
        return False

##################################################################################################

def post_to_wordpress(title,content,headers,date,rating,address,picslist,outputs):
    """
    Post to WordPress.

    This function posts content to a WordPress site using the provided data.

    Args:
        title (str): The title of the post.
        content (str): The content of the post.
        headers: Headers for the request.
        date (str): The date of the post.
        rating (str): The rating of the post.
        address (str): The address associated with the post.
        picslist (list): A list of pictures for the post.
        outputs: Outputs for the post.

    Returns:
        None
"""
    # post
    newPost = False
    #countreview = False
    addresshtml = re.sub(" ", ".",address)
    googleadress = r"<a href=https://www.google.com/maps/dir/?api=1&destination="+\
        addresshtml + r">"+str(address)+r"</a>"
    contentpics = ''
    picl = picslist[1:-1]
    pic2 = picl.replace(",","")#re.sub(r',','',picl) #re.sub( r'[^a-zA-Z0-9]','',tempdate[1])
    pic3= pic2.replace("'","")
    pidchop = pic3.split(" ")
    linkslist=[]
    print ('    Figuring out date of Post : ',title)
    formatting = '%b/%Y/%d' #specifify the formatting of the date_string.
    date_string = date
    if "a day" in date_string:
        date = dt.timedelta(days=-1)
#        newdate = dt.datetime.strptime(date_string, formatting).date()
        newdate = datetime.today() - date
    else:
        if "day" in date:
            tempdate = -(int(re.sub( r'[^0-9]','',date_string)))
            print ('Stuff - > ',tempdate)
#           date = dt.timedelta(days=tempdate)
#            newdate = dt.datetime.strptime(date_string, formatting).date()
            newdate = datetime.today() + relativedelta(days=tempdate)
        else:
            if "a week" in date:
#               date = dt.timedelta(weeks= -1)
#                newdate = dt.datetime.strptime(date_string, formatting).date()
                newdate = datetime.today() - relativedelta(weeks= -1)
            else:
                if "week" in date:
                    tempdate = -(int(re.sub( r'[^0-9]','',date_string)))
                    print ('Stuff - > ',tempdate)
#                   date = dt.timedelta(weeks= tempdate)
#                    newdate = dt.datetime.strptime(date_string, formatting).date()
                    newdate = datetime.today() + relativedelta(weeks= tempdate)
                else:
                    if "a month" in date:
#                       date = dt.timedelta(months= -1)
#                        newdate = dt.datetime.strptime(date_string, formatting).date()
                        newdate = datetime.today() - relativedelta(months = -1)
                    else:
                        if "month" in date:
                            tempdate = -int(re.sub( r'[^0-9]','',date_string))
                            print ('Stuff - > ',tempdate)
#                           date = dt.timedelta(months= tempdate)
#                            newdate = dt.datetime.strptime(date_string, formatting).date()
                            newdate = datetime.today() + relativedelta(months =  tempdate)
                        else:
                            if "a year" in date:
#                               date = dt.timedelta(years= -1)
#                                newdate = dt.datetime.strptime(date_string, formatting).date()
                                newdate = datetime.today() - relativedelta(years= -1)
                            else:
                                if "year" in date:
                                    try:
                                        tempdate = -int(re.sub( r'[^0-9]','',date_string))
                                        print ('Stuff - > ',tempdate)
#                                       date = dt.timedelta( years= tempdate)
#                                    newdate = dt.datetime.strptime(date_string).date()
                                        newdate = datetime.today() + relativedelta(years= tempdate)
                                    except AttributeError  as error:
                                        print("    An error getting date occurred:",error)
                                else:
                                    formatting = '%Y-%b-%d' #specifify the formatting of the date_string.
                                    month = date[:3]
                                    year = date[3:]
                                    day = '01'
                                    date_string = year+'-'+ month+'-'+day
                                    try:
                                        newdate = dt.datetime.strptime(date_string, formatting).date()
                                    except AttributeError  as error:
                                        print("    An error getting date occurred:",error)
#                                    try:
#                                        newdate = dt.datetime.strptime(date_string, formatting).date()
#                                    except AttributeError as error:
#                                        print("    An error getting date occurred:", error)
                                    newdate = str(newdate)
    #formatting = '%b/%Y/%d' #specifify the formatting of the date_string.
    #newdate2 = dt.datetime.strptime(str(newdate), formatting).date()
    dateparts = (str(newdate)).split("-")
    dateparts2 = dateparts[2].split(" ")
    #dateparts = dateparts2[0]
#    print ('dateparts',dateparts)
    newdate2 = dateparts[0]+'-'+dateparts[1]+'-'+dateparts2[0]+'T22:00:00'
    #newdate2 = str(re.sub(r'-','/',str(newdate.date())))+'T22:00:00'
    print ('    Got Date: ', newdate2, newdate)
    try:
        post_id, post_link = check_wordpress_post(title,newdate2,headers)
        database_update_row(title,"wpurl",post_link,"forceall",outputs)
    except  AttributeError  as error :
        print ('Could not check to see post already exists',error)
    if not post_id:
        googleadress =  r"<a href=https://www.google.com/maps/dir/?api=1&destination="+addresshtml\
            + r">"+address+r"</a>"
        post_data = {
            "title": title,
    #        "content": address+'\n\n'+content+'\n'+rating+'\n\n' ,
            "content": googleadress+'\n\n'+content+'\n'+rating ,
            "status": "publish",  # Set to 'draft' if you want to save as a draft
            "date": newdate2,
    #       "date": str(newdate)+'T22:00:00',
        # "author":"joesteele"
        }
        try:
            headers2 = headers
            response = requests.post(env.wpAPOurl, json = post_data, headers=headers2,timeout=30)
            if response.status_code != 201:
                print ('Error: ',response, response.text)
            else:
                newPost = True
                post_id_json = response.json()
                post_id = post_id_json.get('id')
                print ('    New post is has post_id = ',post_id)
        except AttributeError  as error:
            print("An error occurred:", type(error).__name__) # An error occurred:
        #postneedsupdate = True
    else:
        print ('    Post already existed: Post ID : ',post_id)
    for pic in pidchop:
        picslice2 = pic.split("/")[-1]
        picslice = picslice2.split(".")
        picname = picslice[0]
        caption =title
        description = title+"\n"+address
        print ('    Found Picture: ',picname)
        file_id, link = check_wordpress_media(picname, headers)
#        link = linknew['rendered']
        if file_id is False:
            print ('      '+str(picname)+' was not already found in library, adding it')
#            countreview = True
            image = {
                "file": open(pic, "rb"),
                "post": post_id,
                "caption": caption,
                "description": description
            }
            try:
                image_response = requests.post(env.wpAPI + "/media", headers=headers, \
                    files=image,timeout=30)
            except AttributeError  as error:
                print("    An error uploading picture ' + picname+ ' occurred:", \
                    type(error).__name__)
            if image_response.status_code != 201 :
                print ('      Error- Image ',picname,' was not successfully uploaded.  response: ', \
                    image_response)
            else:
                pic_dic=image_response.json()
                file_id= pic_dic.get('id')
                link = pic_dic.get('guid').get("rendered")
                print ('      ',picname,' was successfully uploaded to website with ID: ',\
                    file_id, link)
            try:
                linksDict = {'file_id' : file_id , 'link' : link}
                linkslist.append(linksDict)
            except AttributeError  as error:
                print("    An error adding to dictionary " , file_id , link , " occurred:", \
                    type(error).__name__) # An error occurred:
        else:
            print ('    Photo ',picname,' was already in library and added to post with ID: ', \
                file_id,' : ',link)
            try:
                image_response = requests.post(env.wpAPI + "/media/" + str(file_id), \
                    headers=headers, data={"post" : post_id},timeout=30)
            except AttributeError  as error:
                print ('    Error- Image ',picname,' was not attached to post.  response: ',\
                    image_response+' '+type(error).__name__)
            try:
                post_response = requests.post(env.wpAPI + "/posts/" + str(post_id),\
                    headers=headers,timeout=30)
                if link in post_response.text:
                    print ('    Image link for ', picname, 'already in content of post: ' \
                        ,post_id, post_response.text, link)
                else:
                    linkslist.append({'file_id' : file_id , 'link' : link})
#                   countreview = True
            except AttributeError  as error:
                print("    An error loading the metadata from the post " + post_response.title + \
                    ' occurred: '+type(error).__name__)
    #ratinghtml = post_response.text
    first_mp4 = True
    fmedia = {}
    for piclink in linkslist:
        #for loop in linkslist:
        print ('    Adding ', piclink['link'], ' to posting')
        try:
            ext = piclink['link'].split( '.')[-1]
            if ext == 'mp4':
                if first_mp4:
                    contentpics += '\n' +r'[evp_embed_video url="' + piclink['link'] + \
                        r'" autoplay="true"]'
                    first_mp4 = False
                else:
                    contentpics += '\n' +r'[evp_embed_video url="' + piclink['link'] + r'"]'
#[evp_embed_video url="http://example.com/wp-content/uploads/videos/vid1.mp4" autoplay="true"]
            else:
                contentpics += '\n '+r'<div class="col-xs-4"><img id="'+str(file_id)+r'"' + r'src="' + \
                    piclink['link'] + r'"></div>'
#               fmedia.append = piclink{'file_id' }
#            contentpics += '\n '+r'<img src="'+ piclink['link'] + '> \n'
            #contentpics += r'<img src="'+ piclink['link'] + r' alt="' + title +r'">' +'\n\n'
        except AttributeError  as error:
            print("An error occurred:", type(error).__name__) # An error occurred:
            return False
    try:
#        print ('featured_media = ',linkslist[0]['file_id'])
        if linkslist[0]['file_id']:
            print ('featuredmedia2 = ',linkslist[0]['file_id'])
        else:
            fmedia = file_id
#            print ('featured_media2 = ',file_id)
        business_url_list = outputs['postssession'].query(Posts).filter(Posts.name == title).all()
        business_url = business_url_list[0].businessurl
        # wpurllist = outputs['postssession'].query(Posts).filter(Posts.name == title).all()
        # wpurl = wpurllist[0].wpurl
        if business_url:
            status_message = str(title) + ': Business website: '+ business_url
            response_piclinks = requests.post(env.wpAPI+"/posts/"+ str(post_id), \
                data={"content" : title+' = '+status_message+'\n\n'+content+'\n'+googleadress+'\n'+rating  + contentpics,\
                "featured_media" : fmedia,"rank_math_focus_keyword" : title }, headers=headers,\
                timeout=30)
            print ('  ',response_piclinks)
    except AttributeError  as error:
        print("    An error writing images to the post " + post_response.title + ' occurred:', \
            type(error).__name__) # An error occurred')
        return False
    return newPost

##################################################################################################

def process_reviews(outputs):
    # Process
    webcount = xtwittercount = instagramcount = facebookcount = 0
#    webcount=xtwittercount=instagramcount=yelpcount=threadscount=facebookcount=tiktokcount = 0
    rows = list((outputs['data'].iter_rows(min_row=1, max_row=outputs['data'].max_row)))
    if env.google:
        print('Configuration says to update google Reviews prior to processing them')
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        options.add_argument("--ignore-certificate-error")
        options.add_argument("--ignore-ssl-errors")
        if not env.showchrome:
            options.add_argument("--headless")
            # show browser or not ||| HEAD =>  43.03 ||| No Head => 39 seg
        options.add_argument("--lang=en-US")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--remote-debugging-pipe")
        # Exclude the collection of enable-automation switches
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # Turn-off userAutomationExtension
        options.add_experimental_option("useAutomationExtension", False)
        # Setting the driver path and requesting a page
        caps = webdriver.DesiredCapabilities.CHROME.copy()
        caps['acceptInsecureCerts'] = True
        caps['acceptSslCerts'] = True
        options.set_capability('cloud:options', caps)
        #driver = webdriver.Chrome(desired_capabilities=caps)
        if is_docker() :
            driver = webdriver.Remote("http://192.168.10.9:4444/wd/hub", options=options)
            print ("IN A DOCKER CONTAINER, USING REMOTE CHROME")
        else:
            driver = webdriver.Chrome(options=options) # Firefox(options=options)
        # Changing the property of the navigator value for webdriver to undefined
        driver.execute_script("Object.defineProperty(navigator,'webdriver',\
                            {get:()=> undefined})")
        driver.get(env.URL)
        time.sleep(5)
        google_scroll(counter_google(driver), driver)
        webdata = get_google_data(driver,outputs)
        write_to_xlsx2(webdata, outputs)
        driver.close()
        # outputs['data'].save(xls)
        print('Done getting google reviews and writing them to xls file !')
    else:
        print ('Configuration says to skip creation of new reviews from google for this run')
    if env.needreversed:
        rows = reversed(rows)
    print('Processing Reviews')
    for processrow in rows:
        if processrow[1].value != "name":  # Skip header line of xls sheet
            print ("Processing : ",processrow[1].value)
            writtento = (ast.literal_eval(processrow[9].value))
            # Check to see if the website has already been written to according to the xls sheet,\
            # if it has not... then process
            if (writtento["web"] == 0 or writtento["instagram"]==0 or writtento["facebook"]==0 or \
                writtento["xtwitter"]==0 or writtento["yelp"]==0 or writtento["tiktok"]==0 or \
                writtento["threads"]==0 ) and (check_is_port_open(env.wpAPI, 443)) and (env.web \
                or env.instagram or env.yelp or env.xtwitter or env.tiktok or env.facebook or \
                env.threads or env.google)and (processrow[2].value is not None) :
                if env.web :
                    #if writtento["web"] == 0 :
                    try:
                        if env.forcegoogleupdate:
                            post_id, post_link = get_wordpress_post_id_and_link(processrow[1].value,outputs['web'] )
                            if post_link:
                                database_update_row(processrow[1].value,"wpurl",post_link,"forceall",outputs)
                            else:
                                print ('  Error getting wordpress links to update databse')
                    except  AttributeError  as error :
                        print ('Could not check to see post already exists',error)
                    if len(outputs['postssession'].query(Posts).filter(Posts.name == processrow[1].\
                            value,Posts.web is not False).all()) == 0:
                        if webcount < env.postsperrun:
                            try:
                                new_web_post=post_to_wordpress(processrow[1].value,processrow[2].\
                                    value,outputs['web'] ,processrow[7].value, processrow[3].value\
                                    , processrow[8].value, processrow[5].value,outputs)
                                print ('  Success Posting to Wordpress: '+processrow[1].value)
                                if new_web_post:
                                    webcount +=1
                                    try:
                                        print('  write to xls for web')
                                        outputs['datawb'].save(env.xls)
                                        print('  Successfully updated spreadsheet')
                                    except AttributeError  as error:
                                        print("  An error occurred writing Excel file:", type(error).__name__)
                                    try:
                                        print('  write to DB for web')
                                        outputs['postssession'].query(Posts).filter(Posts.name == processrow[1].value).update({"web" : 1})
                                        outputs['postssession'].commit()
                                        print('  Successfully wrote to database')
                                    except AttributeError  as error:
                                        print("  An error occurred writing database", type(error).__name__)
                            except AttributeError  as error:
                                print ('  Error writing web post : ',processrow[1].value, processrow[2].value,processrow[7].value, processrow[3].value,processrow[8].value, processrow[5].value, writtento["web"],' ',error)
                                print (error)
                        else:
                            print ('  Exceeded the number of web posts per run, skipping', processrow[1].value)
                    else:
                        print ('  Website: Skipping posting for ',processrow[1].value,' previously written')
                if env.instagram:
                    if len(outputs['postssession'].query(Posts).filter(Posts.name == processrow[1].value,Posts.instagram is not False).all()) == 0:
                        if instagramcount < env.postsperrun:
                            try:
                                print('  Starting to generate Instagram post')
                                NewInstagramPost = post_to_instagram2(processrow[1].value, processrow[2].value, processrow[7].value, processrow[3].value, processrow[8].value, processrow[5].value,outputs['instagram'],outputs )
                                try:
                                    print ('  Start generating content to post to Instagram')
                                    writtento["instagram"] = 1
                                    processrow[9].value = str(writtento)
                                except AttributeError  as error:
                                    print("  An error occurred setting value to go into Excel file:", type(error).__name__)
                                print ('  Success Posting to Instagram: '+processrow[1].value)
                                if NewInstagramPost:
                                    instagramcount +=1
                                    try:
                                        print('  write to xls for instagram')
                                        outputs['datawb'].save(env.xls)
                                        print('  write to mariadb for instagram')
                                    except AttributeError  as error:
                                        print("  An error occurred writing Excel file:", type(error).__name__)
                                    try:
                                        print('  write to DB for instagram')
                                        outputs['postssession'].query(Posts).filter(Posts.name == processrow[1].value).update({"instagram" : 1})
                                        outputs['postssession'].commit()
                                        print('  Successfully wrote to database')
                                    except AttributeError  as error:
                                        print("  An error occurred writing database", type(error).__name__)
                            except AttributeError  as error:
                                print ('  Error writing Instagram post : ',processrow[1].value, processrow[2].value, outputs['instagram'],processrow[7].value, processrow[3].value,processrow[8].value, processrow[5].value, writtento["instagram"], type(error).__name__ )
                        else:
                            print ('  Exceeded the number of Instagram posts per run, skipping', processrow[1].value)
                    else:
                        print ('  Instagram: Skipping posting for ',processrow[1].value,' previously written')
                if env.facebook:
                    if len(outputs['postssession'].query(Posts).filter(Posts.name == processrow[1].value,Posts.facebook is not False).all())==0:
                        if facebookcount < env.postsperrun:
                            try:
                                print('  Starting to generate Facebook post')
                                NewFacebookPost = post_facebook3(processrow[1].value, processrow[2].value, processrow[7].value, processrow[3].value, processrow[8].value, processrow[5].value,outputs['facebook'] )
                                try:
                                    print ('  Start generating content to post to facebook')
                                    writtento["facebook"] = 1
                                    processrow[9].value = str(writtento)
                                except AttributeError  as error:
                                    print("  An error occurred setting value to go into Excel file:", type(error).__name__)
                                print ('  Success Posting to facebook: '+processrow[1].value)# ',processrow[1].value, processrow[2].value, headers,processrow[7].value, processrow[3].value,processrow[8].value, processrow[5].value, temp3["web"] )
                                if NewFacebookPost:
                                    facebookcount +=1
                                    try:
                                        print('  write to xls for facebook')
                                        outputs['datawb'].save(env.xls)
                                        print('  write to mariadb for facebook')
                                    except AttributeError  as error:
                                        print("  An error occurred writing Excel file:", type(error).__name__)
                                    try:
                                        print('  write to DB for facebook')
                                        outputs['postssession'].query(Posts).filter(Posts.name == processrow[1].value).update({"facebook" : 1})
                                        outputs['postssession'].commit()
                                        print('  Successfully wrote to database')
                                    except AttributeError  as error:
                                        print("  An error occurred writing database", type(error).__name__)
                            except AttributeError  as error:
                                print ('  Error writing facebook post : ',processrow[1].value, processrow[2].value, outputs,processrow[7].value, processrow[3].value,processrow[8].value, processrow[5].value, writtento["facebook"], type(error).__name__ )
                        else:
                            print ('  Exceeded the number of facebook posts per run, skipping', processrow[1].value)
                    else:
                        print ('  Facebook: Skipping posting for ',processrow[1].value,' previously written')
                if env.xtwitter:
                    #if writtento["xtwitter"] == 0:
                    #               # if Posts.query.filter(Posts.name.xtwitter.op('!=')(1)).first()
                    tempval = len(outputs['postssession'].query(Posts).filter(Posts.name == processrow[1].value,Posts.xtwitter is not False).all())
                    print ('tempval: ',tempval)
                    if len(outputs['postssession'].query(Posts).filter(Posts.name == processrow[1].value,Posts.xtwitter is not False).all())==0:
                        if xtwittercount < env.postsperrun:
                            try:
                                print('  Starting to generate xtwitter post')
                                NewxtwitterPost = post_to_x2(processrow[1].value, processrow[2].value, processrow[7].value, processrow[3].value, processrow[8].value, processrow[5].value,outputs['posts'],outputs )
                                try:
                                    print ('    Start generating content to post to xtwitter')
                                    writtento["xtwitter"] = 1
                                    processrow[9].value = str(writtento)
                                except AttributeError  as error:
                                    print("  An error occurred setting value to go into Excel file:", type(error).__name__) # An error occurred:
                                    print ('  Success Posting to xtwitter: '+processrow[1].value)# ',processrow[1].value, processrow[2].value, headers,processrow[7].value, processrow[3].value,processrow[8].value, processrow[5].value, temp3["web"] )
                                if NewxtwitterPost:
                                    xtwittercount +=1
                                    try:
                                        print('  write to xls for xtwitter')
                                        outputs['datawb'].save(env.xls)
                                        print('  Successfully wrote to xls for xtwitter')
                                        # outputs['postssession'].update('dictPostComplete = '+str(writtento)+' where name == '+processrow[1].value)
                                        # outputs['postssession'].commit()
                                    except AttributeError  as error:
                                        print("  An error occurred writing Excel file:", type(error).__name__) # An error occurred:
                                    try:
                                        print('  write to DB for xtwitter')
                                        outputs['postssession'].query(Posts).filter(Posts.name == processrow[1].value).update({"xtwitter" : 1})
                                        outputs['postssession'].commit()
                                        print('  Successfully wrote to database')
                                    except AttributeError  as error:
                                        print("  An error occurred writing database", type(error).__name__)
                            except AttributeError as error:
                                print ('  Error writing xtwitter post : ',error,processrow[1].value, processrow[2].value, outputs,processrow[7].value, processrow[3].value,processrow[8].value, processrow[5].value, writtento["xtwitter"], type(error).__name__ )
                        else:
                            print ('  Exceeded the number of xtwitter posts per run, skipping', processrow[1].value)
                    else:
                        print ('  Xtwitter: Skipping posting for ',processrow[1].value,' previously written')
    #post_to_x_example(title, content, date, rating, address, picslist, instasession)
    # else:
    #     print ('Exceeded the number of posts per run, exiting')
                # if xtwitter:
                #     namedict = {'name':'xtwitter', 'namecount':xtwittercount, 'namepost':'NewxtwitterPost', 'subroutine':post_to_x_example}
                #    # junction('xtwitter',xtwittercount,'NewxtwitterPost','post_to_x_example', outputs, writtento, processrow)
                #     socials('xtwitter',namedict,outputs,writtento, processrow,post_to_x_example)
    return #(outputs['web'])

##################################################################################################

if __name__ == "__main__":
    print('starting ...')
    preload()
    print('making connections ...')
    outputs = get_auth_connect()
    process_reviews(outputs)
    print('Done!')

##################################################################################################