import sqlalchemy
from env import *

#data
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
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

#instagram
import ast
import base64
import requests
from openpyxl import Workbook, load_workbook
import datetime as dt
import json
import jsonpickle

#Instgram
#from instapy import InstaPy
#import instapy
#from instabot import Bot
import pathlib
import instagrapi
from instagrapi.types import StoryMention, StoryMedia, StoryLink, StoryHashtag
from instagrapi.story import StoryBuilder
from moviepy.editor import *
import moviepy

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
#import mysqlclient
#import mysql-connector-python
Base = declarative_base()

##################################################################################################

def preload():
    file=pathlib.Path("./config/joeteststeele_uuid_and_cookie.json")
    if pathlib.Path.exists(file):
        pathlib.Path.unlink(file)
    global today
    today = datetime.today().strftime('%Y-%m-%d')
    return

##################################################################################################    

class Users(Base):
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
    #active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

##################################################################################################

def authconnect():
    connections = {}
    if mariadb:
        print('Connecting to MariaDB for configuration and storage')
        from sqlalchemy import create_engine
        engine = sqlalchemy.create_engine("mysql+mysqldb://"+mariadbuser+":"+mariadbpass+"@"+mariadbserver+"/"+mariadbdb+"?charset=utf8mb4", echo=False)        
        Session = sqlalchemy.orm.sessionmaker()
        Session.configure(bind=engine)
        session = Session()
        usersession = session.query(Users).filter(Users.user=='joesteele')
        dbuser = usersession[0]
        #for userloop in usersession:
        print(" - " + dbuser.user + ' ' + dbuser.googleurl)
        connections.update({'user':dbuser})
        posts = session.query(Posts).all()
        connections.update({'posts':posts})
        connections.update({'postssession':session})
    if data:
        print('  loading XLS content data source ...')
        if (os.path.exists(xls)):
            wb = load_workbook(filename = xls)
            xlswbDF = pd.read_excel(xls)
        else:
            if (os.path.exists('./GoogleScrape/'+ xls)):
                wb = load_workbook(filename = './GoogleScrape/'+ xls)
                xlswbDF = pd.read_excel('./GoogleScrape/'+ xls)
            else:
                input("Not able to find xls file Press any key to continue...")   
        ws = wb['Sheet1']
        #xlswbDF = pd.read_excel(xls)
        connections.update({'xlsdf':xlswbDF})
        connections.update({'data':ws})
        connections.update({'datawb':wb})
    if instagram :
        print('  Connecting to Instagram ...')
        instasessionclient = instagrapi.Client()
        instasessionclient.login(instagramuser, instagrampass)
        connections.update({'instagram':instasessionclient})
    if facebook :
        print('  Connecting to facebook ...')
        # msg = 'Purple Ombre Bob Lace Wig Natural Human Hair now available on https://lace-wigs.co.za/'
        # page_id_1 = facebookpageID
        # facebook_access_token = 'paste-your-page-access-token-here'
        # image_url = 'https://graph.facebook.com/{}/photos'.format(page_id_1)
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
    if yelp :
        print('  Connecting to yelp ...')
    if xtwitter :
        print('  Connecting to xtwitter ...')
    if threads :
        print('  Connecting to threads ...')
    if web :
        print('  Connecting to joeeatswhat.com ...')
        data_string = f"{user}:{password}"
        token = base64.b64encode(data_string.encode()).decode("utf-8")
        headers = {"Authorization": f"Basic {token}"}
        connections.update({'web' : headers})
    if tiktok :
        print('  Connecting to Instagram ...')
    return connections

##################################################################################################

# Grab a count of how far we need to scroll
def counter(driver):
    result = driver.find_element(By.CLASS_NAME,'Qha3nb').text
    result = result.replace(',', '')
    result = result.split(' ')
    result = result[0].split('\n')
    return int(int(result[0])/10)+1

##################################################################################################

def post_facebook(title, content, date, rating, address, picslist, instasession):
    #msg = 'Purple Ombre Bob Lace Wig Natural Human Hair now available on https://lace-wigs.co.za/'
    pics = ((picslist[1:-1].replace(",","")).replace("'","")).split(" ")
    page_id_1 = facebookpageID
    facebook_access_token = facebookpass
    #facebook_access_token = 'paste-your-page-access-token-here'
#    image_url = 'https://graph.facebook.com/{}/feed'.format(page_id_1)
    image_url = 'https://graph.facebook.com/{}/photos'.format(page_id_1)
    image_location = pics[0]
    img_payload = {
    'message': content,
    'url': image_location,
    'access_token': facebook_access_token
    }
    #Send the POST request
    r = requests.post(image_url, data=img_payload)
    print('    Facebook response: ',r.text, img_payload)
    return  (r)

##################################################################################################

def postImage(group_id, img,auth_token):
    files={}
    url = f"https://graph.facebook.com/{group_id}/photos?access_token=" + auth_token
    for eachfile in img:
        files.update({eachfile: open(eachfile, 'rb')})
    data = {
        "published" : False
    }
    try: 
        r = requests.post(url, files=files, data=data).json()
    except Exception as error:
        print("    An error getting date occurred:", type(error).c) # An error occurred:
        r = False
    time.sleep(facebooksleep)
    return r

##################################################################################################

def postVideo(group_id, video_path,auth_token,title, content, date, rating, address):
    url = f"https://graph-video.facebook.com/{group_id}/videos?access_token=" + auth_token
    files={}
    addresshtml = re.sub(" ", ".",address)
    #args={}
    #data["message"]=title + "\n"+address+"\n\n"+ content + "\n"+rating+"\n"+date
    for eachfile in video_path:
       # my_dict['key'].append(1)
        files.update({eachfile: open(eachfile, 'rb')})
    data = { "title":title,"description" : title + "\n"+ address+"\nGoogle map to destination: "
             r"https://www.google.com/maps/dir/?api=1&destination="+addresshtml +"\n\n"+ content + "\n"+rating+"\n"+date+"\n\n"+ hastags(address, title)+"\n\nhttps://www.joeeatswhat.com"+"\n\n","published" : True
    }
    #try: r = requests.post(url, files=files, data=data)
    try: r = requests.post(url, files=files, data=data).json()
    except Exception as error:
        print("    An error getting date occurred:", type(error).c) # An error occurred:
        r = False
    time.sleep(facebooksleep)
    print (r)
    print ('r id  = ',r['id'])
    return r

