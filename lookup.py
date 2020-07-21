#-------------------------------------------------------------------------------
# Name:      lookup.py
# Purpose:   Primary program flow for LIFE webapp
# Author(s): Vincent Lin
# Created:   06/10/2020
# TODO:      XXX YYY ZZZ
# Note:      This function looks up the multiplier to be used in the calculation
#-------------------------------------------------------------------------------

# importing module  
from preferences import * 
import PIL
from PIL import ImageTk, Image, ImageDraw, ImageFont
import csv 

def pull_csv(file, delimiter=','):
    if not delimiter:
        delimiter = ','   # why not set delimiter=',' in function header (instead None?)
    readexertable = csv.DictReader(open(file), delimiter=delimiter)
    return readexertable

def convert_time_string(minutes):
    time_s = ""
    hours = minutes / 60
    rhours = minutes // 60
    mhours = minutes%60
    days = hours / 24
    rdays = hours // 24
    mdays = hours%24

    if days > 2:
        if mdays == 0:
            time_s = (str(int(rdays))+" days of ")
        elif mhours == 0:
            time_s = (str(int(rdays))+" days " + str(int(rhours))+" hours of")        
        else:
            time_s = (str(int(rdays))+" days " + str(int(mdays))+" hours "+str(int(mhours))+" minutes of")
    elif hours > 2:
        if mhours == 0:
            time_s = (str(int(rhours))+" hours of")
        else:
            time_s = (str(int(rhours))+" hours "+str(int(minutes%60))+" minutes of")
    else:
        time_s = (str(int(minutes))+" minutes of")
    return time_s

