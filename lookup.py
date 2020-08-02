#-------------------------------------------------------------------------------
# Name:      lookup.py
# Purpose:   Primary program flow for LIFE webapp
# Author(s): Vincent Lin
# Created:   06/10/2020
# TODO:      Fold the primary equivalency calculation back into this module.
# Note:      This module handles the time string conversion and the 
#            Meme Card creation.  
#-------------------------------------------------------------------------------

# importing module  
from preferences import * 
import PIL # used for get_meme_images to render image
from PIL import ImageTk, Image, ImageDraw, ImageFont # used for get_meme_images to render image
import os.path # used with pathlib to check to see if file exists in get meme
from os import path
import csv # used throughout to import data files for exercise, food

def convert_time_string(minutes):
    '''Time String Converter

    Function converts integer (assumed minutes) into a string (a phrase)

    Example: 
    Input integer '87' will convert to '1 hour and 27 minutes'
    Input integer '120' will convert to '2 hours'
    Input integer '34' will convert to '34 minutes' 

    Args:
    minutes: integer representing the total number of minute equivalents needed of a specific exercise

    Returns:
    time_s: string - a phrase that will be used in the Meme Card text.

    '''
    time_s = ""
    hours = minutes / 60
    rhours = minutes // 60
    mhours = minutes % 60
    days = hours / 24
    rdays = hours // 24
    mdays = hours % 24

    if days > 2:
        if mdays == 0:
            time_s = (str(int(rdays)) + " days of ")
        elif mhours == 0:
            time_s = (str(int(rdays)) + " days " + str(int(rhours))+" hours of")        
        else:
            time_s = (str(int(rdays)) + " days " + str(int(mdays))+" hours " + str(int(mhours)) + " minutes of")
    elif hours > 2:
        if mhours == 0:
            time_s = (str(int(rhours)) + " hours of")
        else:
            time_s = (str(int(rhours)) + " hours and "+str(int(minutes%60))+" minutes of")
    else:
        time_s = (str(int(minutes))+" minutes of")
    return time_s

