''' PREFERENCES DEFAULT SETTINGS 

This module contains the default paths, settings to make some cosmetic changes easier.

TODO: Include additional aesthetic settings within the preference file.

'''
versionnum = "2.01"
verdate = "20200803"

# Files
foodfile = "db\mfoodv3.csv" # Food database - contains restaurant, item, calorie name, and image path of food item
startimgpath = "images\main.jpg" # Main screen image
searchimgpath = "images\search.jpg" # Magnifier icon
imagepath = "images\\" # Where default location for all images for the program sit
exfile = 'db\exercise.csv' # Exercise database - contains exercise full name, multiplier value, and short name

# Default Values
did = ""
dLoginId = ""
dEmail = ""
dPassword = ""
dFirstName = "User"
dLastName = ""
dPref1 = "NA"
dPref2 = "NA"
dPref3 = "NA"
dWeight = 150
dUnits = "LB"
dRestaurant = ""
dFood = ""
dCalories = ""
dMinEquiv1 = ""
dMinEquiv2 = ""
dMinEquiv3 = ""

memeTotal = 1

# Tolerances
MinWeight = 50
MaxWeight = 500

# Meme Card Settings
MemeHt = 500 # Height dimension of the Meme Card - DO NOT EXCEED WINDOW SIZE
MemeWt = 500 # Width dimension of the Meme Card
ImagepadX = 10 # Distance between text and side
TextpadY = 10 # Distance between text and top and bottom edges
MemeLinespacing = 1.1 # Distance between main body text
MemeTextFont = 'fonts/impact.ttf'
MemeTextShadowOn = "thick" # OPTIONS: thin, thick, thicker, NA
MemeTextFontColor = "red" # Body Text Fill Color
MemeTextShadowColor = "black" # Body Text Outline/Shadow Color
MemeDiscFont = 'fonts\Roboto-Medium.ttf' # Bottom Disclosure Text Font
MemeDiscFontSize = 12
MemeDiscFontColor = (150,150,150) # Bottom Disclosure Text color
defaultFdImg = "images\default_item.png" # Placeholder for item if no item picture is available
defaultBG = "images\WhiteBG.png"

# App Settings
#Fonts
headfont = ('arial', 12, 'bold')
subheadfont = ('arial', 10, 'bold')
buttonfont = ('arial', 14, 'bold')

parafont = ('times', 10) # Main Text Font

#Colors
statuscolor = 'goldenrod' # statusbar
headlabelbg = 'RoyalBlue2'
headlabeltxt = 'white'
#Buttons
exprefNextImg = "images\\Next.png" # Button image
buttcolor = 'dark green' # Try "chartreuse2", "green2", "green yellow"
butttextcolor = 'white'
fdnext_Button_Color = 'gray33'
fdnext_ButtonText_Color = 'gray75'
#Window Size
appwidth=800
appheight=600
appresolution = str(appwidth) + 'x' + str(appheight)