##################################################################################################

def post_facebook2(title, content, date, rating, address, picslist, instasession):
    #msg = 'Purple Ombre Bob Lace Wig Natural Human Hair now available on https://lace-wigs.co.za/'
    pics = ((picslist[1:-1].replace(",","")).replace("'","")).split(" ")
    group_id = facebookpageID
    auth_token = facebookpass
    page_id_1 = facebookpageID
    facebook_access_token = facebookpass
    imgs_id = []
    imgs_vid = []
    imgs_pic = []
    img_list = pics
    for img in img_list:
        if ('.mp4' in img ):
            imgs_vid.append(img)
        else:
            imgs_pic.append(img)
    # if (imgs_vid ):
    #     print ("loop")
    #     try: 
    #         post_id = postVideo(group_id, imgs_vid,auth_token)
    #         imgs_id.append(post_id['id'])
    #     except Exception as error:
    #         print("    An error occurred:", type(error).c) # An error occurred:
    if (imgs_pic):
        try: 
            post_id = postImage(group_id ,imgs_pic,auth_token)
            imgs_id.append(post_id['id'])
        except Exception as error:
            print("    An error occurred:", type(error)) # An error occurred:

    # try: 
    #     imgs_id.append(post_id['id'])
    # except Exception as error:
    #     print("    An error occurred:", type(error).c) # An error occurred:
    args=dict()
 #   args['title']= title
    args["message"]=title + "  "+ content
    for img_id in imgs_id:
        key="attached_media["+str(imgs_id.index(img_id))+"]"
        args[key]="{'media_fbid': '"+img_id+"'}"
    #url = f"https://graph.facebook.com/me/feed?access_token=" + auth_token
    url = f"https://graph.facebook.com/{group_id}/feed?access_token=" + auth_token
    #print ("r = request.post(" +url+", data="+args+")")
    try: r = requests.post(url, data=args)
    #try: r = requests.post(url, data=args).json()
    except Exception as error:
        print("    An error getting date occurred:", type(error).c) # An error occurred:
        r = False
    time.sleep(facebooksleep)
    print('    Facebook response: ',r)
    return  (r)

##################################################################################################

def post_facebook3(title, content, date, rating, address, picslist, instasession):
    pics = ((picslist[1:-1]).replace("'","")).split(",")
    group_id = facebookpageID
    auth_token = facebookpass
    page_id_1 = facebookpageID
    facebook_access_token = facebookpass
    imgs_id = []
    imgs_vid = []
    imgs_pic = []
    img_list = pics
    for img in img_list:
        if ('montage.mp4' in img ):
            imgs_vid.append(img.strip())
        else:
            imgs_pic.append(img.strip())
    if (imgs_vid ):
       # print ("loop")
        try: 
            post_id = postVideo(group_id, imgs_vid,auth_token,title, content, date, rating, address)
            imgs_id.append(post_id['id'])
        except Exception as error:
            print("    An error occurred:", type(error).c) # An error occurred:
    time.sleep(facebooksleep)
    print('    Facebook response: ',post_id)
    return  (True)

##################################################################################################
   

def get_data(driver,outputs ):

#     curl -X GET -H 'Content-Type: application/json' -H "X-Goog-Api-Key: API_KEY" -H "X-Goog-FieldMask: id,displayName,formattedAddress,plusCode" https://places.googleapis.com/v1/places/ChIJj61dQgK6j4AR4GeTYWZsKWw #placeId #websiteUri  AIzaSyB_hglzM7N8HzjXwi1dF1E8WYTql3akS7Q
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
        try: address = data.find_element(By.CSS_SELECTOR, 'div.RfnDt.xJVozb').text
        except: address = 'Unknonwn'
        print ('Name of location: ',name, '   Address:',address)
        try: visitdate = data.find_element(By.CSS_SELECTOR, 'span.rsqaWe').text
        except: visitdate = "Unknown"
        print('Visited: ',visitdate)  
        try: text = data.find_element(By.CSS_SELECTOR, 'div.MyEned').text 
        except: text = '' 
        try: score = data.find_element(By.CSS_SELECTOR, 'span.kvMYJc').get_attribute("aria-label")  #find_element(By.CSS_SELECTOR,'aria-label').text #)  ##QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf > div.m6QErb > div:nth-child(3) > div:nth-child(2) > div > div:nth-child(4) > div.DU9Pgb > span.kvMYJc
        except: score = "Unknown"
        more_specific_pics = data.find_elements(By.CLASS_NAME, 'Tya61d') 
        pics= [] 
        pics2 = []
        # check to see if folder for pictures and videos already exists, if not, create it
        cleanname = re.sub( r'[^a-zA-Z0-9]','', name)
        if not os.path.exists('./Output/Pics/'+cleanname):
            os.makedirs('./Output/Pics/'+cleanname)
        # Walk through all the pictures and videos for a given review
        for lmpics in more_specific_pics:  
            # if pics2 and not pics:
            #     pics2 = []
            # Grab URL from style definiton (long multivalue string), and remove the -p-k so that it is full size 
            urlmedia = re.sub('=\S*-p-k-no', '=-no', (re.findall(r"['\"](.*?)['\"]", lmpics.get_attribute("style")))[0])
            print ('URL : ',urlmedia)
            pics.append(urlmedia)
            # Grab the name of the file and remove all spaces and special charecters to name the folder
            filename = re.sub( r'[^a-zA-Z0-9]','', str(lmpics.get_attribute("aria-label")))
            if lmpics == more_specific_pics[0]:
                lmpics.click()
                time.sleep(2)
                #iframe = driver.find_element(By.TAG_NAME, "iframe")
                tempdate = str((driver.find_element(By.CLASS_NAME,'mqX5ad')).text).rsplit("-",1)
                visitdate = re.sub( r'[^a-zA-Z0-9]','',tempdate[1])
                print ('Visited: ',visitdate)
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
            if not os.path.exists('./Output/Pics/'+cleanname+'/'+visitdate):
                os.makedirs('./Output/Pics/'+cleanname+'/'+visitdate)
            if not os.path.isfile('./Output/Pics/'+cleanname+'/'+visitdate+'/'+filename):
                urlretrieve(urlmedia, './Output/Pics/'+cleanname+'/'+visitdate+'/'+filename)
            # Store the local path to be used in the excel document
            picsLocalpath = "./Output/Pics/"+cleanname+"/"+visitdate+'/'+filename
            pics2.append(picsLocalpath)
        if pics2:
            make_video(pics2)
            pics2.append("./Output/Pics/"+cleanname+"/"+visitdate+'/'+'montage.mp4') 
        dictPostComplete= {'google':1,'web':0,'yelp':0,'facebook':0,'xtwitter':0,'instagram':0,'tiktok':0}
        lst_data.append([name , text, score,pics,pics2,"GoogleMaps",visitdate,address,dictPostComplete])
  
    return lst_data

