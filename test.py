from tkinter import *
import PIL
from PIL import ImageTk, Image, ImageDraw, ImageFont

root=Tk()

MemeHt = 500
MemeWt = 500
ImagepadX = 10
TextpadY = 10
MemeLinespacing = 1.1
defaultFdImg = "images\\t-mcdonalds-Big-Mac.jpg"
defaultBG = "images\WhiteBG.png"

Fdimage = Image.open(defaultFdImg)
Bgimage = Image.open(defaultBG)

# Open a window the size of the Preset Meme height and width
canvas=Canvas(root, height=MemeHt, width=MemeWt)
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
Mstr1="The tough realization"
M1Wt,M1Ht=myFont.getsize(Mstr1)
#imageBd.text((0, 0), Mstr1, font=myFont, fill =(255, 0, 0))
#imageBd.text(((MemeWt - M1Wt)/2,(MemeHt - M1Ht)/2), Mstr1, font=myFont, fill =(255, 0, 0))
imageBd.text(((MemeWt - M1Wt)/2,TextpadY), Mstr1, font=myFont, fill =(255, 0, 0))

# LINE 2
Mstr2="that this is the equivalent of"
M2Wt,M2Ht=myFont.getsize(Mstr2)
#imageBd.text((0, 0), Mstr1, font=myFont, fill =(255, 0, 0))
imageBd.text(((MemeWt - M2Wt)/2,(TextpadY + int(M1Ht * MemeLinespacing))), Mstr2, font=myFont, fill =(255, 0, 0))

# LINE 3
Mstr3="44 minutes of"
#Mstr3="30 minutes of"
#Mstr3="63 minutes of"
M3Wt,M3Ht=myFont.getsize(Mstr3)
#imageBd.text((0, 0), Mstr1, font=myFont, fill =(255, 0, 0))
imageBd.text(((MemeWt - M3Wt)/2,(int(MemeHt * 0.75))), Mstr3, font=myFont, fill =(255, 0, 0))

# LINE 4
Mstr4="high impact aerobics..."
#Mstr4="jogging..."
#Mstr4="active Sex..."
M4Wt,M4Ht=myFont.getsize(Mstr4)
#imageBd.text((0, 0), Mstr1, font=myFont, fill =(255, 0, 0))
imageBd.text(((MemeWt - M4Wt)/2,(int(MemeHt * 0.75)+(M1Ht * MemeLinespacing))), Mstr4, font=myFont, fill =(255, 0, 0))

# Move image to frame
photo = ImageTk.PhotoImage(Bgimage)

item4 = canvas.create_image(250, 250, image=photo)
canvas.pack(side = TOP, expand=True, fill=BOTH, anchor=CENTER)

Bgimage.save('test.png')

root.mainloop()

'''
# ADDITIONAL TRANSFORMATION EXAMPLES
im = Image.open("images\\t-mcdonalds-Big-Mac.jpg")
print(im.format, im.size, im.mode)
#im.show()

out = im.resize((128, 128))
out = im.rotate(45) # degrees counter-clockwise

out = im.transpose(Image.FLIP_LEFT_RIGHT)
out = im.transpose(Image.FLIP_TOP_BOTTOM)
out = im.transpose(Image.ROTATE_90)
out = im.transpose(Image.ROTATE_180)
out = im.transpose(Image.ROTATE_270)
out.show()
'''