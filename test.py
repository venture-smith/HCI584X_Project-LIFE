'''
from PIL import Image, ImageDraw, ImageFont
 
img = Image.new('RGB', (100, 30), color = (73, 109, 137))
 


'''
from tkinter import *
import PIL
from PIL import ImageTk, Image, ImageDraw, ImageFont

root=Tk()
Fdimage = Image.open("images\\t-mcdonalds-Big-Mac.jpg")
Bgimage = Image.open("images\WhiteBG.png")

MemeHt = 500
MemeWt = 500
ImagepadX = 10
canvas=Canvas(root, height=MemeHt, width=MemeWt)
Fdwidth = MemeWt - (ImagepadX * 2)
FdimageW, FdimageH = Fdimage.size
wpercent = (Fdwidth / float(FdimageW))
print (wpercent)
hsize = int((float(Fdimage.size[1]) * float(wpercent)))
Fdimage = Fdimage.resize((Fdwidth, hsize), PIL.Image.ANTIALIAS)
vpos = int((MemeHt - hsize) / 2)
print ("hsize=",hsize)
print ("vpos=",vpos)
# Paste in food item
Bgimage.paste(Fdimage,(ImagepadX,vpos))
imageBd = ImageDraw.Draw(Bgimage)
myFont = ImageFont.truetype('fonts/impact.ttf', 40)
imageBd.text((0, 0), "The tough realization", font=myFont, fill =(255, 0, 0))

photo = ImageTk.PhotoImage(Bgimage)

item4 = canvas.create_image(250, 250, image=photo)
canvas.pack(side = TOP, expand=True, fill=BOTH, anchor=CENTER)

Bgimage.save('test.png')


root.mainloop()

'''
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