##################################################################################################

# Do the scrolling
def scrolling(counter,driver):
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

##################################################################################################

def write_to_xlsx(webdata, outputs):
    print('Start to write to excel...')
    cols = ["name", "comment", 'rating','picsURL','picsLocalpath','source','date','address','dictPostComplete']
    # rows = list((outputs['data'].iter_rows(min_row=1, max_row=outputs['data'].max_row)))
    rows = list(webdata)
    if needreversed:
        rows = reversed(rows)
    for processrow in rows:
        print (processrow[4], processrow[0])
        if (processrow[4] in outputs['data']) and (processrow[0] in outputs['data']):
            print ('  Row ',processrow[0],'  already in XLS sheet')
        else:
            if (processrow[0] != None):
#                processrow.append({'google':1,'web':0,'yelp':0,'facebook':0,'xtwitter':0,'Instagram':0,'tiktok':0})
                outputs['data'].append([processrow[0],processrow[1],processrow[2],str(processrow[3]),str(processrow[4]),str(processrow[5]),str(processrow[6]),str(processrow[7]),str(processrow[8])]) # sheet_obj.append([col1, col2])
                #outputs['data'].parent.save(xls)
    #outputs['datawb'].save(xls)
    cols = ['num',"name", "comment", 'rating','picsURL','picsLocalpath','source','date','address','dictPostComplete', 'test']
    df = pd.DataFrame(outputs['data'], columns=cols)
    df.to_excel(xls)
    return True

    #df = pd.DataFrame(data, columns=cols)
    #df.to_excel('./Output/reviews.xlsx')

def write_to_xlsx2(data, outputs):
    print('write to excel...')
    sqlalchemy.null()
    cols = ["name", "comment", 'rating','picsURL','picsLocalpath','source','date','address','dictPostComplete']
    cols2 = ["num","name", "comment", 'rating','picsURL','picsLocalpath','source','date','address','dictPostComplete']
    df = pd.DataFrame(data, columns=cols)
    df2 = pd.DataFrame(outputs['xlsdf'].values, columns=cols2)
    #df2 = df1.where((pd.notnull(df)), None)  # take out NAN problems
    #df3.astype(object).where(pd.notnull(df2), None)
    print ('Dropped items not included in sync to database: ',df2.dropna(inplace=True))
    rows = list(data)
    if needreversed:
        rows = reversed(rows)
    #jsonposts = json.dumps(outputs['posts'], default=Posts)
    print("Encode Object into JSON formatted Data using jsonpickle")
    jsonposts = jsonpickle.encode(outputs['posts'], unpicklable=False)
    for processrow in df2.values:
        if  (processrow[1] in df.values):
            print ('  Row ',processrow[0],' ', processrow[1],'  already in XLS sheet')
            d2_row = Posts(name=processrow[1],comment=processrow[2],rating=processrow[3],picsURL=processrow[4],picsLocalpath=processrow[5],source=processrow[6],date=processrow[7],address=processrow[8],dictPostComplete=processrow[9])
            # if not (processrow[1] in outputs['posts']) : 
            #     outputs['postssession'].add(d2_row)
            #     outputs['postssession'].commit()
        else:
            if (processrow[1] != None):
                # Create a Python dictionary object with all the column values
                d_row = {'name':processrow[1],'comment':processrow[2],'rating':processrow[3],'picsURL':processrow[4],'picsLocalpath':processrow[5], 'source':processrow[6],'date':processrow[7],'address':processrow[8],'dictPostComplete':processrow[9]}
                d2_row = Posts(name=processrow[1],comment=processrow[2],rating=processrow[3],picsURL=processrow[4],picsLocalpath=processrow[5],source=processrow[6],date=processrow[7],address=processrow[8],dictPostComplete=processrow[9])
                print ('  Row ',processrow[0],' ', processrow[1],'  added to XLS sheet')
        # Append the above Python dictionary object as a row to the existing pandas DataFrame
        # Using the DataFrame.append() function
        try:
            if (processrow[1] in jsonposts) : #outputs['posts']):
                print ('  Row ',processrow[0],' ', processrow[1],'  already in Database')
            else:
                outputs['postssession'].add(d2_row)
                outputs['postssession'].commit()
                print ('  Row ',processrow[0],' ', processrow[1],'  added to Database')
        except Exception as error:
            print('    Not able to write to post data table: ' , type(error))
            outputs['postssession'].rollback()
            raise
    df.to_excel(xls)
    return data

##################################################################################################

def database_read(data):
    from sqlalchemy import create_engine
    import pandas as pd
    db_connection_str = 'mysql+pymysql://mysql_user:mysql_password@mysql_host/mysql_db'
    db_connection = create_engine(db_connection_str)
    df = pd.read_sql('SELECT * FROM table_name', con=db_connection)
    return df

##################################################################################################


