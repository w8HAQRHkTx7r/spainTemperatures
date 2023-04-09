import time
import board
from adafruit_pyportal import PyPortal
from secrets import secrets

from adafruit_display_text.label import Label
from adafruit_display_shapes.circle import Circle
import terminalio
import displayio
from adafruit_bitmap_font import bitmap_font

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep","Oct","Nov","Dec"]
DOW_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# Function to convert Unix time to month, day, and day of week
def unix_to_date(unix_time):
    # Convert Unix time to a Python time struct
    time_struct = time.localtime(unix_time)
    # Extract month, day, and day of week from time struct
    month = MONTH_NAMES[time_struct.tm_mon-1]
    day = time_struct.tm_mday
    day_of_week = DOW_NAMES[time_struct.tm_wday]
    hour = time_struct.tm_hour
    minute = time_struct.tm_min

    # Return a string containing month, day, DOW, hh:mm
    return f"{day_of_week} {month} {day} {hour}:{minute:02d}"

def oneDecimal(parm):
    return f"{parm:4.1f}"

def query():
    CURRENT_SPAIN_CONDITIONS = []
    for c in cities:
        lat = c['lat']
        lon = c['lon']
        URL = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={EXCLUDES}&units={UNITS}&appid=" + secrets['weather']
        status_label.text = f"Getting {c['city']}"
        try:
            value = pyportal.fetch(URL)
            CURRENT_SPAIN_CONDITIONS.append(value)
            time.sleep(2)
        except RuntimeError as e:
            print("Some error occured, retrying! -", e)
    status_label.text = " "
    return CURRENT_SPAIN_CONDITIONS

cities = [
          {"city" : "Lisboa",     "lat" : 38.71,     "lon" : -9.14,     "x" : 40,  "y" : 149},
          {"city" : "Evora",      "lat" : 38.57,     "lon" : -7.91,     "x" : 66,  "y" : 153},
          {"city" : "Carmona",    "lat" : 37.450915, "lon" : -5.648573, "x" : 103, "y" : 187},
          {"city" : "Ronda",      "lat" : 36.743917, "lon" : -5.162285, "x" : 120, "y" : 203},
          {"city" : "Ubeda",      "lat" : 38.014979, "lon" : -3.371276, "x" : 159, "y" : 171},
          {"city" : "Madrid",     "lat" : 40.410688, "lon" : -3.718344, "x" : 153, "y" : 104},
          {"city" : "Barcelona",  "lat" : 41.402369, "lon" :  2.171505, "x" : 270, "y" : 77},
         ]

UNITS    = "imperial"
EXCLUDES = "minutely,hourly" #,alerts"

lat = cities[0]['lat']
lon = cities[0]['lon']

TIMESTAMP_PATH = ['current', 'dt']
TEMPERATURE_PATH = ['current', 'temp']
CONDITIONS_PATH = ['current', 'weather', 0, 'description']

DAY0_MAX_PATH = ['daily',0, 'temp', 'max']
DAY0_MIN_PATH = ['daily',0, 'temp', 'min']

cwd = ("/"+__file__).rsplit('/', 1)[0]

ROW_SPACING = 18
COL_SPACING = 50
MAX_ROW = 50
MIN_ROW = 70

pyportal = PyPortal(#url=URL,
                    json_path=(TIMESTAMP_PATH, TEMPERATURE_PATH, CONDITIONS_PATH,
                        DAY0_MAX_PATH, DAY0_MIN_PATH),
                    status_neopixel=board.NEOPIXEL,
                    default_bg=cwd+"/iberian_peninsula.bmp"
                    )

pyportal.preload_font()

CITYLABELCOLOR = 0xffff00
CIRCLEFILL = 0xff0000
CIRCLEOUTLINE = 0x000000
BACKGROUPCIRCLEFILL = 0x000000

city_labels = []
CIRCLES_GROUP = displayio.Group()
LABELS_GROUP = displayio.Group()

next_city = 0
# Create labels for each city
for idx,c in enumerate(cities):
    generic_label = Label(terminalio.FONT, text=c['city'][:1], color=CITYLABELCOLOR)
    lat = c['x']
    lon = c['y']
    generic_label.x = lat
    generic_label.y = lon
    LABELS_GROUP.append(generic_label)

# Create label for status of queries
status_label = Label(terminalio.FONT, text = "Getting Barcelona", color=CITYLABELCOLOR)
status_label.x = 10
status_label.y = 50
LABELS_GROUP.append(status_label)

# Create circles
def draw_circles(special_city):
    while len(CIRCLES_GROUP) > 0:
        CIRCLES_GROUP.pop()
    for idx,c in enumerate(cities):
        lat = c['x']
        lon = c['y']
        if idx == special_city:
            background_circle = Circle(lat, lon, 8, fill=CIRCLEFILL, outline=CIRCLEOUTLINE)
            CIRCLES_GROUP.append(background_circle)
        else:
            highlighted_circle = Circle(lat, lon, 8, fill=BACKGROUPCIRCLEFILL, outline=CIRCLEOUTLINE)
            CIRCLES_GROUP.append(highlighted_circle)

draw_circles(0)
pyportal.splash.append(CIRCLES_GROUP)
pyportal.splash.append(LABELS_GROUP)

CURRENT_SPAIN_CONDITIONS = []
CURRENT_SPAIN_CONDITIONS = query()

# Font for temperature data
font_name = "Arial-Bold-12.bdf"
font = bitmap_font.load_font("fonts/"+font_name)
font.load_glyphs(b'abcdefghjiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ- ()0123456789.:')

# Create labels for the temperatures
lblTime =  Label(font, text = "*"*16, color=0xffffff)
lblTime.x = 10
lblTime.y = 30
lblConditions = Label(font, text = "*"*20, color=0xffffff)
lblConditions.x = 140
lblConditions.y = 30
lblMin = Label(font, text = "*"*4, color=0xffffff)
lblMin.x = 10
lblMin.y = 60
lblMin.background_color = 0x0000ff
lblNow = Label(font, text = "*"*4, color=0xffffff)
lblNow.x = 90
lblNow.y = 60
lblMax = Label(font, text = "*"*4, color=0xffffff)
lblMax.x = 170
lblMax.y = 60
lblMax.background_color = 0xff0000

# Put the labels in a group
DATA_GROUP = displayio.Group()
DATA_GROUP.append(lblTime)
DATA_GROUP.append(lblConditions)
DATA_GROUP.append(lblMin)
DATA_GROUP.append(lblNow)
DATA_GROUP.append(lblMax)

# Put the group into the main group (splash)
pyportal.splash.append(DATA_GROUP)

# Display the data and loop
timeout = 3600
while True:
    currenttime = time.monotonic()
    limit = currenttime + timeout
    while currenttime < limit:
        for idx, conditions in enumerate(CURRENT_SPAIN_CONDITIONS):
            draw_circles(idx)
            lblTime.text = unix_to_date(conditions[0])
            lblConditions.text = conditions[2]
            lblMin.text = oneDecimal(conditions[4])
            lblMax.text = oneDecimal(conditions[3])
            lblNow.text = oneDecimal(conditions[1])
            time.sleep(4)
        currenttime = time.monotonic()
    print("Time to freshen the data")
    CURRENT_SPAIN_CONDITIONS = query()