def get_meme_image(food_dict, food, exercise, minutes, minutestring, meme_count):
    '''MemeCard Renderer

    This function renders the memecard and saves it.

    Args:
    food_dict: food table w/ restaurant, item, calories, and image - used to lookup image
    food: food item being passed for the meme
    exercise: the exercise selected being passed for the meme
    minutes: integer - number of actual minutes so that the meme text can be adjusted based on this value
    minutestring: minutes converted to a readable string, e.g. 220 = "3 hours 40 minutes"
    mem_count: keeps track of which meme we're on
    
    Returns: 
    MemeCard: Photo Image that is rendered in the app frame.

    '''

    global defaultFdImg # Make sure the default image is picked up from Preferences
    global MemeTextFont
    global MemeTextFontColor
    global MemeDiscFontColor
    global MemeDiscFont
    global MemeDiscFontSize
    
    # Font settings for easy manipulation of format 
    Line1Font = ImageFont.truetype(MemeTextFont, 40) # Headline "The something something"
    Line2Font = ImageFont.truetype(MemeTextFont, 38) # "Equivalent of"
    Line3Font = ImageFont.truetype(MemeTextFont, 40) # "so and so minutes"
    Line4Font = ImageFont.truetype(MemeTextFont, 40) # "sport/activity"
    Line5Font = ImageFont.truetype(MemeDiscFont, MemeDiscFontSize) # Disclaimer / Name of Meme Program

    Fdfilepath = imagepath + food_dict[food.Restaurant][food.Food][1] # Lookup the food image path from the food dictionary
    
    # Check to see if image file exists at location
    if path.exists(Fdfilepath): # if image exists do nothing
        Fdfilepath = Fdfilepath
    else: # if image doesn't exist use the default generic image
        Fdfilepath = defaultFdImg
    FdimageA = Image.open(Fdfilepath).convert('RGBA')
    background = Image.new('RGBA', FdimageA.size, (255,255,255))
    Fdimage = Image.alpha_composite(background, FdimageA)
    #Fdimage = Image.open(Fdfilepath)
    #Fdimage.convert('RGBA')
    Bgimage = Image.open(defaultBG)

    # Calculate the desired size of the Food image by removing the horizontal padding
    Fdwidth = MemeWt - (ImagepadX * 2)
    # Get the width and height of the Food image
    FdimageW, FdimageH = Fdimage.size
    # Calculate the % adjustment to get to the desired width
    wpercent = (Fdwidth / float(FdimageW))
    # Calculate the height adjustment based on the same conversion for width
    hsize = int((float(Fdimage.size[1]) * float(wpercent)))
    # Resize the entire food image
    Fdimage = Fdimage.resize((Fdwidth, hsize), PIL.Image.ANTIALIAS)
    # Center the image by calculating the difference between the height of the meme card and the food image then dividing by 2
    vpos = int((MemeHt - hsize) / 2)
    # Paste in food item
    Bgimage.paste(Fdimage,(ImagepadX,vpos))
    imageBd = ImageDraw.Draw(Bgimage)

    global discfont
    global MemeDiscFillColor

    # LINE 1
    # Can generate some random phrases based on how many minutes are involved "The eye-popping reality" "The horror sicks in:"
    if minutes > 119:
        Mstr1="The nauseating realization"
    elif minutes > 59:
        Mstr1="The horrible discovery"
    elif minutes > 44:
        Mstr1="The weary resignation"
    elif minutes > 29:
        Mstr1="The acceptance"
    elif minutes > 14:
        Mstr1="The ready mental trade-off"
    elif minutes > 4:
        Mstr1="The smug knowledge"
    else:
        Mstr1 = "The joy in knowing"
    Mstr1 = Mstr1.upper() # Make all upper case

    # Get the width and height of the specific string
    M1Wt,M1Ht=Line1Font.getsize(Mstr1)
    #Generate shadow https://stackoverflow.com/questions/18974194/text-shadow-with-python
    if MemeTextShadowOn == "thin":
        thickness = 1
        imageBd.text((((MemeWt - M1Wt)/2)-thickness,TextpadY), Mstr1, font=Line1Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M1Wt)/2)+thickness,TextpadY), Mstr1, font=Line1Font, fill =MemeTextShadowColor)
        imageBd.text(((MemeWt - M1Wt)/2,TextpadY-thickness), Mstr1, font=Line1Font, fill =MemeTextShadowColor)
        imageBd.text(((MemeWt - M1Wt)/2,TextpadY+thickness), Mstr1, font=Line1Font, fill =MemeTextShadowColor)
    elif MemeTextShadowOn == "thick":
        thickness = 2
        imageBd.text((((MemeWt - M1Wt)/2)-thickness,TextpadY-thickness), Mstr1, font=Line1Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M1Wt)/2)+thickness,TextpadY-thickness), Mstr1, font=Line1Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M1Wt)/2)-thickness,TextpadY-thickness), Mstr1, font=Line1Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M1Wt)/2)+thickness,TextpadY+thickness), Mstr1, font=Line1Font, fill =MemeTextShadowColor)
    elif MemeTextShadowOn == "thicker":
        thickness = 3
        imageBd.text((((MemeWt - M1Wt)/2)-thickness,TextpadY-thickness), Mstr1, font=Line1Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M1Wt)/2)+thickness,TextpadY-thickness), Mstr1, font=Line1Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M1Wt)/2)-thickness,TextpadY-thickness), Mstr1, font=Line1Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M1Wt)/2)+thickness,TextpadY+thickness), Mstr1, font=Line1Font, fill =MemeTextShadowColor)
    #Lay down the text
    imageBd.text(((MemeWt - M1Wt)/2,TextpadY), Mstr1, font=Line1Font, fill =MemeTextFontColor)

    # LINE 2
    # Can generate some random versions of this line
    Mstr2="that this is the equivalent of"
    Mstr2 = Mstr2.upper() # Make all upper case

    # Get the width and height of the specific string
    M2Wt,M2Ht=Line2Font.getsize(Mstr2)
    #Generate shadow
    if MemeTextShadowOn == "thin":
        thickness = 1
        imageBd.text((((MemeWt - M2Wt)/2)-thickness,(TextpadY + int(M1Ht * MemeLinespacing))), 
                        Mstr2, 
                        #font=Line2Font, 
                        fill=MemeTextShadowColor)
        imageBd.text((((MemeWt - M2Wt)/2)+thickness,(TextpadY + int(M1Ht * MemeLinespacing))), Mstr2, font=Line2Font, fill=MemeTextShadowColor)
        imageBd.text(((MemeWt - M2Wt)/2,(TextpadY + int(M1Ht * MemeLinespacing))-thickness), Mstr2, font=Line2Font, fill=MemeTextShadowColor)
        imageBd.text(((MemeWt - M2Wt)/2,(TextpadY + int(M1Ht * MemeLinespacing))+thickness), Mstr2, font=Line2Font, fill=MemeTextShadowColor)
    elif MemeTextShadowOn == "thick":
        thickness = 2
        imageBd.text((((MemeWt - M2Wt)/2)-thickness,(TextpadY + int(M1Ht * MemeLinespacing)-thickness)), Mstr2, font=Line2Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M2Wt)/2)+thickness,(TextpadY + int(M1Ht * MemeLinespacing)-thickness)), Mstr2, font=Line2Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M2Wt)/2)-thickness,(TextpadY + int(M1Ht * MemeLinespacing)-thickness)), Mstr2, font=Line2Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M2Wt)/2)+thickness,(TextpadY + int(M1Ht * MemeLinespacing)+thickness)), Mstr2, font=Line2Font, fill =MemeTextShadowColor)
    elif MemeTextShadowOn == "thicker":
        thickness = 3
        imageBd.text((((MemeWt - M2Wt)/2)-thickness,(TextpadY + int(M1Ht * MemeLinespacing)-thickness)), Mstr2, font=Line2Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M2Wt)/2)+thickness,(TextpadY + int(M1Ht * MemeLinespacing)-thickness)), Mstr2, font=Line2Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M2Wt)/2)-thickness,(TextpadY + int(M1Ht * MemeLinespacing)-thickness)), Mstr2, font=Line2Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M2Wt)/2)+thickness,(TextpadY + int(M1Ht * MemeLinespacing)+thickness)), Mstr2, font=Line2Font, fill =MemeTextShadowColor)
    #Lay down the text
    imageBd.text(((MemeWt - M2Wt)/2,(TextpadY + int(M1Ht * MemeLinespacing))), Mstr2, font=Line2Font, fill =MemeTextFontColor)

    # LINE 3
    Mstr3=minutestring
    M3Wt,M3Ht=Line3Font.getsize(Mstr3)     # Get the width and height of the specific string
    #Generate shadow
    if MemeTextShadowOn == "thin":
        thickness = 1
        imageBd.text(((MemeWt - M3Wt)/2)-thickness,((int(MemeHt * 0.75))), Mstr3, font=Line3Font, fill =MemeTextShadowColor)
        imageBd.text(((MemeWt - M3Wt)/2)+thickness,((int(MemeHt * 0.75))), Mstr3, font=Line3Font, fill =MemeTextShadowColor)
        imageBd.text(((MemeWt - M3Wt)/2,((int(MemeHt * 0.75)-thickness))), Mstr3, font=Line3Font, fill =MemeTextShadowColor)
        imageBd.text(((MemeWt - M3Wt)/2,((int(MemeHt * 0.75)+thickness))), Mstr3, font=Line3Font, fill =MemeTextShadowColor)
    elif MemeTextShadowOn == "thick":
        thickness = 2
        imageBd.text((((MemeWt - M3Wt)/2)-thickness,((int(MemeHt * 0.75)-thickness))), Mstr3, font=Line3Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M3Wt)/2)+thickness,((int(MemeHt * 0.75)-thickness))), Mstr3, font=Line3Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M3Wt)/2)-thickness,((int(MemeHt * 0.75)-thickness))), Mstr3, font=Line3Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M3Wt)/2)+thickness,((int(MemeHt * 0.75)+thickness))), Mstr3, font=Line3Font, fill =MemeTextShadowColor)
    elif MemeTextShadowOn == "thicker":
        thickness = 3
        imageBd.text((((MemeWt - M3Wt)/2)-thickness,((int(MemeHt * 0.75)-thickness))), Mstr3, font=Line3Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M3Wt)/2)+thickness,((int(MemeHt * 0.75)-thickness))), Mstr3, font=Line3Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M3Wt)/2)-thickness,((int(MemeHt * 0.75)-thickness))), Mstr3, font=Line3Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M3Wt)/2)+thickness,((int(MemeHt * 0.75)+thickness))), Mstr3, font=Line3Font, fill =MemeTextShadowColor)
    
    imageBd.text(((MemeWt - M3Wt)/2,(int(MemeHt * 0.75))), Mstr3, font=Line3Font, fill =MemeTextFontColor)

    # LINE 4
    Mstr4=exercise
    Mstr4 = Mstr4.upper() # Make all upper case

    M4Wt,M4Ht=Line4Font.getsize(Mstr4)
    #imageBd.text((0, 0), Mstr1, font=Line4Font, fill =(255, 0, 0))

    if MemeTextShadowOn == "thin":
        thickness = 1
        imageBd.text(((MemeWt - M4Wt)/2)-thickness,((int(MemeHt * 0.75)+(M1Ht * MemeLinespacing))), Mstr4, font=Line4Font, fill =MemeTextShadowColor)
        imageBd.text(((MemeWt - M4Wt)/2)+thickness,((int(MemeHt * 0.75)+(M1Ht * MemeLinespacing))), Mstr4, font=Line4Font, fill =MemeTextShadowColor)
        imageBd.text(((MemeWt - M4Wt)/2,((int(MemeHt * 0.75)+(M1Ht * MemeLinespacing)-thickness))), Mstr4, font=Line4Font, fill =MemeTextShadowColor)
        imageBd.text(((MemeWt - M4Wt)/2,((int(MemeHt * 0.75)+(M1Ht * MemeLinespacing)+thickness))), Mstr4, font=Line4Font, fill =MemeTextShadowColor)
    elif MemeTextShadowOn == "thick":
        thickness = 2
        imageBd.text((((MemeWt - M4Wt)/2)-thickness,((int(MemeHt * 0.75)+(M1Ht * MemeLinespacing)-thickness))), Mstr4, font=Line4Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M4Wt)/2)+thickness,((int(MemeHt * 0.75)+(M1Ht * MemeLinespacing)-thickness))), Mstr4, font=Line4Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M4Wt)/2)-thickness,((int(MemeHt * 0.75)+(M1Ht * MemeLinespacing)-thickness))), Mstr4, font=Line4Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M4Wt)/2)+thickness,((int(MemeHt * 0.75)+(M1Ht * MemeLinespacing)+thickness))), Mstr4, font=Line4Font, fill =MemeTextShadowColor)
    elif MemeTextShadowOn == "thicker":
        thickness = 3
        imageBd.text((((MemeWt - M4Wt)/2)-thickness,((int(MemeHt * 0.75)+(M1Ht * MemeLinespacing)-thickness))), Mstr4, font=Line4Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M4Wt)/2)+thickness,((int(MemeHt * 0.75)+(M1Ht * MemeLinespacing)-thickness))), Mstr4, font=Line4Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M4Wt)/2)-thickness,((int(MemeHt * 0.75)+(M1Ht * MemeLinespacing)-thickness))), Mstr4, font=Line4Font, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M4Wt)/2)+thickness,((int(MemeHt * 0.75)+(M1Ht * MemeLinespacing)+thickness))), Mstr4, font=Line4Font, fill =MemeTextShadowColor)
    
    imageBd.text(((MemeWt - M4Wt)/2,(int(MemeHt * 0.75)+(M1Ht * MemeLinespacing))), Mstr4, font=Line4Font, fill =MemeTextFontColor)
    
    # LINE 5
    Mstr5=("Learning Important Factual Equivalents, 2020")
    M5Wt,M5Ht=Line5Font.getsize(Mstr5)

    imageBd.text((((MemeWt - M5Wt)/2),MemeHt - TextpadY - M5Ht), Mstr5, font=Line5Font, fill =MemeDiscFontColor)

    Bgimage.save("MemeCard0"+str(meme_count) + ".jpg", "JPEG")

    # Move image to frame
    MemeCard = ImageTk.PhotoImage(Bgimage)
    return MemeCard