def check_web_media(filename,headers):
    file_name_minus_extension = filename
    response = requests.get(wpAPI + "/media?search="+file_name_minus_extension, headers=headers)
    try:
        result = response.json()
        file_id = int(result[0]['id'])
        link = result[0]['guid']['rendered']
        return file_id, link
    except Exception as error:
        print('    No existing media with same name in Wordpress media folder: ' + filename)
        return False, False
 
##################################################################################################
       
def check_web_post(postname,postdate,headers):
    response = requests.get(wpAPI+"/posts?search="+postname, headers=headers)
    try:
        result = response.json()
        post_id = int(result[0]['id'])
        post_date = result[0]['date']
        if postdate == post_date:
            return post_id
    except: 
        print('No existing post with same name: ' + postname)
    return False

##################################################################################################
    
def is_port_open(host, port):
    try:
        isWebUp = urllib3.request("GET", host)
        if isWebUp.status == 200:
            return True
    except Exception as error:
        print ('Could not open port to website: ', host,  type(error))
        return False     

##################################################################################################
    
def check_media(filename, headers):
    # Regex gilename to format like in WordPress media name
    #file_name_minus_extension = re.sub(r'\'|(....$)','', filename, flags=re.IGNORECASE)
    file_name_minus_extension = filename
    response = requests.get(wpAPI + "/media?search="+file_name_minus_extension, headers=headers)
    try:
        result = response.json()
        file_id = int(result[0]['id'])
        link = result[0]['guid']['rendered']
        return file_id, link
    except Exception as error:
        print('    No existing media with same name in Wordpress media folder: ' + filename)
        return False, False
    
##################################################################################################
    
def check_post(postname,postdate,headers2):
    response = requests.get(wpAPI+"/posts?search="+postname, headers=headers2)
    result = response.json()
    if len(result) > 0 :
        post_id = int(result[0]['id'])
        post_date = result[0]['date']
        if postdate == post_date:
            return post_id
        else: #  Exception as error:
            print('No existing post with same name: ' + postname)
            return False
    else:
        print('No existing post with same name: ' + postname)
        return False

##################################################################################################

def post_x(title, content, date, rating, address, picslist, instasession):
    pics = ((picslist[1:-1]).replace("'","")).split(",")
    from requests_oauthlib import OAuth1Session
    # Be sure to add replace the text of the with the text you wish to Tweet. You can also add parameters to post polls, quote Tweets, Tweet with reply settings, and Tweet to Super Followers in addition to other features.
    payload = {"text": content}
    # Get request token
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        print("There may have been an issue with the consumer_key or consumer_secret you entered.")
    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_secret")
    print("Got OAuth token: %s" % resource_owner_key)
    # Get authorization
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)
    print("Please go here and authorize: %s" % authorization_url)
    verifier = input("Paste the PIN here: ")
    # Get the access token
    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier,
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]
    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )
    # Making the request
    response = oauth.post("https://api.twitter.com/2/tweets",json=payload)
    if response.status_code != 201:
        raise Exception("Request returned an error: {} {}".format(response.status_code, response.text) )
    print("Response code: {}".format(response.status_code))
    # Saving the response as JSON
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))
    return

##################################################################################################


def post_to_wp(title, content,  headers,date, rating,address, picslist):
    # post
    NewPost = False
    countreview = False
    addresshtml = re.sub(" ", ".",address)
    googleadress = r"<a href=https://www.google.com/maps/dir/?api=1&destination="+addresshtml + r">"+address+r"</a>" # https://www.google.com/maps/dir/?api=1&destination=760+West+Genesee+Street+Syracuse+NY+13204
    contentpics = ''
    picl = picslist[1:-1] 
    pic2 = picl.replace(",","")#re.sub(r',','',picl) #re.sub( r'[^a-zA-Z0-9]','',tempdate[1])
    pic3= pic2.replace("'","")
#    print (pic3)
    pidchop = pic3.split(" ")
    linkslist=[]
    # linkslist.clear
    print ('    Figuring out date of Post : ',title)
    format = '%b/%Y/%d' #specifify the format of the date_string.
    date_string = date
    if "a day" in date_string:
        date = dt.timedelta(days=-1)
#        newdate = dt.datetime.strptime(date_string, format).date()
        newdate = datetime.today() - date
    else:
        if "day" in date:
            tempdate = -(int(re.sub( r'[^0-9]','',date_string)))
            print ('Stuff - > ',tempdate)
 #           date = dt.timedelta(days=tempdate)
#            newdate = dt.datetime.strptime(date_string, format).date()
            newdate = datetime.today() - relativedelta(days=tempdate)
        else:
            if "a week" in date:
 #               date = dt.timedelta(weeks= -1)  
#                newdate = dt.datetime.strptime(date_string, format).date()
                newdate = datetime.today() - relativedelta(weeks= -1) 
            else:
                if "week" in date:
                    tempdate = -(int(re.sub( r'[^0-9]','',date_string)))
                    print ('Stuff - > ',tempdate)
 #                   date = dt.timedelta(weeks= tempdate)  
#                    newdate = dt.datetime.strptime(date_string, format).date()
                    newdate = datetime.today() - relativedelta(weeks= tempdate)
                else:
                    if "a month" in date:
 #                       date = dt.timedelta(months= -1)
#                        newdate = dt.datetime.strptime(date_string, format).date()
                        newdate = datetime.today() - relativedelta(months = -1)
                    else:
                        if "month" in date:
                            tempdate = -int(re.sub( r'[^0-9]','',date_string))
                            print ('Stuff - > ',tempdate)
 #                           date = dt.timedelta(months= tempdate)
#                            newdate = dt.datetime.strptime(date_string, format).date()
                            newdate = datetime.today() - relativedelta(months =  tempdate)
                        else:
                            if "a year" in date:
 #                               date = dt.timedelta(years= -1)
#                                newdate = dt.datetime.strptime(date_string, format).date()
                                newdate = datetime.today() - relativedelta(years= -1)
                            else:
                                if "year" in date:
                                    try: 
                                        tempdate = -int(re.sub( r'[^0-9]','',date_string))
                                        print ('Stuff - > ',tempdate)
 #                                       date = dt.timedelta( years= tempdate)