def get_meme_image(food_dict, food, exercise, minutes, meme_count):
    #weirdly won't pick up food_dict as a global variable - try passing it.
    #global food_dict 
    Fdfilepath = imagepath + food_dict[food.Restaurant][food.Food][1]
    Fdimage = Image.open(Fdfilepath)
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
    myFont = ImageFont.truetype('fonts/impact.ttf', 40)


    # LINE 1
    # Can generate some random phrases based on how many minutes are involved "The eye-popping reality" "The horror sicks in:"
    Mstr1="The tough realization"
    # Get the width and height of the specific string
    M1Wt,M1Ht=myFont.getsize(Mstr1)
    #Generate shadow https://stackoverflow.com/questions/18974194/text-shadow-with-python
    if MemeTextShadowOn == "thin":
        thickness = 1
        imageBd.text((((MemeWt - M1Wt)/2)-thickness,TextpadY), Mstr1, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M1Wt)/2)+thickness,TextpadY), Mstr1, font=myFont, fill =MemeTextShadowColor)
        imageBd.text(((MemeWt - M1Wt)/2,TextpadY-thickness), Mstr1, font=myFont, fill =MemeTextShadowColor)
        imageBd.text(((MemeWt - M1Wt)/2,TextpadY+thickness), Mstr1, font=myFont, fill =MemeTextShadowColor)
    elif MemeTextShadowOn == "thick":
        thickness = 2
        imageBd.text((((MemeWt - M1Wt)/2)-thickness,TextpadY-thickness), Mstr1, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M1Wt)/2)+thickness,TextpadY-thickness), Mstr1, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M1Wt)/2)-thickness,TextpadY-thickness), Mstr1, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M1Wt)/2)+thickness,TextpadY+thickness), Mstr1, font=myFont, fill =MemeTextShadowColor)
    elif MemeTextShadowOn == "thicker":
        thickness = 3
        imageBd.text((((MemeWt - M1Wt)/2)-thickness,TextpadY-thickness), Mstr1, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M1Wt)/2)+thickness,TextpadY-thickness), Mstr1, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M1Wt)/2)-thickness,TextpadY-thickness), Mstr1, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M1Wt)/2)+thickness,TextpadY+thickness), Mstr1, font=myFont, fill =MemeTextShadowColor)
    #Lay down the text
    imageBd.text(((MemeWt - M1Wt)/2,TextpadY), Mstr1, font=myFont, fill =MemeTextFillColor)

    # LINE 2
    # Can generate some random versions of this line
    Mstr2="that this is the equivalent of"
    # Get the width and height of the specific string
    M2Wt,M2Ht=myFont.getsize(Mstr2)
    #Generate shadow
    if MemeTextShadowOn == "thin":
        thickness = 1
        imageBd.text((((MemeWt - M2Wt)/2)-thickness,(TextpadY + int(M1Ht * MemeLinespacing))), Mstr2, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M2Wt)/2)+thickness,(TextpadY + int(M1Ht * MemeLinespacing))), Mstr2, font=myFont, fill =MemeTextShadowColor)
        imageBd.text(((MemeWt - M2Wt)/2,(TextpadY + int(M1Ht * MemeLinespacing))-thickness), Mstr2, font=myFont, fill =MemeTextShadowColor)
        imageBd.text(((MemeWt - M2Wt)/2,(TextpadY + int(M1Ht * MemeLinespacing))+thickness), Mstr2, font=myFont, fill =MemeTextShadowColor)
    elif MemeTextShadowOn == "thick":
        thickness = 2
        imageBd.text((((MemeWt - M2Wt)/2)-thickness,(TextpadY + int(M1Ht * MemeLinespacing)-thickness)), Mstr2, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M2Wt)/2)+thickness,(TextpadY + int(M1Ht * MemeLinespacing)-thickness)), Mstr2, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M2Wt)/2)-thickness,(TextpadY + int(M1Ht * MemeLinespacing)-thickness)), Mstr2, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M2Wt)/2)+thickness,(TextpadY + int(M1Ht * MemeLinespacing)+thickness)), Mstr2, font=myFont, fill =MemeTextShadowColor)
    elif MemeTextShadowOn == "thicker":
        thickness = 3
        imageBd.text((((MemeWt - M2Wt)/2)-thickness,(TextpadY + int(M1Ht * MemeLinespacing)-thickness)), Mstr2, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M2Wt)/2)+thickness,(TextpadY + int(M1Ht * MemeLinespacing)-thickness)), Mstr2, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M2Wt)/2)-thickness,(TextpadY + int(M1Ht * MemeLinespacing)-thickness)), Mstr2, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M2Wt)/2)+thickness,(TextpadY + int(M1Ht * MemeLinespacing)+thickness)), Mstr2, font=myFont, fill =MemeTextShadowColor)
    #Lay down the text
    imageBd.text(((MemeWt - M2Wt)/2,(TextpadY + int(M1Ht * MemeLinespacing))), Mstr2, font=myFont, fill =(255, 0, 0))

    # LINE 3
    Mstr3=minutes
    M3Wt,M3Ht=myFont.getsize(Mstr3)     # Get the width and height of the specific string
    #Generate shadow
    if MemeTextShadowOn == "thin":
        thickness = 1
        imageBd.text(((MemeWt - M3Wt)/2)-thickness,((int(MemeHt * 0.75))), Mstr3, font=myFont, fill =MemeTextShadowColor)
        imageBd.text(((MemeWt - M3Wt)/2)+thickness,((int(MemeHt * 0.75))), Mstr3, font=myFont, fill =MemeTextShadowColor)
        imageBd.text(((MemeWt - M3Wt)/2,((int(MemeHt * 0.75)-thickness))), Mstr3, font=myFont, fill =MemeTextShadowColor)
        imageBd.text(((MemeWt - M3Wt)/2,((int(MemeHt * 0.75)+thickness))), Mstr3, font=myFont, fill =MemeTextShadowColor)
    elif MemeTextShadowOn == "thick":
        thickness = 2
        imageBd.text((((MemeWt - M3Wt)/2)-thickness,((int(MemeHt * 0.75)-thickness))), Mstr3, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M3Wt)/2)+thickness,((int(MemeHt * 0.75)-thickness))), Mstr3, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M3Wt)/2)-thickness,((int(MemeHt * 0.75)-thickness))), Mstr3, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M3Wt)/2)+thickness,((int(MemeHt * 0.75)+thickness))), Mstr3, font=myFont, fill =MemeTextShadowColor)
    elif MemeTextShadowOn == "thicker":
        thickness = 3
        imageBd.text((((MemeWt - M3Wt)/2)-thickness,((int(MemeHt * 0.75)-thickness))), Mstr3, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M3Wt)/2)+thickness,((int(MemeHt * 0.75)-thickness))), Mstr3, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M3Wt)/2)-thickness,((int(MemeHt * 0.75)-thickness))), Mstr3, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M3Wt)/2)+thickness,((int(MemeHt * 0.75)+thickness))), Mstr3, font=myFont, fill =MemeTextShadowColor)
    
    imageBd.text(((MemeWt - M3Wt)/2,(int(MemeHt * 0.75))), Mstr3, font=myFont, fill =(255, 0, 0))

    # LINE 4
    Mstr4=exercise
    #Mstr4="jogging..."
    #Mstr4="active Sex..."
    M4Wt,M4Ht=myFont.getsize(Mstr4)
    #imageBd.text((0, 0), Mstr1, font=myFont, fill =(255, 0, 0))

    if MemeTextShadowOn == "thin":
        thickness = 1
        imageBd.text(((MemeWt - M4Wt)/2)-thickness,((int(MemeHt * 0.75)+(M1Ht * MemeLinespacing))), Mstr4, font=myFont, fill =MemeTextShadowColor)
        imageBd.text(((MemeWt - M4Wt)/2)+thickness,((int(MemeHt * 0.75)+(M1Ht * MemeLinespacing))), Mstr4, font=myFont, fill =MemeTextShadowColor)
        imageBd.text(((MemeWt - M4Wt)/2,((int(MemeHt * 0.75)+(M1Ht * MemeLinespacing)-thickness))), Mstr4, font=myFont, fill =MemeTextShadowColor)
        imageBd.text(((MemeWt - M4Wt)/2,((int(MemeHt * 0.75)+(M1Ht * MemeLinespacing)+thickness))), Mstr4, font=myFont, fill =MemeTextShadowColor)
    elif MemeTextShadowOn == "thick":
        thickness = 2
        imageBd.text((((MemeWt - M4Wt)/2)-thickness,((int(MemeHt * 0.75)+(M1Ht * MemeLinespacing)-thickness))), Mstr4, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M4Wt)/2)+thickness,((int(MemeHt * 0.75)+(M1Ht * MemeLinespacing)-thickness))), Mstr4, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M4Wt)/2)-thickness,((int(MemeHt * 0.75)+(M1Ht * MemeLinespacing)-thickness))), Mstr4, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M4Wt)/2)+thickness,((int(MemeHt * 0.75)+(M1Ht * MemeLinespacing)+thickness))), Mstr4, font=myFont, fill =MemeTextShadowColor)
    elif MemeTextShadowOn == "thicker":
        thickness = 3
        imageBd.text((((MemeWt - M4Wt)/2)-thickness,((int(MemeHt * 0.75)+(M1Ht * MemeLinespacing)-thickness))), Mstr4, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M4Wt)/2)+thickness,((int(MemeHt * 0.75)+(M1Ht * MemeLinespacing)-thickness))), Mstr4, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M4Wt)/2)-thickness,((int(MemeHt * 0.75)+(M1Ht * MemeLinespacing)-thickness))), Mstr4, font=myFont, fill =MemeTextShadowColor)
        imageBd.text((((MemeWt - M4Wt)/2)+thickness,((int(MemeHt * 0.75)+(M1Ht * MemeLinespacing)+thickness))), Mstr4, font=myFont, fill =MemeTextShadowColor)
    
    imageBd.text(((MemeWt - M4Wt)/2,(int(MemeHt * 0.75)+(M1Ht * MemeLinespacing))), Mstr4, font=myFont, fill =(255, 0, 0))
    Bgimage.save("MemeCard0"+str(meme_count) + ".jpg", "JPEG")

    # Move image to frame
    MemeCard = ImageTk.PhotoImage(Bgimage)
    return MemeCard