#-------------------------------------------------------------------------------
# Name:      main.py
# Purpose:   Primary program flow for LIFE webapp
# Author(s): Vincent Lin
# Created:   06/10/2020
# TODO:      XXX YYY ZZZ
# Note:      Need to pull in data from this: https://exceltemplate.net/weight/calorie-tracker/
#            Restaurant and food item calorie sources from: http://fastfoodmacros.com/
#-------------------------------------------------------------------------------

###### 1. IMPORT MODULES

# Using Tkinter to create a window to display application, will investigate creating a web app 
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.scrolledtext as tkst
# import sqlite3 # Bring this back in if we end up using a database for a webapp.
from tkinter import messagebox as msgbox
from PIL import ImageTk, Image
import fileinput # May not need this module - imported from a different application.
from lookup import *

# Preferences
from preferences import *

# 2. SET UP DATA STRUCTURES
# Data Hierarchy - Account - User - Preferences - Transaction history

# Setup Restaurant-Food-Calorie Dictionary
food_dict = {}
with open(foodfile, 'r') as data_file:
    data = csv.DictReader(data_file, delimiter=",")
    for row in data:
        item = food_dict.get(row["Restaurant"], dict())
        item[row["Item"]] = (int(row["Calories"]),row["Image"])
        #item[row["Item"]] = int(row["Calories"]) # This is from an older version with fewer columns
        food_dict[row["Restaurant"]] = item

# Setup Exercise table with Conversion Weight Calorie Burn rates
exertable = {}
with open(exfile, 'r') as data_file:
    data = csv.DictReader(data_file, delimiter=",")
    for row in data:
        #exertable.update({row["Exercise"]:row["Multiplier"]}) # This version only assumes two columns
        exertable.update({row["Exercise"]:[row["Multiplier"],row["Phrase"]]}) # This version assumes three columns, but the "value" is a list of two items.

class Account:
    # Create user account
    def __init__(self, id, LoginId, Email, Password, FirstName, LastName, Pref1, Pref2, Pref3, Weight, Units, Item, MinEquiv1, MinEquiv2, MinEquiv3):
        self.id = id
        self.LoginId = LoginId
        self.Email = Email
        self.Password = Password
        self.FirstName = FirstName
        self.LastName = LastName
        self.Pref1 = Pref1
        self.Pref2 = Pref2
        self.Pref3 = Pref3
        self.Weight = Weight
        self.Units = Units
        self.Item = Item
        self.MinEquiv1 = MinEquiv1
        self.MinEquiv2 = MinEquiv2
        self.MinEquiv3 = MinEquiv3
 
    def getId(self):
        return self.id

    def getLoginId(self):
        return self.LoginId

    def getEmail(self):
        return self.Email
 
    def getPassword(self):
        return self.Password
 
    def getFirstName(self):
        return self.FirstName
 
    def getLastName(self):
        return self.LastName

    def getPref1(self):
        return self.Pref1
    
    def getPref2(self):
        return self.Pref2

    def getPref3(self):
        return self.Pref3

    def getWeight(self):
        return self.Weight

    def getUnits(self):
        return self.Units

    def getItem(self):
        return self.Item

    def getMinEquiv1(self):
        return self.MinEquiv1

    def getMinEquiv2(self):
        return self.MinEquiv2

    def getMinEquiv3(self):
        return self.MinEquiv3

class Item:
        # Create user account
    def __init__(self, Restaurant, Food, Calories):
        self.id = id
        self.Restaurant = Restaurant
        self.Food = Food
        self.Calories = Calories

    def getRestaurant(self):
        return self.Restaurant

    def getFood(self):
        return self.Food

    def getCalories(self):
        return self.Calories

# Main Calculation
def get_minutes(req_exercise, weight, units, src_calories, exertable):
    if units == "LB":
        wconv = 1
    elif units == "KG":
        wconv = 2.20462262
    else: 
        print("ERROR: NO ACCEPTABLE WEIGHT UNIT CONVERSION PASSED")
    #Multiple = exertable.get(req_exercise)
    Multiple = exertable[req_exercise][0] # Note the second item is the number of the item in the exertable list - in this case the first item starts with 0
    MultiplierX = float(Multiple)
    Minutes = (src_calories) / (weight * wconv * MultiplierX)
    return Minutes
    # Original using Dictreader

from app_class_def import App