#                                    newdate = dt.datetime.strptime(date_string).date()
                                        newdate = datetime.today() - relativedelta(years= tempdate)
                                    except Exception as error:
                                        print("    An error getting date occurred:", type(error).c) # An error occurred:
                                else:
                                    format = '%Y-%b-%d' #specifify the format of the date_string.
                                    month = date[:3]
                                    year = date[3:]
                                    day = '01'
                                    date_string = year+'-'+ month+'-'+day
                                    try: 
                                        newdate = dt.datetime.strptime(date_string, format).date()
                                    except Exception as error:
                                        print("    An error getting date occurred:", type(error).c) # An error occurred:
#                                    try:
#                                        newdate = dt.datetime.strptime(date_string, format).date()
#                                    except Exception as error:
#                                        print("    An error getting date occurred:", type(error).c) # An error occurred:
                                    newdate = str(newdate)
    #format = '%b/%Y/%d' #specifify the format of the date_string.
    #newdate2 = dt.datetime.strptime(str(newdate), format).date()
    dateparts = (str(newdate)).split("-")
    dateparts2 = dateparts[2].split(" ")
    #dateparts = dateparts2[0]
#    print ('dateparts',dateparts)
    newdate2 = dateparts[0]+'-'+dateparts[1]+'-'+dateparts2[0]+'T22:00:00'
    #newdate2 = str(re.sub(r'-','/',str(newdate.date())))+'T22:00:00'
    print ('    Got Date: ', newdate2, newdate)
    try:
        post_id = check_post(title,newdate2,headers)
    except  Exception as error :
        print ('Could not check to see post already exists', type(error).c)
    if ( post_id == False):        
        googleadress =  r"<a href=https://www.google.com/maps/dir/?api=1&destination="+addresshtml + r">"+address+r"</a>"
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
            response = requests.post(wpAPOurl, json = post_data, headers=headers2)
            if ( response.status_code != 201 ):
                print ('Error: ',response, response.text)
            else:
                NewPost = True
                post_id_json = response.json()
                post_id = post_id_json.get('id')
                print ('    New post is has post_id = ',post_id)
        except Exception as error:
            print("An error occurred:", type(error).__name__) # An error occurred:
        postneedsupdate = True
    else:
        print ('    Post already existed: Post ID : ',post_id)
    for pic in pidchop:
        picslice2 = pic.split("/")[-1]
        picslice = picslice2.split(".")
        picname = picslice[0] 
        caption =title
        description = title+"\n"+address
        print ('  Found Picture: ',picname)
        file_id, link = check_media(picname, headers)
#        link = linknew['rendered']
        if (file_id) is False:
            print ('    '+picname+' was not already found in library, adding it')
            countreview = True
            image = {
                "file": open(pic, "rb"),
                "post": post_id,
                "caption": caption,
                "description": description
            }
            try:
                image_response = requests.post(wpAPI + "/media", headers=headers, files=image)
            except Exception as error:
                print("    An error uploading picture ' + picname+ ' occurred:", type(error).__name__) # An error occurred:
            if ( image_response.status_code != 201 ):
                print ('    Error- Image ',picname,' was not successfully uploaded.  response: ',image_response)
            else:
                PicDict=image_response.json()
                file_id= PicDict.get('id')
                link = PicDict.get('guid').get("rendered")
                print ('    ',picname,' was successfully uploaded to website with ID: ',file_id, link)
            try:
                linksDict = {'file_id' : file_id , 'link' : link}
                linkslist.append(linksDict)
            except Exception as error:
                print("    An error adding to dictionary " , file_id , link , " occurred:", type(error).__name__) # An error occurred:
        else:
            print ('    Photo ',picname,' was already in library and added to post with ID: ',file_id,' : ',link)
            try:
                image_response = requests.post(wpAPI + "/media/" + str(file_id), headers=headers, data={"post" : post_id})
            except Exception as error:
                print ('    Error- Image ',picname,' was not attached to post.  response: ',image_response)
            try:
                post_response = requests.post(wpAPI + "/posts/" + str(post_id), headers=headers)
                if (link in str(post_response.text)):
                    print ('    Image link for ', picname, 'already in content of post: ',post_id, post_response.text, link)
                else:
                    linkslist.append({'file_id' : file_id , 'link' : link})
                    countreview = True
            except Exception as error:
                print("    An error loading the metadata from the post " + post_response.title + ' occurred:", type(error).__name__) # An error occurred')
    #ratinghtml = post_response.text
    firstMP4 = True
    for piclink in linkslist:
        #for loop in linkslist:
        print ('    Adding ', piclink['link'], ' to posting')
        try:
            ext = (piclink['link'].split( '.')[-1] )
            if (ext == 'mp4'):
                if (firstMP4):
                    contentpics += '\n' +r'[evp_embed_video url="' + piclink['link'] + r'" autoplay="true"]'
                    firstMP4 = False
                else:
                    contentpics += '\n' +r'[evp_embed_video url="' + piclink['link'] + r'"]'           
                #[evp_embed_video url="http://example.com/wp-content/uploads/videos/vid1.mp4" autoplay="true"]
            else:
                contentpics += '\n '+r'<div class="col-xs-4"><img id="'+str(file_id)+r'"' + r'src="' + piclink['link'] + r'"></div>'
#            contentpics += '\n '+r'<img src="'+ piclink['link'] + '> \n'
            #contentpics += r'<img src="'+ piclink['link'] + r' alt="' + title +r'">' +'\n\n'
        except Exception as error:
            print("An error occurred:", type(error).__name__) # An error occurred:
    try:
        response_piclinks = requests.post(wpAPI+"/posts/"+ str(post_id), data={"content" : googleadress+'\n\n'+content+'\n'+rating  + contentpics, "featured_media" : file_id}, headers=headers)
    except Exception as error:
        print("    An error writing images to the post " + post_response.title + ' occurred:", type(error).__name__) # An error occurred')
    return NewPost

