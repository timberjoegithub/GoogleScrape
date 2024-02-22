import ast
import base64
import pandas as pd
import requests
from openpyxl import Workbook, load_workbook
from env import wpAPOurl, xls,user, password,wpAPOurl
import datetime as dt

def connect_and_auth_wp(headers):
    # connect and  auth
    data_string = f"{user}:{password}"
    token = base64.b64encode(data_string.encode()).decode("utf-8")
    headers = {"Authorization": f"Basic {token}"}
    return (headers)

def post_to_wp(title, content, headers,date, rating,address, hash):
    # post
    #wpAPOurl = "https://www.joeeatswhat.com/wp-json/wp/v2/posts"
    #newdate = pd.to_datetime(df['date']).dt.strftime('%d-%m-%Y')
    #df = pd.DataFrame({})
        # newdate = pd.to_datetime(
        #     dict(
            # year=df[date].str[2:], 
            # month=df[date].str[:2], 
            # day=1
    format = '%b/%Y/%d' #specifify the format of the date_string.
    month = date[:3]
    year = date[3:]
    day = '01'
    date_string = month+'/'+year+'/'+day
    try: 
        newdate = dt.datetime.strptime(date_string, format).date()
        print ('Got it')
    except Exception as error:
        print("An error occurred:", type(error).__name__) # An error occurred:
    post_data = {
        "title": title,
        "content": address+'\n\n'+content+'\n'+rating ,
        "status": "draft",  # Set to 'draft' if you want to save as a draft
        "date": newdate,
        "author":"jsteele" 
    }
    try: 
#        response = requests.post(wpAPOurl, json=post_data, headers=headers)
        myobj = {'json': post_data, 'headers':headers}
        response = requests.post(wpAPOurl, json = myobj)
    except Exception as error:
        print("An error occurred:", type(error).__name__) # An error occurred:
    return (response, headers)

def add_image(imageinfo, postinfo):
    # loop thru
    image = {
        "file": open("your_image.jpg", "rb"),
        "caption": "Image caption",
        "description": "Image description"
    }
    image_response = requests.post(wpAPOurl + "/media", headers=headers, files=image)

def read_from_xlsx(ws):
    print('read from excel...')
    return (ws)

def process_reviews(ws, headers):
    # Process
    for processrow in ws.rows:
#        If reviewxls (comment has content) and (picsURL has connect)
        if processrow[1].value != "name":
            print (processrow[1].value)
           # ast.literal_eval(deployments) = processrow[9].value
            temp3 = (ast.literal_eval(processrow[9].value))
            if ((temp3["web"]) == 0):
                try: 
                    post_to_wp(processrow[1].value, processrow[2].value, headers ,processrow[7].value, processrow[3].value, processrow[8].value, processrow[5].value)
                    temp3['web'] = 1
                except: 
                    print ('Error writing: ',processrow[1].value, processrow[2].value, headers,processrow[7].value, processrow[3].value,processrow[8].value, processrow[5].value, temp3["web"] )


if __name__ == "__main__":
    headers = dict
    wb = load_workbook(filename = xls)
    ws = wb['Sheet1']
    print('starting...')
   # read_from_xlsx(ws)
    print('Connect and auth to Wordpress')
    connect_and_auth_wp(headers)
    print('Processing Reviews')
    process_reviews(ws, headers)  
    print('Done!')