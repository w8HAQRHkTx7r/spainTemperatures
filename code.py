# Purpose: Read city temps from OpenWeather API and display 4 day forecast.
import time
import board
from adafruit_pyportal import PyPortal
from secrets import secrets

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep","Oct","Nov","Dec"]
DOW_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# Function to convert Unix time to month, day, and day of week
def unix_to_date(unix_time):
    # Convert Unix time to a Python time struct
    time_struct = time.localtime(unix_time)
    print(time_struct)
    # Extract month, day, and day of week from time struct
    month = MONTH_NAMES[time_struct.tm_mon-1]
    day = time_struct.tm_mday
    day_of_week = DOW_NAMES[time_struct.tm_wday]

    # Return a tuple containing month, day, and day of week
    return f"{day_of_week} {month} {day}"

def null(parm):
    return parm

def twoDec(parm):
    return f"{parm:5.2f}"

cities = [
          {"city" : "Lisboa",     "lat" : 38.71,     "lon" : -9.14     },
          {"city" : "Evora",      "lat" : 38.57,     "lon" : -7.91     },
          {"city" : "Carmona",    "lat" : 37.450915, "lon" : -5.648573 },
          {"city" : "Ronda",      "lat" : 36.743917, "lon" : -5.162285 },
          {"city" : "Ubeda",      "lat" : 38.014979, "lon" : -3.371276 },
          {"city" : "Marid",      "lat" : 40.410688, "lon" : -3.718344 },
          {"city" : "Barcelona",  "lat" : 41.402369, "lon" :  2.171505 },
         ]

UNITS    = "imperial"
EXCLUDES = "minutely,hourly" #,alerts"

for c in cities:
    print(c)
    lat = c['lat']
    lon = c['lon']
print(lat,lon)

URL = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={EXCLUDES}&units={UNITS}&appid=" + secrets['weather']

TIMESTAMP_PATH = ['current', 'dt']
TEMPERATURE_PATH = ['current', 'temp']
CONDITIONS_PATH = ['current', 'weather', 0, 'description']

DAY0_MAX_PATH = ['daily',0, 'temp', 'max']
DAY0_MIN_PATH = ['daily',0, 'temp', 'min']
DAY1_MAX_PATH = ['daily',1, 'temp', 'max']
DAY1_MIN_PATH = ['daily',1, 'temp', 'min']
DAY2_MAX_PATH = ['daily',2, 'temp', 'max']
DAY2_MIN_PATH = ['daily',2, 'temp', 'min']
DAY3_MAX_PATH = ['daily',3, 'temp', 'max']
DAY3_MIN_PATH = ['daily',3, 'temp', 'min']
DAY4_MAX_PATH = ['daily',4, 'temp', 'max']
DAY4_MIN_PATH = ['daily',4, 'temp', 'min']

cwd = ("/"+__file__).rsplit('/', 1)[0]

ROW_SPACING = 18
COL_SPACING = 50
MAX_ROW = 50
MIN_ROW = 70

pyportal = PyPortal(url=URL,
                    json_path=(TIMESTAMP_PATH, TEMPERATURE_PATH, CONDITIONS_PATH,
                        DAY0_MAX_PATH, DAY0_MIN_PATH,
                        DAY1_MAX_PATH, DAY1_MIN_PATH,
                        DAY2_MAX_PATH, DAY2_MIN_PATH,
                        DAY3_MAX_PATH, DAY3_MIN_PATH,),
                    text_font = cwd+"/fonts/Arial-Bold-12.bdf",
                    text_position=[(COL_SPACING,30), (COL_SPACING + 90, 30), (COL_SPACING + 150, 30),
                        (COL_SPACING, MAX_ROW), (COL_SPACING,MIN_ROW),
                        (COL_SPACING*2, MAX_ROW), (COL_SPACING*2, MIN_ROW),
                        (COL_SPACING*3, MAX_ROW), (COL_SPACING*3, MIN_ROW),
                        (COL_SPACING*4, MAX_ROW), (COL_SPACING*4, MIN_ROW),],
                    text_color=(0xffffff, 0xffffff, 0xffffff,
                        0xffff00, 0xffff00,
                        0xffff00, 0xffff00,
                        0xffff00, 0xffff00,
                        0xffff00, 0xffff00,),
                    status_neopixel=board.NEOPIXEL,
                    text_transform=(unix_to_date, twoDec, null,
                        twoDec, twoDec,
                        twoDec, twoDec,
                        twoDec, twoDec,
                        twoDec, twoDec,),
                    default_bg=cwd+"/iberian_peninsula.bmp"
                    )

pyportal.preload_font()

while True:
    try:
        value = pyportal.fetch()
    except RuntimeError as e:
        print("Some error occured, retrying! -", e)
    print(value)
    time.sleep(28800)