##################################################################################################
    
def make_video(inphotos):
# Load the photos from the folder
# Set the duration of each photo to 2 seconds
    if inphotos:
        dir = inphotos[0].rsplit(r'/', 1)
        folder = dir[0]
        output = folder+"/montage.mp4"
        if ((not os.path.exists(output)) and (len(inphotos) >1)):
            video = VideoFileClip(inphotos[0])
            for photo in inphotos :
                #clip = VideoFileClip("myHolidays.mp4").subclip(50,60)
                clip = VideoFileClip(photo)
                # Concatenate the photos into a clip
                if (".jpg" in photo):
                    clip.duration = 2
                try:
                    video = concatenate_videoclips([video, clip], method="compose")
                except Exception as error:
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
    return False, False

##################################################################################################
    

##################################################################################################
    
def post_to_instagram2 (title, content, date, rating, address, picslist, instasession):
    #post_to_instagram2(processrow[1].value, processrow[2].value ,processrow[7].value, processrow[3].value, processrow[8].value, processrow[5].value,outputs['instagram'])
    #montageexists = "montage.mp4" in picslist
    if ((picslist != '[]' ) and ("montage.mp4" in picslist)):
        outputmontage = ''
        addresshtml = re.sub(" ", ".",address)
        #content = content + hastags(address, title)
        pics = ((picslist[1:-1].replace(",","")).replace("'","")).split(" ")
        video, outputmontage = make_video(pics)
        try:
            data =  title + "\n"+ address+"\nGoogle map to destination: " r"https://www.google.com/maps/dir/?api=1&destination="+addresshtml +"\n\n"+ content + "\n"+rating+"\n"+date+"\n\n"+ hastags(address, title)+"\n\nhttps://www.joeeatswhat.com"+"\n\n"
            video2 = instasession.video_upload(outputmontage, data)
        except Exception as error:
            print("  An error occurred uploading video to Instagram:", type(error).__name__) # An error occurred:
            return False
        #media_pk = instasession.media_pk_from_url('https://www.instagram.com/p/CGgDsi7JQdS/')
        #media_path = instasession.video_download(media_pk)
        # joeeatswhat = instasession.user_info_by_username('timberjoe')
        # try: buildout = instagrapi.story.StoryBuilder(outputmontage,'Credits @timberjoe',[StoryMention(user=joeeatswhat)]).video(40)  # seconds
        # except Exception as error:
        #     print("  An error occurred uploading video to Instagram:", type(error).__name__) # An error occurred:
        # try: instasession.video_upload_to_story(buildout.path,"Credits @example",mentions=buildout.mentions,links=[StoryLink(webUri='https://www.joeeatswhat.com')],medias=[StoryMedia(media_pk=outputmontage)])
#         try:   
#             instasession.video_upload_to_story(
#             outputmontage,
#             "Credits @joeeatswhat",
#  #           mentions=[StoryMention(user='timberjoe', x=0.49892962, y=0.703125, width=0.8333333333333334, height=0.125)],
#             links=[StoryLink(webUri='https://www.joeeatswhat.com')],
#   #          hashtags=[StoryHashtag(hashtag=hastags(address,title), x=0.23, y=0.32, width=0.5, height=0.22)],
#             #medias=[StoryMedia(media_pk=media_pk, x=0.5, y=0.5, width=0.6, height=0.8)],
#         )
#             story = instasession.story_photo("path/to/photo.jpg")
#             instasession.video_elements.add_link("https://www.joeeatswhat.com")
#             #story.add_link("https://www.joeeatswhat.com")
#             instasession.video_elements.add_hashtags(hastags)
#             story = instasession.video_upload_to_story(outputmontage)
#             story.upload()
#             #instasession.video_upload_to_story(path:outputmontage,caption:content, mentions:r'@timberjoe',links:'https://www.joeeatswhat.com',hashtags: hastag) ( path: outputmontage, caption: content, mentions:['@timberjoe'], links: ['https://www.joeeatswhat.com'], hashtags: hastags )
#             # temp = dict()
#             # temp = instasession.video_upload_to_story(path=outputmontage,caption=content,mentions=r'@timberjoe',links='https://www.joeeatswhat.com',hashtags=hastags)
#         except Exception as error:
#             print("  An error occurred uploading video to Instagram:", type(error).__name__) # An error occurred:
#             return False
        return True
    else:
        return False 

##################################################################################################
    
def clearlist (list):
    for listelement in list:
        listelement.clear
    return list
 
##################################################################################################
       
def hastags (address, name):
    nameNoSpaces = re.sub( r'[^a-zA-Z]','',name)
    addressdict = address.rsplit(r' ',3)
    zip = addressdict[3]
    state = addressdict[2]
    city =  re.sub( r'[^a-zA-Z]','',addressdict[1])
    defaulttags = "\n\n\n#"+nameNoSpaces+" #foodie #music #food #travel #drinks #instagood #feedme #joeeatswhat @timberjoe"
    citytag = "#"+city
    statetag = "#"+state
    ziptag = "#"+zip
    if statetag == 'FL':  statetag += ' #Florida'
    fulltag = defaulttags+" "+citytag+" "+statetag+" "+ziptag
    # 153 Sugar Belle Dr, Winter Garden, FL 34787
    # inphotos[0].rsplit(r'/', 1)
    return fulltag

##################################################################################################
    