# Application class 
class App(object):
    def __init__(self, master):

        self.master = master # Naming the master widget       	
        self.master.title("LIFE PROTOTYPE") #window title
        master.geometry(appresolution)
        self.frame = None
        self.switch_to_main() # start with frame "A" Main
        self.fss = 0
        self.meme_count = 1 # CH: Which meme are we showing?

        # Create menu bar
        menu = Menu(self.master) 
        # CH this is copy/pasted from here: http://effbot.org/tkinterbook/menu.htm
        # create a pulldown menu, and add it to the menu bar
        mainmenu = Menu(menu, tearoff=0)
        #menu.add_cascade(label="Main", menu=mainmenu)
        menu.add_command(label="Main", command=self.switch_to_main)
        #mainmenu.add_command(label="Exit", command=root.quit)

        #signupmenu = Menu(menu, tearoff=0)
        #menu.add_cascade(label="Signup", menu=signupmenu)
        #menu.add_command(label="Load Preferences", command=self.switch_to_signup)

        setexprefmenu = Menu(menu, tearoff=0)
        menu.add_command(label="Exercise Prefs", command=self.switch_to_setexpref)

        findfoodmenu = Menu(menu, tearoff=0)
        menu.add_command(label="Fast Food Match", command=self.switch_to_findfood)

        optionsmenu = Menu(menu, tearoff=0)
        optionsmenu.add_command(label="About LIFE", command=self.about)
        #optionsmenu.add_command(label="Change password", command=self.switch_to_main)
        optionsmenu.add_separator()
        optionsmenu.add_command(label="Logout", command=self.switch_to_result)

        menu.add_cascade(label="Options", menu=optionsmenu)

        self.master.config(menu=menu)
    
    # This section reserved for save settings
    # Based on https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter#:~:text=One%20way%20to%20switch%20frames,use%20any%20generic%20Frame%20class.
    def switch_to_signup(self):
        if self.frame is not None:
            self.frame.destroy() # remove current frame
        self.frame = Frame(self.master, background="white", width=640, height=480) # B
        self.frame.pack(fill=BOTH)

        # as you are inside the App class, it's better to make these into attributes, rather than globals
        #global u_name
        global f_name
        global l_name
        global email
        global pw

        self.u_name = Entry(self.frame, width=30) # make/overwrite attribute
        self.u_name.grid(row=0, column=1, padx=20)
        f_name = Entry(self.frame, width=30)
        f_name.grid(row=1, column=1, padx=20)
        l_name = Entry(self.frame, width=30)
        l_name.grid(row=2, column=1)
        email = Entry(self.frame, width=30)
        email.grid(row=3, column=1)
        pw = Entry(self.frame, width=30)
        pw.grid(row=4, column=1)
        #Labels
        u_name_label = Label(self.frame, text="User Name")
        u_name_label.grid(row=0, column=0)
        f_name_label = Label(self.frame, text="First Name")
        f_name_label.grid(row=1, column=0)
        l_name_label = Label(self.frame, text="Last Name")
        l_name_label.grid(row=2, column=0)        
        email_name_label = Label(self.frame, text="Email")
        email_name_label.grid(row=3, column=0)
        pw_label = Label(self.frame, text="Password")
        pw_label.grid(row=4, column=0)
        # Submit button
        submit_button = Button(self.frame, text="Submit",command=self.switch_to_submitted)         
        submit_button.grid(row=6, column=0, columnspan=2, pady=5, padx=5, ipadx=50)
        # put B label in self.frame
        self.start_label = Label(self.frame, text="Sign up")
        self.start_label.pack()

        # put C label in self.frame
        self.start_label = Label(self.frame, text="Set Exercise Preferences")
        self.start_label.pack()

    def switch_to_submitted(self):
        if self.frame is not None:
            self.frame.destroy() # remove current frame
        self.frame = Frame(self.master, background="white", width=appwidth, height=appheight) # C
        self.frame.pack(fill=BOTH)
        write_to_csv(accountfile, self.u_name) 
        # put C label in self.frame
        self.start_label = Label(self.frame, text="Submitted")
        self.start_label.pack()

    def switch_to_setexpref(self):
        if self.frame is not None:
            self.frame.destroy() # remove current frame
        self.frame = Frame(self.master, background="white", width=appwidth, height=appheight) 
        self.frame.pack(fill=BOTH)

        # Auto Complete Code from: https://stackoverflow.com/questions/47839813/python-tkinter-autocomplete-combobox-with-like-search
        def on_keyrelease(event):

            # get text from entry
            entry_widget = event.widget.get()   # CH: make clear what the class/type is
            value = entry_widget.strip().lower()

            # get data from test_list
            if value == '':
                data = self.exercise_list # CH test_list is not defined here
            else:
                data = []
                for item in self.exercise_list:
                    if value in item.lower():
                        data.append(item)                

            # update data in listbox
            listbox_update(data)

        def listbox_update(data):
            # delete previous data
            listbox.delete(0, 'end')
            # sorting data 
            data = sorted(data, key=str.lower)
            # put new data
            for item in data:
                listbox.insert('end', item)

        def on_select(event):
            # display element selected on list
            print('(event) previous:', event.widget.get('active'))
            print('(event)  current:', event.widget.get(event.widget.curselection()))
            print('---')
            current_selection = event.widget.get(event.widget.curselection())
           
            # If this is the first time running and not reset STATE 0, look for the first empty slot to add one - indicate the slot just filled STATE X (slot just filled)
            
            if userzero.Pref1 == "NA":  # Look for the first open slot starting with the first slot
                self.fa1.set(current_selection)
                userzero.Pref1 = current_selection
                self.fss = 1 
            elif userzero.Pref2 == "NA": # Look for open slot on #2
                self.fa2.set(current_selection)
                userzero.Pref2 = current_selection
                self.fss = 2
            elif userzero.Pref3 == "NA": # Look for open slot on #3
                self.fa3.set(current_selection)
                userzero.Pref3 = current_selection
                self.fss = 3
            elif self.fss == 0: # If no open slots, start with replacing the first one if beginning of sequence
                self.fa1.set(current_selection)
                userzero.Pref1 = current_selection
                self.fss = 1 
            elif self.fss == 1: # Go to next in sequence
                self.fa2.set(current_selection)
                userzero.Pref2 = current_selection
                self.fss = 2
            elif self.fss == 2:
                self.fa3.set(current_selection)
                userzero.Pref3 = current_selection
                self.fss = 3
            elif self.fss == 3: # If last start back at the beginning
                self.fa1.set(current_selection)
                userzero.Pref1 = current_selection
                self.fss = 1 

        # Add sub-frames - note the %s for appwidth need to add to 1.
        f1 = Frame(self.frame, background="white", width=appwidth*0.4, height=appheight)
        f2 = Frame(self.frame, background="white", width=appwidth*0.4, height=appheight)
        f3 = Frame(self.frame, background="white", width=appwidth*0.2, height=appheight)
        f1.pack(side=LEFT)
        f2.pack(side=LEFT)
        f3.pack(side=LEFT)
        
        # Add sub-sub-frames - THIS IS AN EXAMPLE IF WE WANT TO GET FANCY
        #f1suba = Frame(f1, background="white")
        #f1subb = Frame(f1, background="white")
        #f1suba.pack(side=TOP, padx=20, pady=20)
        #f1subb.pack(side=BOTTOM)
        #f2suba = Frame(f2, background="white")
        #f2subb = Frame(f2, background="white")
        #f2suba.pack(side=TOP)
        #f2subb.pack(side=BOTTOM)

        # Create list of Exercises from Exercise table to use in the list box
        self.exercise_list = [] # Create list for dictionary        
        self.exercise_list = list(exertable.keys())

        # Initialize Favorite Activity Tk state var that automatically update
        self.fa1 = StringVar()
        self.fa2 = StringVar()
        self.fa3 = StringVar()
        self.fa1.set(userzero.Pref1)
        self.fa2.set(userzero.Pref2)
        self.fa3.set(userzero.Pref3)

        # COLUMN1
        self.start_label = Label(f1, text="Choose your top 3\nPREFERRED Physical Activites:",bg='white')
        self.start_label.config(font=headfont)
        self.start_label.place(in_= f1, relx = 0.5, rely = 0.05, anchor=CENTER)

        self.exer_instruct_label = Label(f1, text="Scroll down the list to find your activity\nof interest. Select the activity by clicking on it.\n\nTry typing the first few characters describing\nyour activity to filter the list.",justify=LEFT,bg='white')
        self.exer_instruct_label.place(in_= f1, relx = 0.1, rely = 0.10, anchor=NW)

        entry = tk.Entry(f1) # Tkinter type Entry Box
        entry.place(in_= f1, relx = 0.1, rely = 0.25, anchor = NW, width=220)
        #entry.pack(side = LEFT, expand = True, fill = Y)
        entry.bind('<KeyRelease>', on_keyrelease)

        searchimg = ImageTk.PhotoImage(Image.open(searchimgpath))
        self.search_image = Label(f1, image = searchimg)
        self.search_image.image = searchimg # Had to add this to "anchor" image - don't know why
        self.search_image.place(in_=f1, relx = 0.9, rely=0.265, anchor = CENTER)

        # Create Listbox of Exercises
        listbox = tk.Listbox(f1)
        listbox.place(in_= f1, relx = 0.1, rely = 0.30, anchor=NW, height = 250, width = 250)
        #listbox.bind('<Double-Button-1>', on_select) # Not sure what this is - look it up!
        listbox.bind('<<ListboxSelect>>', on_select)
        listbox_update(self.exercise_list)
        # Add scrollbar to listbox https://www.geeksforgeeks.org/scrollable-listbox-in-python-tkinter/
        scrollbar = Scrollbar(f1)
        scrollbar.place(in_=f1, relx = 0.9, rely = 0.30, anchor=NW, height=250)
        listbox.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = listbox.yview)

        # COLUMN 2
        self.fav1a_label = Label(f2, text="FAVORITE ACTIVITY #1",bg='white')
        self.fav1a_label.config(font=subheadfont)
        self.fav1a_label.place(in_= f2, relx = 0.5, rely = 0.22, anchor=N)

        self.fav1b_label = Label(f2, textvariable = self.fa1,bg='white')
        self.fav1b_label.place(in_= f2, relx = 0.5, rely = 0.28, anchor=N)

        self.fav2a_label = Label(f2, text="FAVORITE ACTIVITY #2",bg='white')
        self.fav2a_label.config(font=subheadfont)
        self.fav2a_label.place(in_= f2, relx = 0.5, rely = 0.37, anchor=N)

        self.fav2b_label = Label(f2, textvariable = self.fa2,bg='white')
        self.fav2b_label.place(in_= f2, relx = 0.5, rely = 0.43, anchor=N)

        self.fav3a_label = Label(f2, text="FAVORITE ACTIVITY #3",bg='white')
        self.fav3a_label.config(font=subheadfont)
        self.fav3a_label.place(in_= f2, relx = 0.5, rely = 0.52, anchor=N)

        self.fav3b_label = Label(f2, textvariable = self.fa3,bg='white')
        self.fav3b_label.place(in_= f2, relx = 0.5, rely = 0.58, anchor=N)

        # COLUMN 3
        self.exnext_button = Button(f3, text ="Next", bg=buttcolor, command = self.switch_to_weight)
        self.exnext_button.place(in_= f3, relx = 0.5, rely = 0.4, anchor=CENTER)

    def switch_to_weight(self):
        
        def unit_sel():
            print( "You selected the option " + str(self.uvar.get()))
            unitwt = str(self.uvar.get())
            userzero.Units = unitwt

        def wton_keyrelease(event):
            # get text from entry
            value = event.widget.get()
            userzero.Weight = value
            print (userzero.Weight)

        if self.frame is not None:
            self.frame.destroy() # remove current frame
        self.frame = Frame(self.master, background="white", width=appwidth, height=appheight) 
        self.frame.pack(side = LEFT, fill= Y)

        # Reset current meme to 1
        self.meme_count = 1  # CH why is this done here?




        # Add sub-frames
        f1 = Frame(self.frame, background="white", width=appwidth*.2, height=appheight)
        f2 = Frame(self.frame, background="white", width=appwidth*.4, height=appheight)
        f3 = Frame(self.frame, background="white", width=appwidth*.2, height=appheight)
        f4 = Frame(self.frame, background="white", width=appwidth*.2, height=appheight)
        f1.pack(side=LEFT)
        f2.pack(side=LEFT)
        f3.pack(side=LEFT)
        f4.pack(side=LEFT)

        self.back_button = Button(f1, text ="Back", bg=buttcolor,command = self.switch_to_setexpref)
        self.back_button.place(in_= f1, relx = 0.5, rely = 0.4, anchor=CENTER)
        
        self.start_label = Label(f2, text="ENTER YOUR WEIGHT:", bg='white')
        self.start_label.config(font=subheadfont)
        self.start_label.place(in_=f2, relx = 0.5, rely = 0.36, anchor = CENTER)

        v = IntVar()
        v.set(userzero.Weight)
        wtentry = tk.Entry(f2, text=v) # Tkinter type Entry Box
        wtentry.place(in_= f2, relx = 0.5, rely = 0.40, anchor = CENTER, width=50)
        wtentry.bind('<KeyRelease>', wton_keyrelease)
        
        # LBS vs KGS
        self.uvar = StringVar()
        self.uvar.set(userzero.Units)
        R1 = Radiobutton(f3, text="Pounds/Lbs.", bg=buttcolor, variable=self.uvar, value="LB",
                        command=unit_sel)
        R1.place(in_=f3, relx = 0.1, rely = 0.35, anchor = NW )

        R2 = Radiobutton(f3, text="Kilograms/Kgs.", bg=buttcolor, variable=self.uvar, value="KG",
                        command=unit_sel)
        R2.place(in_=f3, relx = 0.1, rely = 0.40, anchor = NW )

        # Next button
        self.wtnext_button = Button(f4, text ="Next", bg=buttcolor, command = self.switch_to_findfood)
        self.wtnext_button.place(in_= f4, relx = 0.5, rely = 0.4, anchor=CENTER)

    def switch_to_findfood(self):
        if self.frame is not None:
            self.frame.destroy() # remove current frame
        self.frame = Frame(self.master, background="white", width=appwidth, height=appheight) 
        self.frame.pack(side = LEFT, fill= Y)

        # Reset current meme to 1
        self.meme_count = 1

        # Add sub-frames
        f1 = Frame(self.frame, background="white", width=appwidth*.2, height=appheight)
        f2 = Frame(self.frame, background="white", width=appwidth*.3, height=appheight)
        f3 = Frame(self.frame, background="white", width=appwidth*.3, height=appheight)
        f4 = Frame(self.frame, background="white", width=appwidth*.2, height=appheight)
        f1.pack(side=LEFT)
        f2.pack(side=LEFT)
        f3.pack(side=LEFT)
        f4.pack(side=LEFT)
        
        def foodbox_update(data):
            # delete previous data
            foodbox.delete(0, 'end')
            # sorting data 
            data = sorted(data, key=str.lower)
            # put new data
            for item in data:
                foodbox.insert('end', item)

        def ron_select(event):
            # register restaurant and narrow list of food items
            print('(event) previous:', event.widget.get('active'))
            print('(event)  current:', event.widget.get(event.widget.curselection()))
            print('---')
            Foodbox.delete(0, END)
            rcurrent_selection = event.widget.get(event.widget.curselection())
            userzero.Item.Restaurant = rcurrent_selection
            fdict = []
            flist = []
            fdict = food_dict.get(rcurrent_selection)
            flist = list(fdict)
            # print (flist) # DIAGNOSTIC
            print ("Selected:",userzero.Item.Restaurant)
            for d in flist:
                Foodbox.insert('end',d)

        def fon_select(fevent):
            # display element selected on list
            # print('(event) previous:', fevent.widget.get('active')) # DIAGNOSTIC
            # print('(event)  current:', fevent.widget.get(fevent.widget.curselection()))
            # print('---')
            fcurrent_selection = fevent.widget.get(fevent.widget.curselection())
            userzero.Item.Food = fcurrent_selection
            print ("Food Selected:",userzero.Item.Food) # DIAGNOSTIC

        # Pull restaurant list from Food Dictionary for use in Selection List
        restaurant_list = []
        restaurant_list = list(food_dict)
        
         # put label in self.frame
        self.back_button = Button(f1, text ="Back", bg=buttcolor,command = self.switch_to_weight)
        self.back_button.place(in_= f1, relx = 0.5, rely = 0.4, anchor=CENTER)

        self.chooser_label = Label(f2, text="CHOOSE A RESTAURANT:", bg='white')
        self.chooser_label.config(font=subheadfont)
        self.chooser_label.place(in_=f2, relx = 0.5, rely = 0.25, anchor = CENTER)

        # Create Listbox of Restaurants
        Rlistbox = tk.Listbox(f2, exportselection=False) # NOTE: need to have the exportselection = false feature when you have two listboxes otherwise it will have problems
        Rlistbox.place(in_= f2, relx = 0.1, rely = 0.30, anchor=NW, height = 250, width = 180)
        #listbox.bind('<Double-Button-1>', on_select) # Not sure what this is - look it up!
        Rlistbox.bind('<<ListboxSelect>>', ron_select)
        for d in restaurant_list:
            Rlistbox.insert('end',d)
        
        # Add scrollbar to listbox https://www.geeksforgeeks.org/scrollable-listbox-in-python-tkinter/
        scrollbar = Scrollbar(f2)
        scrollbar.place(in_=f2, relx = 0.95, rely = 0.30, anchor=NW, height=250)
        Rlistbox.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = Rlistbox.yview)

        # Create Listbox of Food Items
        Foodbox = tk.Listbox(f3, exportselection=False)
        Foodbox.place(in_= f3, relx = 0.1, rely = 0.30, anchor=NW, height = 250, width = 180)
        Foodbox.bind('<<ListboxSelect>>', fon_select)

        # Add scrollbar to listbox https://www.geeksforgeeks.org/scrollable-listbox-in-python-tkinter/
        scrollbar = Scrollbar(f3)
        scrollbar.place(in_=f3, relx = 0.95, rely = 0.30, anchor=NW, height=250)
        Foodbox.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = Foodbox.yview)

        self.fdnext_button = Button(f4, text ="Next", bg=buttcolor, command = self.switch_to_result)
        self.fdnext_button.place(in_= f4, relx = 0.5, rely = 0.4, anchor=CENTER)

    def switch_to_result(self):
        if self.frame is not None:
            self.frame.destroy() # remove current frame
        self.frame = Frame(self.master, background="white", width=appwidth, height=appheight) 
        self.frame.pack(fill=BOTH)
        
        # Reset current meme to 1
        self.meme_count = 1

        # Add sub-frames
        f1 = Frame(self.frame, background="white", width=appwidth*.2, height=appheight)
        f2 = Frame(self.frame, background="white", width=appwidth*.6, height=appheight)
        f3 = Frame(self.frame, background="white", width=appwidth*.2, height=appheight)
        f1.pack(side=LEFT)
        f2.pack(side=LEFT)
        f3.pack(side=LEFT)

        # COLUMN ONE
        self.back_button = Button(f1, text ="Back", bg=buttcolor,command = self.switch_to_findfood)
        self.back_button.place(in_= f1, relx = 0.5, rely = 0.4, anchor=CENTER)

        # COLUMN TWO
        self.chooser_label = Label(f2, text="RESULT:", bg='white')
        self.chooser_label.config(font=subheadfont)
        self.chooser_label.place(in_=f2, relx = 0.5, rely = 0.25, anchor = CENTER)

        self.food_label = Label(f2, text= userzero.Item.Restaurant +" "+ userzero.Item.Food, bg='white')
        self.food_label.config(font=subheadfont)
        self.food_label.place(in_=f2, relx = 0.5, rely = 0.30, anchor = CENTER)

        self.calories_label = Label(f2, text= "Calories="+str(food_dict[userzero.Item.Restaurant][userzero.Item.Food][0]), bg='white')
        self.calories_label.config(font=subheadfont)
        self.calories_label.place(in_=f2, relx = 0.5, rely = 0.35, anchor = CENTER)

        # Add an if statement in case they only pick one preferred exercise (note that theoretically there should always be at least one exercise chosen)
        if userzero.Pref1 != "NA":
            userzero.MinEquiv1 = get_minutes(userzero.Pref1, float(userzero.Weight), userzero.Units, float(food_dict[userzero.Item.Restaurant][userzero.Item.Food][0]), exertable) # Get the total numbeer of minutes
            Exer1_string = convert_time_string(userzero.MinEquiv1) # Convert integer minutes to a string that makes sense
            self.ex1equivalent_label = Label(f2, text=Exer1_string +" "+userzero.Pref1, bg='white')
            self.ex1equivalent_label.config(font=subheadfont)
            self.ex1equivalent_label.place(in_=f2, relx = 0.5, rely = 0.40, anchor = CENTER)
        if userzero.Pref2 != "NA":
            userzero.MinEquiv2 = get_minutes(userzero.Pref2, float(userzero.Weight), userzero.Units, float(food_dict[userzero.Item.Restaurant][userzero.Item.Food][0]), exertable)
            Exer2_string = convert_time_string(userzero.MinEquiv2)
            self.ex2equivalent_label = Label(f2, text=Exer2_string +" "+userzero.Pref2, bg='white')
            self.ex2equivalent_label.config(font=subheadfont)
            self.ex2equivalent_label.place(in_=f2, relx = 0.5, rely = 0.45, anchor = CENTER)
        if userzero.Pref3 != "NA":
            userzero.MinEquiv3 = get_minutes(userzero.Pref3, float(userzero.Weight), userzero.Units, float(food_dict[userzero.Item.Restaurant][userzero.Item.Food][0]), exertable)
            Exer3_string = convert_time_string(userzero.MinEquiv3)
            self.ex3equivalent_label = Label(f2, text=Exer3_string +" "+userzero.Pref3, bg='white')
            self.ex3equivalent_label.config(font=subheadfont)
            self.ex3equivalent_label.place(in_=f2, relx = 0.5, rely = 0.50, anchor = CENTER)
        
        # COLUMN THREE
        # Right hand side button to show the first card.
        self.fdnext_button = Button(f3, text ="Show Meme Cards", bg=buttcolor, command = self.show_memes)
        self.fdnext_button.place(in_= f3, relx = 0.5, rely = 0.4, anchor=CENTER)

    def show_memes(self):
        if self.frame is not None:
            self.frame.destroy() # remove current frame
        self.frame = Frame(self.master, background="white", width=appwidth, height=appheight) # A
        self.frame.pack(fill=BOTH)
        print("--Showing Memes--")
        f1 = Frame(self.frame, background="white", width=appwidth * 0.2, height=appheight)
        f2 = Frame(self.frame, background="white", width=appwidth * 0.6, height=appheight)
        f3 = Frame(self.frame, background="white", width=appwidth * 0.2, height=appheight)
        f1.pack(side=LEFT)
        f2.pack(side=LEFT)
        f3.pack(side=LEFT)
        food=userzero.Item
        if self.meme_count == 1: # Depending on which meme currently being shown, set the exercise and minutes string to the correct one. 
            exercise=exertable[userzero.Pref1][1]
            minutes=convert_time_string(userzero.MinEquiv1)
        elif self.meme_count == 2:
            exercise=exertable[userzero.Pref2][1]
            minutes=convert_time_string(userzero.MinEquiv2)
        elif self.meme_count == 3:
            exercise=exertable[userzero.Pref3][1]
            minutes=convert_time_string(userzero.MinEquiv3)

        # Add code to change command button based on which meme page you're on
        self.start_button = Button(f1, text ="Previous", bg=buttcolor, command = self.prev_meme)
        self.start_button.place(in_= f1, relx = 0.5, rely = 0.4, anchor=CENTER)

        # COLUMN 2 MAIN IMAGE
        startimg = get_meme_image(food_dict, food, exercise, minutes, self.meme_count)
        self.start_image = Label(f2, image = startimg)
        self.start_image.image = startimg # Had to add this to "anchor" image - don't know why
        self.start_image.place(in_= f2, relx = 0.5, rely = 0.4, anchor=CENTER)

        # COLUMN 3 Next button
        self.start_button = Button(f3, text ="Next", bg=buttcolor, command = self.next_meme)
        self.start_button.place(in_= f3, relx = 0.5, rely = 0.4, anchor=CENTER)

    # This function is meant to determine which meme card you are currently on, correctly route back to the function if necessary on the correct meme
    def prev_meme(self):
        '''
        if self.frame is not None:
            self.frame.destroy() # remove current frame
        self.frame = Frame(self.master, background="white", width=appwidth, height=appheight) 
        self.frame.pack(fill=BOTH)
        '''
        #self.frame.destroy() # Thought this might work to refresh the frame - but it only succeeds in destroying it - it doesn't come back.
        print("Memcount before=", self.meme_count)
        if self.meme_count == 1:
            print ("going to back to result")
            self.switch_to_result # I don't think this is correctly calling the prior function
        elif self.meme_count == 2:
            self.meme_count -= 1
            print ("going to meme1")
            self.show_memes
        elif self.meme_count == 3:
            self.meme_count -=1
            print ("going to meme2")
            self.show_memes # Start over
        print("Memecount after=",self.meme_count)

        self.show_memes()

    # This function is meant to determine which meme card you are currently on, correctly route back to the function if necessary on the correct meme
    def next_meme(self):
        '''    
        #self.frame.destroy() # Thought this might work to refresh the frame - but it only succeeds in destroying it - it doesn't come back.
    
        print("Memcount before=",self.meme_count)
        if self.meme_count == 1:
            self.meme_count += 1
            print ("going to meme1")

            self.frame = Frame(self.master, background="white", width=appwidth, height=appheight) # A
            self.frame.pack(fill=BOTH)
            f1 = Frame(self.frame, background="white", width=appwidth / 3, height=appheight)
            f2 = Frame(self.frame, background="white", width=appwidth / 3, height=appheight)
            f1.pack(side=LEFT)
            f2.pack(side=LEFT)
            startimg = ImageTk.PhotoImage(Image.open(startimgpath))
            self.start_image = Label(f1, image = startimg)
            self.start_image.image = startimg # Had to add this to "anchor" image - don't know why
            self.start_image.place(in_= f1, relx = 0.5, rely = 0.4, anchor=CENTER)
            print ("TEST DONE")
        elif self.meme_count == 2:
            self.meme_count += 1
            print ("going to meme2")
            meme3 = self.show_memes
        elif self.meme_count == 3:
            self.meme_count = 1
            print ("starting over")
            self.switch_to_main # Start over
        print("Memecount after=",self.meme_count)
        '''

        # CH
        self.meme_count += 1
        if self.meme_count > 3:
            self.meme_count == 1
            self.switch_to_main()
        else:
            self.show_memes()

    def switch_to_main(self):
        if self.frame is not None:
            self.frame.destroy() # remove current frame
        self.frame = Frame(self.master, background="white", width=appwidth, height=appheight) # A
        self.frame.pack(fill=BOTH)

        f1 = Frame(self.frame, background="white", width=appwidth / 3, height=appheight)
        f2 = Frame(self.frame, background="white", width=appwidth / 3, height=appheight)
        f3 = Frame(self.frame, background="white", width=appwidth / 3, height=appheight)
        f1.pack(side=LEFT)
        f2.pack(side=LEFT)
        f3.pack(side=LEFT)
        # put B label in self.frame
        #self.start_label = Label(self.frame, text="PLACEHOLDER: Logo image, example meme, call to action")
        #self.start_label.pack()

        startimg = ImageTk.PhotoImage(Image.open(startimgpath))
        self.start_image = Label(f1, image = startimg)
        self.start_image.image = startimg # Had to add this to "anchor" image - don't know why
        self.start_image.place(in_= f1, relx = 0.5, rely = 0.4, anchor=CENTER)

        self.start_label = Label(f2, text="This program will show you\nwhat your favorite fast food\nequivalents are in terms of\nyour preferred physical activity.", bg="white")
        self.start_label.place(in_= f2, relx = 0.5, rely = 0.4, anchor=CENTER)

        self.start_button = Button(f3, text ="Start Now", bg=buttcolor, command = self.switch_to_setexpref)
        self.start_button.place(in_= f3, relx = 0.5, rely = 0.4, anchor=CENTER)

        #self.chosen_label = Label(f2, text="Choose your\n activity!", bg="white")
        #self.chosen_label.pack(padx=20, pady=20)

  #About
    def about(self):
        if self.frame is not None:
            self.frame.destroy() # remove current frame
        self.frame = Frame(self.master, background="white", width=300, height=100) # A
        self.frame.pack(fill=BOTH)

        # put B label in self.frame
        self.start_label = Label(self.frame, text="ABOUT LIFE: A fastfood, exercise meme generator")
        self.start_label.pack()

    #Do nothing Placeholder
    def donothing(self):
        msgbox.showinfo(title='DO NOTHING', message='PLACEHOLDER')

    def signup(self):
        #Text Boxes
        u_name = Entry(self, width=30)
        u_name.grid(row=0, column=1, padx=20)
        f_name = Entry(self, width=30)
        f_name.grid(row=1, column=1, padx=20)
        l_name = Entry(self, width=30)
        l_name.grid(row=2, column=1)
        email = Entry(self, width=30)
        email.grid(row=3, column=1)
        pw = Entry(self, width=30)
        pw.grid(row=4, column=1)
        #Labels
        u_name_label = Label(self, text="User Name")
        u_name_label.grid(row=0, column=0)
        f_name_label = Label(self, text="First Name")
        f_name_label.grid(row=1, column=0)
        l_name_label = Label(self, text="Last Name")
        l_name_label.grid(row=2, column=0)        
        email_name_label = Label(self, text="Email")
        email_name_label.grid(row=3, column=0)
        pw_label = Label(self, text="Password")
        pw_label.grid(row=4, column=0)
        #submit_btn = Button(self, text="Submit",command = submit)
        #submit_btn.grid(row=5, column=0, columnspan=2, pady=15, padx=15,ipadx=150)

    def prog_exit(self):
        exit()
        #Labels

# Initialize Account values
dItem = Item(dRestaurant, dFood, dCalories)
userzero = Account(did, dLoginId, dEmail, dPassword, dFirstName, dLastName, dPref1, dPref2, dPref3, dWeight, dUnits, dItem, dMinEquiv1, dMinEquiv2, dMinEquiv3)


# Initialize Window
root = Tk()
root.geometry("400x300")

# Run program loop
app = App(root)
root.mainloop()	