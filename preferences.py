#-------------------------------------------------------------------------------
# Name:      preferences.py
# Purpose:   Program preferences/settings
# Author(s): Vincent Lin
# Created:   06/10/2020
# TODO:      Cleanup and remove test data. Add additional styles to control fonts, windows, etc. 
# Note:      
#-------------------------------------------------------------------------------

# Files
accountfile = "db\maccount.csv"
foodfile = "db\mfoodv3.csv"
startimgpath = "images\main.jpg"
searchimgpath = "images\search.jpg"
imagepath = "images\\"
exfile = 'db\exercise.csv'

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
dWeight = ""
dUnits = "LB"
dRestaurant = ""
dFood = ""
dCalories = ""
dMinEquiv1 = ""
dMinEquiv2 = ""
dMinEquiv3 = ""

memeCount = 1
memeTotal = 1

# Meme Card Settings
MemeHt = 500
MemeWt = 500
ImagepadX = 10
TextpadY = 10
MemeLinespacing = 1.1
MemeTextShadowOn = "NA"
MemeTextFillColor = "red"
MemeTextShadowColor = "black"
defaultFdImg = "images\\t-mcdonalds-Big-Mac.jpg"
defaultBG = "images\WhiteBG.png"

# App Settings
#Fonts
headfont = ('arial', 12, 'bold')
subheadfont = ('arial', 10, 'bold')
parafont = ('times', 10)
#Buttons
buttcolor = 'white'
#Window Size
appwidth=800
appheight=600
appresolution = str(appwidth)+'x'+str(appheight)