def process_reviews(outputs):
    # Process
    webcount = xtwittercount = instagramcount = yelpcount = threadscount = facebookcount= tiktokcount = 0
    rows = list((outputs['data'].iter_rows(min_row=1, max_row=outputs['data'].max_row)))
    if (google):
        print('Configuration says to update google Reviews prior to processing them')
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        options.add_argument("--ignore-certificate-error")
        options.add_argument("--ignore-ssl-errors")
        if not showchrome: options.add_argument("--headless")  # show browser or not ||| HEAD =>  43.03 ||| No Head => 39 seg
        options.add_argument("--lang=en-US")
        options.add_argument("--disable-blink-features=AutomationControlled") 
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
        driver = webdriver.Chrome(options=options) # Firefox(options=options)  
        # Changing the property of the navigator value for webdriver to undefined 
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
        driver.get(URL)
        time.sleep(5)
    #                    counter = counter()
        scrolling(counter(driver), driver)
        webdata = get_data(driver,outputs)
        write_to_xlsx2(webdata, outputs)
        driver.close()
        # outputs['data'].save(xls)
        print('Done getting google reviews and writing them to xls file !')
    else:
        print ('Configuration says to skip creation of new reviews from google for this run')
    if needreversed:
        rows = reversed(rows)
    print('Processing Reviews')
    for processrow in rows:
        if processrow[1].value != "name":  # Skip header line of xls sheet
            print ("Processing : ",processrow[1].value)
            writtento = (ast.literal_eval(processrow[9].value))
            # Check to see if the website has already been written to according to the xls sheet, if it has not... then process
            if ((writtento["web"]) == 0 or writtento["instagram"]==0 or writtento["facebook"]==0 or writtento["xtwitter"]==0 or writtento["yelp"]==0 or writtento["tiktok"]==0 or writtento["threads"]==0 ) and (is_port_open(wpAPI, 443)) and (web or instagram or yelp or xtwitter or tiktok or facebook or threads or google)and (processrow[2].value != None) :
                if web :
                    if (writtento["web"] == 0) :
                        if (webcount <= postsperrun):
                            try: 
                                #NewWebPost = post_to_wp(processrow[1].value, processrow[2].value, processrow[2].value ,processrow[7].value, processrow[3].value, processrow[8].value, processrow[5].value)
                                NewWebPost = post_to_wp(processrow[1].value, processrow[2].value, outputs['web'] ,processrow[7].value, processrow[3].value, processrow[8].value, processrow[5].value)
                                try:
                                    writtento["web"] = 1
                                    processrow[9].value = str(writtento)
                                except Exception as error:
                                    print("  An error occurred setting value to go into Excel file:", type(error).__name__) # An error occurred:
                                print ('  Success Posting to Wordpress: '+processrow[1].value)# ',processrow[1].value, processrow[2].value, headers,processrow[7].value, processrow[3].value,processrow[8].value, processrow[5].value, temp3["web"] )
                                if NewWebPost == True:
                                    webcount +=1
                                try: 
                                    print('  write to xls for web')
                                    outputs['datawb'].save(xls)
                                except Exception as error:
                                    print("  An error occurred writing Excel file:", type(error).__name__) # An error occurred:
                            except Exception as error: 
                                print ('  Error writing web post : ',processrow[1].value, processrow[2].value,processrow[7].value, processrow[3].value,processrow[8].value, processrow[5].value, writtento["web"] )   
                                #print ('  Error writing web post : ',processrow[1].value, processrow[2].value, outputs['web'],processrow[7].value, processrow[3].value,processrow[8].value, processrow[5].value, writtento["web"] )
                        else:
                            print ('  Exceeded the number of web posts per run, skipping', processrow[1].value)
                    else:
                        print ('  Website: Skipping posting for ',processrow[1].value,' previously written')
                if instagram:
                    if (writtento["instagram"] == 0 ):
                        if (instagramcount <= postsperrun):
                            try: 
                                print('  Starting to generate Instagram post')
                                NewInstagramPost = post_to_instagram2(processrow[1].value, processrow[2].value, processrow[7].value, processrow[3].value, processrow[8].value, processrow[5].value,outputs['instagram'] )
                                try:
                                    print ('  Start generating content to post to Instagram')
                                    writtento["instagram"] = 1
                                    processrow[9].value = str(writtento)
                                except Exception as error:
                                    print("  An error occurred setting value to go into Excel file:", type(error).__name__) # An error occurred:
                                print ('  Success Posting to Instagram: '+processrow[1].value)# ',processrow[1].value, processrow[2].value, headers,processrow[7].value, processrow[3].value,processrow[8].value, processrow[5].value, temp3["web"] )
                                if NewInstagramPost == True:
                                    instagramcount +=1
                                try: 
                                    print('  write to xls for instagram')
                                    outputs['datawb'].save(xls)
                                    print('  write to mariadb for instagram')
                                    # outputs['postssession'].update('dictPostComplete = '+str(writtento)+' where name == '+processrow[1].value)
                                    # outputs['postssession'].commit()
                                except Exception as error:
                                    print("  An error occurred writing Excel file:", type(error).__name__) # An error occurred:
                            except Exception as error: 
                                print ('  Error writing Instagram post : ',processrow[1].value, processrow[2].value, outputs['instagram'],processrow[7].value, processrow[3].value,processrow[8].value, processrow[5].value, writtento["instagram"], type(error).__name__ )
                        else:
                            print ('  Exceeded the number of Instagram posts per run, skipping', processrow[1].value)
                    else:
                        print ('  Instagram: Skipping posting for ',processrow[1].value,' previously written')
                if facebook:
                    if (writtento["facebook"] == 0 ):
                        if (facebookcount <= postsperrun):
                            try: 
                                print('  Starting to generate Facebook post')
                                NewFacebookPost = post_facebook3(processrow[1].value, processrow[2].value, processrow[7].value, processrow[3].value, processrow[8].value, processrow[5].value,outputs['facebook'] )
                                try:
                                    print ('  Start generating content to post to facebook')
                                    writtento["facebook"] = 1
                                    processrow[9].value = str(writtento)
                                except Exception as error:
                                    print("  An error occurred setting value to go into Excel file:", type(error).__name__) # An error occurred:
                                print ('  Success Posting to facebook: '+processrow[1].value)# ',processrow[1].value, processrow[2].value, headers,processrow[7].value, processrow[3].value,processrow[8].value, processrow[5].value, temp3["web"] )
                                if NewFacebookPost == True:
                                    facebookcount +=1
                                try: 
                                    print('  write to xls for facebook')
                                    outputs['datawb'].save(xls)
                                    print('  write to mariadb for facebook')
                                    # outputs['postssession'].update('dictPostComplete = '+str(writtento)+' where name == '+processrow[1].value)
                                    # outputs['postssession'].commit()
                                except Exception as error:
                                    print("  An error occurred writing Excel file:", type(error).__name__) # An error occurred:
                            except Exception as error: 
                                print ('  Error writing facebook post : ',processrow[1].value, processrow[2].value, outputs,processrow[7].value, processrow[3].value,processrow[8].value, processrow[5].value, writtento["facebook"], type(error).__name__ )
                        else:
                            print ('  Exceeded the number of facebook posts per run, skipping', processrow[1].value)
                    else:
                        print ('  Facebook: Skipping posting for ',processrow[1].value,' previously written')
                if False:
                    if (writtento["xtwitter"] == 0 ):
                        if (xtwittercount <= postsperrun):
                            try: 
                                print('  Starting to generate xtwitter post')
                                NewxtwitterPost = post_x(processrow[1].value, processrow[2].value, processrow[7].value, processrow[3].value, processrow[8].value, processrow[5].value,outputs['xtwitter'] )
                                try:
                                    print ('  Start generating content to post to xtwitter')
                                    writtento["facebook"] = 1
                                    processrow[9].value = str(writtento)
                                except Exception as error:
                                    print("  An error occurred setting value to go into Excel file:", type(error).__name__) # An error occurred:
                                print ('  Success Posting to xtwitter: '+processrow[1].value)# ',processrow[1].value, processrow[2].value, headers,processrow[7].value, processrow[3].value,processrow[8].value, processrow[5].value, temp3["web"] )
                                if NewxtwitterPost == True:
                                    xtwittercount +=1
                                try: 
                                    print('  write to xls for xtwitter')
                                    outputs['datawb'].save(xls)
                                    print('  write to mariadb for xtwitter')
                                    # outputs['postssession'].update('dictPostComplete = '+str(writtento)+' where name == '+processrow[1].value)
                                    # outputs['postssession'].commit()
                                except Exception as error:
                                    print("  An error occurred writing Excel file:", type(error).__name__) # An error occurred:
                            except Exception as error: 
                                print ('  Error writing xtwitter post : ',processrow[1].value, processrow[2].value, outputsmo,processrow[7].value, processrow[3].value,processrow[8].value, processrow[5].value, writtento["xtwitter"], type(error).__name__ )
                        else:
                            print ('  Exceeded the number of xtwitter posts per run, skipping', processrow[1].value)
                    else:
                        print ('  Xtwitter: Skipping posting for ',processrow[1].value,' previously written')
    #post_x(title, content, date, rating, address, picslist, instasession)
    # else:
    #     print ('Exceeded the number of posts per run, exiting')
                # if xtwitter:
                #     namedict = {'name':'xtwitter', 'namecount':xtwittercount, 'namepost':'NewxtwitterPost', 'subroutine':post_x}
                #    # junction('xtwitter',xtwittercount,'NewxtwitterPost','post_x', outputs, writtento, processrow)
                #     socials('xtwitter',namedict,outputs,writtento, processrow,post_x)
    return #(outputs['web'])




