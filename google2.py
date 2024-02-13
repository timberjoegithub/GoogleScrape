
# Import the beautifulsoup  
# and request libraries of python. 
import requests 
import bs4 
  
# Make two strings with default google search URL 
# 'https://google.com/search?q=' and 
# our customized search keyword. 
# Concatenate them 
text= "joe"
url = "https://www.google.com/maps/contrib/109274792898041753066/reviews"
  
# Fetch the URL data using requests.get(url), 
# store it in a variable, request_result. 
request_result=requests.get( url ) 
  
# Creating soup from the fetched request 
soup = bs4.BeautifulSoup(request_result.text, 
                         "html.parser") 
#print(soup) 
heading_object=soup #.find_all( 'h1' ) 
  
# Iterate through the object  
# and print it as a string. 
for info in heading_object: 
    print(info.getText()) 
    print("------") 