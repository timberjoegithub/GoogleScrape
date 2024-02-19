URL = "https://www.google.com/maps/contrib/109274792898041753066/reviews/"

import platform
if platform.system() eq 'Linux'
    DriverLocation = "./Driver/chromedriver"
else:
    DriverLocation = "./Driver/chromedriver.exe"