##################################################################################################

# def junction(name,namedict, outputs, writtento, processrow ):
#     if name == "xtwitter":
#         twitteroptions = {'name':'xtwitter', 'namecount':namedict['namecount'], 'namepost':'NewxtwitterPost', 'subroutine':'post_x'}
#         namedict.update({'xtwitter':twitteroptions}) 
#         stationout = socials(name, namedict, outputs, writtento, processrow)
#     return namedict

#def socials(namedict, outputs, writtento, processrow):
#def socials(name, namecount, namepost, subroutine, outputs, writtento, processrow):
def socials(name, namedict,outputs, writtento, processrow,funct):# namecount, namepost, subroutine, outputs, writtento, processrow):
    #namedict{'name':name, 'namecount':namecount, 'namepost':namepost, 'subroutine':subroutine}
    #namedict{'name':xtwitter, 'namecount':xtwiteercount, 'namepost':NewxtwitterPost, 'subroutine':postx}
    if name:
        if (writtento[name] == 0 ):
            print (namedict['namecount'])
            if (int(namedict['namecount']) <= postsperrun):
                try: 
                    print('  Starting to generate xtwitter post : ',namedict['subroutine'])
                    postoutput = funct(processrow[1].value, processrow[2].value, processrow[7].value, processrow[3].value, processrow[8].value, processrow[4].value,outputs )
                    try:
                        print ('  Start generating content to post to xtwitter : ') #,namedict['subroutine'])
                        writtento[name] = 1
                        processrow[9].value = str(writtento)
                    except Exception as error:
                        print("  An error occurred setting value to go into Excel file:", type(error).__name__) # An error occurred:
                    print ('  Success Posting to '+name+': '+processrow[1].value)# ',processrow[1].value, processrow[2].value, headers,processrow[7].value, processrow[3].value,processrow[8].value, processrow[5].value, temp3["web"] )
                    if namedict['namepost'].value == True:
                        namecount +=1
                    try: 
                        print('  write to xls for '+name)
                        outputs['datawb'].save(xls)
                        print('  write to mariadb for '+name)
                        # outputs['postssession'].update('dictPostComplete = '+str(writtento)+' where name == '+processrow[1].value)
                        # outputs['postssession'].commit()
                    except Exception as error:
                        print("  An error occurred writing Excel file:", type(error).__name__) # An error occurred:
                except Exception as error: 
                    print ('  Error writing '+name+' post : ',processrow[1].value, processrow[2].value, outputs[name],processrow[7].value, processrow[3].value,processrow[8].value, processrow[5].value, writtento[name], type(error).__name__ )
            else:
                print ('  Exceeded the number of '+name+' posts per run, skipping', processrow[1].value)
        else:
            print ('  '+name+': Skipping posting for ',processrow[1].value,' previously written')
    return namedict

##################################################################################################
    
if __name__ == "__main__":
    print('starting ...')
    driver = preload()
    print('making connections ...')
    outputs = authconnect()
    process_reviews(outputs)  
    print('Done!')

##################################################################################################
    