URL = "https://www.google.com/maps/contrib/109274792898041753066/reviews/"
wpAPOurl = "https://www.joeeatswhat.com/wp-json/wp/v2/posts"
xls="./Output/reviews.xlsx"
user='pythonwpadmin'
password='5SQL x0K6 tBuP ThwR Qg6q KsMB'
import platform
if platform.system() is 'Linux':
    DriverLocation = "./Driver/chromedriver"
else:
    DriverLocation = "./Driver/chromedriver.exe"