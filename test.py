from tkinter import *
import PIL
from PIL import ImageTk, Image, ImageDraw, ImageFont
from preferences import *


root=Tk()
# Pre settings for this are in preferences

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
# Get the width and height of the specific string
M1Wt,M1Ht=myFont.getsize(Mstr1)
#Generate shadow
if MemeTextShadowOn == "thin":
    imageBd.text((((MemeWt - M1Wt)/2)-1,TextpadY), Mstr1, font=myFont, fill =MemeTextShadowColor)
    imageBd.text((((MemeWt - M1Wt)/2)+1,TextpadY), Mstr1, font=myFont, fill =MemeTextShadowColor)
    imageBd.text(((MemeWt - M1Wt)/2,TextpadY-1), Mstr1, font=myFont, fill =MemeTextShadowColor)
    imageBd.text(((MemeWt - M1Wt)/2,TextpadY+1), Mstr1, font=myFont, fill =MemeTextShadowColor)
elif MemeTextShadowOn == "thick":
    imageBd.text((((MemeWt - M1Wt)/2)-1,TextpadY-1), Mstr1, font=myFont, fill =MemeTextShadowColor)
    imageBd.text((((MemeWt - M1Wt)/2)+1,TextpadY-1), Mstr1, font=myFont, fill =MemeTextShadowColor)
    imageBd.text((((MemeWt - M1Wt)/2)-1,TextpadY-1), Mstr1, font=myFont, fill =MemeTextShadowColor)
    imageBd.text((((MemeWt - M1Wt)/2)+1,TextpadY+1), Mstr1, font=myFont, fill =MemeTextShadowColor)
elif MemeTextShadowOn == "thicker":
    imageBd.text((((MemeWt - M1Wt)/2)-2,TextpadY-2), Mstr1, font=myFont, fill =MemeTextShadowColor)
    imageBd.text((((MemeWt - M1Wt)/2)+2,TextpadY-2), Mstr1, font=myFont, fill =MemeTextShadowColor)
    imageBd.text((((MemeWt - M1Wt)/2)-2,TextpadY-2), Mstr1, font=myFont, fill =MemeTextShadowColor)
    imageBd.text((((MemeWt - M1Wt)/2)+2,TextpadY+2), Mstr1, font=myFont, fill =MemeTextShadowColor)
#Lay down the text
imageBd.text(((MemeWt - M1Wt)/2,TextpadY), Mstr1, font=myFont, fill =MemeTextFillColor)

# LINE 2
Mstr2="that this is the equivalent of"
# Get the width and height of the specific string
M2Wt,M2Ht=myFont.getsize(Mstr2)
#Generate shadow
if MemeTextShadowOn == "thin":
    imageBd.text((((MemeWt - M2Wt)/2)-1,(TextpadY + int(M1Ht * MemeLinespacing))), Mstr2, font=myFont, fill =MemeTextShadowColor)
    imageBd.text((((MemeWt - M2Wt)/2)+1,(TextpadY + int(M1Ht * MemeLinespacing))), Mstr2, font=myFont, fill =MemeTextShadowColor)
    imageBd.text(((MemeWt - M2Wt)/2,(TextpadY + int(M1Ht * MemeLinespacing))-1), Mstr2, font=myFont, fill =MemeTextShadowColor)
    imageBd.text(((MemeWt - M2Wt)/2,(TextpadY + int(M1Ht * MemeLinespacing))+1), Mstr2, font=myFont, fill =MemeTextShadowColor)
#Lay down the text
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

# CH testing: where is the current folder for me?
from os import getcwd, chdir
print("cwd", getcwd())
# CH go to parent so that the settings work for me
#chdir("..")

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

# This is for a web app database
''' 
def submit():
    # Database functions
        
    conn = sqlite3.connect('LIFE_MemberDB.db')
    c= conn.cursor()
    c.execute("INSERT INTO MemberDb VALUES (:u_name, :f_name, :l_name, :email, :pw)",
        {
            'u_name': u_name.get(),
            'f_name': f_name.get(),
            'l_name': l_name.get(),
            'email': email.get(),
            'pw': pw.get()
        })
    conn.commit()
    conn.close()
'''

# This section placeholder for loading account/previously saved preferences
'''
def login():
    userlvl = Label(win, text = "Username :")
    passwdlvl = Label(win, text = "Password  :")

    user1 = Entry(win, textvariable = StringVar())
    passwd1 = Entry(win, textvariable = IntVar().set(""))

    enter = Button(win, text = "Enter", command = lambda: login(), bd = 0)
    enter.configure(bg = "pink")

    user1.place(x = 200, y = 220)
    passwd1.place(x = 200, y = 270)
    userlvl.place(x = 130, y = 220)
    passwdlvl.place(x = 130, y = 270)
    enter.place(x = 238, y = 325)

    #app.f_name.delete(0, END)
'''