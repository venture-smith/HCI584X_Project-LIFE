from preferences import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.scrolledtext as tkst
from tkinter import messagebox as msgbox
from PIL import ImageTk, Image
import fileinput # May not need this module - imported from a different application.
from lookup import *
from account_class import Account, Item

# Application class 
class App(object):
    def __init__(self, master):

        # SETUP WINDOW
        self.master = master # Naming the master widget       	
        self.master.title("LIFE PROTOTYPE") #window title
        master.geometry(appresolution)
        self.frame = None
        self.switch_to_main() # start with main screen

        # CREATE WINDOW BAR
        # CH this is copy/pasted from here: http://effbot.org/tkinterbook/menu.htm
        # create a pulldown menu, and add it to the menu bar
        menu = Menu(self.master) 
        mainmenu = Menu(menu, tearoff=0)
        menu.add_command(label="Main", command=self.switch_to_main)
        # MENU ITEM 1
        setexprefmenu = Menu(menu, tearoff=0)
        menu.add_command(label="Exercise Prefs", command=self.switch_to_setexpref)
        # MENU ITEM 2
        findfoodmenu = Menu(menu, tearoff=0)
        menu.add_command(label="Fast Food Match", command=self.switch_to_findfood)
        # MENU ITEM 3
        optionsmenu = Menu(menu, tearoff=0)
        optionsmenu.add_command(label="About LIFE", command=self.about)
        optionsmenu.add_separator()
        optionsmenu.add_command(label="Exit", command=self.prog_exit)
        menu.add_cascade(label="Options", menu=optionsmenu)
        self.master.config(menu=menu)

        # INITIALIZE VALUES
        self.fss = 0 # Set count of selected exercises
        self.meme_count = 1 # CH: Which meme are we showing?
        global dItem
        global userzero
        dItem = Item(dRestaurant, dFood, dCalories)
        userzero = Account(did, dLoginId, dEmail, dPassword, dFirstName, dLastName, 
                    dPref1, dPref2, dPref3, dWeight, dUnits, dItem, dMinEquiv1, dMinEquiv2, dMinEquiv3)

    def get_food_dict(self):
        '''
        OUTPUT: food_dict - Dictionary
        Gets the Food table from foodfile from Preferences.py. Uses csv Dictreader to convert into an orderedred dictionary of DictReader type.
        Converts the DictReader to a nested Dictionary, with the outer Dictionary with the "Restaurant" as key, and the Food "Item" as the value.
        In the nested dictionary, the Food "Item" is the key, and each item has a tuple as the value, with the "Calories" being the first item, and the
        "Image" path being the second item.
        '''
        food_dict = {}
        with open(foodfile, 'r') as data_file:
            data = csv.DictReader(data_file, delimiter=",")
            for row in data:
                item = food_dict.get(row["Restaurant"], dict())
                item[row["Item"]] = (int(row["Calories"]),row["Image"])
                food_dict[row["Restaurant"]] = item
        return food_dict

    # Setup Exercise table with Conversion Weight Calorie Burn rates
    def get_exertable(self):
        '''
        OUTPUT: exertable - Dictionary
        Gets Exercise table from exfile path from Preferences.py. Uses csv Dictreader to convert into an ordered dictionary of DictReader type.
        Converts the DictReader to a Dictionary with the string value 'Exercise' as the key. The Values are tuples with the 'Multiplier' as the first 
        item, and the 'Phrase' - a shorthand version of the exercise as the second item in the list.
        '''
        exertable = {}
        with open(exfile, 'r') as data_file:
            data = csv.DictReader(data_file, delimiter=",")
            for row in data:
                exertable.update({row["Exercise"]:[row["Multiplier"],row["Phrase"]]}) # This version assumes three columns, but the "value" is a list of two items.
        return exertable

    # Main Calculation
    def get_minutes(self, req_exercise, weight, units, src_calories, exertable):
        '''
        req_exercise is the exercise string
        weight is given units
        units is in LB or KG
        src_calories is the passed calories of the food item
        exertable is the entire exercise weight conversion table (exercise calories burned per minute by weight)
        '''
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

    # STEP 1: Set Exercise Preference
    def switch_to_setexpref(self):
        '''
        This function shows a scrollable list of exercises/physical activities, and allows the user to select up to 3 preferred exercises.
        Stores the 3 preferred activities as Pref1, Pref2, Pref3.
        '''
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
                data = self.exercise_list
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

        # CREATE FRAMES
        # Create two primary rows
        f1 = Frame(self.frame, background="white", width=appwidth, height=appheight*0.1)
        f2 = Frame(self.frame, background="white", width=appwidth, height=appheight*0.9)
        f1.pack(side=TOP)
        f2.pack(side=BOTTOM)
        # Create sub-columns within the second row
        f2suba = Frame(f2, background="white", width=appwidth * 0.4, height=appheight*0.9)
        f2subb = Frame(f2, background="white", width=appwidth * 0.4, height=appheight*0.9)
        f2subc = Frame(f2, background="white", width=appwidth * 0.2, height=appheight*0.9)
        f2suba.pack(side=LEFT)
        f2subb.pack(side=LEFT)
        f2subc.pack(side=RIGHT)

        # Create list of Exercises from Exercise table to use in the list box
        self.exercise_list = [] # Create list for dictionary 
        exertable = self.get_exertable()       
        self.exercise_list = list(exertable.keys())

        # Initialize Favorite Activity Tk state var that automatically update
        self.fa1 = StringVar()
        self.fa2 = StringVar()
        self.fa3 = StringVar()
        self.fa1.set(userzero.Pref1)
        self.fa2.set(userzero.Pref2)
        self.fa3.set(userzero.Pref3)

        # COLUMN1
        self.start_label = Label(f1, text="STEP 1: Choose your TOP 3 PREFERRED Physical Activites:",bg='white')
        self.start_label.config(font=headfont)
        self.start_label.place(in_= f1, relx = 0.5, rely = 0.5, anchor=CENTER)

        self.exer_instruct_label = Label(f2suba, text="Scroll down the list to find your activity\nof interest. Select the activity by clicking on it.\n\nTry typing the first few characters describing\nyour activity to filter the list.",justify=LEFT,bg='white')
        self.exer_instruct_label.place(in_= f2suba, relx = 0.1, rely = 0.05, anchor=NW)

        entry = tk.Entry(f2suba) # Tkinter type Entry Box
        entry.place(in_= f2suba, relx = 0.1, rely = 0.25, anchor = NW, width=220)
        #entry.pack(side = LEFT, expand = True, fill = Y)
        entry.bind('<KeyRelease>', on_keyrelease)

        searchimg = ImageTk.PhotoImage(Image.open(searchimgpath))
        self.search_image = Label(f2suba, image = searchimg)
        self.search_image.image = searchimg # Had to add this to "anchor" image - don't know why
        self.search_image.place(in_=f2suba, relx = 0.9, rely=0.265, anchor = CENTER)

        # Create Listbox of Exercises
        listbox = tk.Listbox(f2suba)
        listbox.place(in_= f2suba, relx = 0.1, rely = 0.30, anchor=NW, height = 250, width = 250)
        #listbox.bind('<Double-Button-1>', on_select) # Not sure what this is - look it up!
        listbox.bind('<<ListboxSelect>>', on_select)
        listbox_update(self.exercise_list)
        # Add scrollbar to listbox https://www.geeksforgeeks.org/scrollable-listbox-in-python-tkinter/
        scrollbar = Scrollbar(f2suba)
        scrollbar.place(in_=f2suba, relx = 0.9, rely = 0.30, anchor=NW, height=250)
        listbox.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = listbox.yview)

        # COLUMN 2
        self.fav1a_label = Label(f2subb, text="FAVORITE ACTIVITY #1",bg='white')
        self.fav1a_label.config(font=subheadfont)
        self.fav1a_label.place(in_= f2subb, relx = 0.5, rely = 0.22, anchor=N)

        self.fav1b_label = Label(f2subb, textvariable = self.fa1,bg='white')
        self.fav1b_label.place(in_= f2subb, relx = 0.5, rely = 0.28, anchor=N)

        self.fav2a_label = Label(f2subb, text="FAVORITE ACTIVITY #2",bg='white')
        self.fav2a_label.config(font=subheadfont)
        self.fav2a_label.place(in_= f2subb, relx = 0.5, rely = 0.37, anchor=N)

        self.fav2b_label = Label(f2subb, textvariable = self.fa2,bg='white')
        self.fav2b_label.place(in_= f2subb, relx = 0.5, rely = 0.43, anchor=N)

        self.fav3a_label = Label(f2subb, text="FAVORITE ACTIVITY #3",bg='white')
        self.fav3a_label.config(font=subheadfont)
        self.fav3a_label.place(in_= f2subb, relx = 0.5, rely = 0.52, anchor=N)

        self.fav3b_label = Label(f2subb, textvariable = self.fa3,bg='white')
        self.fav3b_label.place(in_= f2subb, relx = 0.5, rely = 0.58, anchor=N)

        # COLUMN 3: NEXT BUTTON
        
        self.exnext_button = Button(f2subc, text ="Next", bg=buttcolor, command = self.switch_to_weight)
        self.exnext_button.place(in_= f2subc, relx = 0.5, rely = 0.4, anchor=CENTER)
        '''
        self.exnext_button = Button(f3, text ="Next", command = self.switch_to_weight)
        img = PhotoImage(file="images/Next.png") # make sure to add "/" not "\"
        self.exnext_button.config(image=img)
        self.exnext_button.place(in_= f3, relx = 0.5, rely = 0.4, anchor=CENTER)
        '''
    def switch_to_weight(self):
        '''
        This function gets the weight in pounds or kilograms and also allows the user to select the preferred unit (LB/KG).
        '''
        def unit_sel():
            print( "You selected the option " + str(self.uvar.get())) # This is a diagnostic
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

        # CREATE FRAMES
        # Create two primary rows
        f1 = Frame(self.frame, background="white", width=appwidth, height=appheight*0.1)
        f2 = Frame(self.frame, background="white", width=appwidth, height=appheight*0.9)
        f1.pack(side=TOP)
        f2.pack(side=BOTTOM)
        # Create sub-columns within the second row
        f2suba = Frame(f2, background="white", width=appwidth * 0.2, height=appheight*0.9) # Use a multiplier in app width to allocate column width
        f2subb = Frame(f2, background="white", width=appwidth * 0.4, height=appheight*0.9)
        f2subc = Frame(f2, background="white", width=appwidth * 0.2, height=appheight*0.9)
        f2subd = Frame(f2, background="white", width=appwidth * 0.2, height=appheight*0.9)
        f2suba.pack(side=LEFT)
        f2subb.pack(side=LEFT)
        f2subc.pack(side=LEFT)
        f2subd.pack(side=LEFT)

        # HEADING
        self.weight_label = Label(f1, text="STEP 2: ENTER YOUR WEIGHT (in Pounds or Kilograms):",bg='white')
        self.weight_label.config(font=headfont)
        self.weight_label.place(in_= f1, relx = 0.5, rely = 0.5, anchor=CENTER)
        
        # COLUMN 1
        self.back_button = Button(f2suba, text ="Back", bg=buttcolor,command = self.switch_to_setexpref)
        self.back_button.place(in_= f2suba, relx = 0.5, rely = 0.4, anchor=CENTER)
        
        # COLUMN 2
        self.start_label = Label(f2subb, text="WEIGHT:", bg='white')
        self.start_label.config(font=subheadfont)
        self.start_label.place(in_=f2subb, relx = 0.5, rely = 0.36, anchor = CENTER)

        v = IntVar()
        v.set(userzero.Weight) # Set the default value, or store the last value
        wtentry = tk.Entry(f2subb, text=v) # Tkinter type Entry Box
        wtentry.place(in_= f2subb, relx = 0.5, rely = 0.40, anchor = CENTER, width=50)
        wtentry.bind('<KeyRelease>', wton_keyrelease) # allows the user to enter the value without hitting enter
        
        # LBS vs KGS
        self.uvar = StringVar()
        self.uvar.set(userzero.Units) # Set the default value, or store the last value
        R1 = Radiobutton(f2subc, text="Pounds/Lbs.", bg=buttcolor, variable=self.uvar, value="LB",
                        command=unit_sel)
        R1.place(in_=f2subc, relx = 0.1, rely = 0.35, anchor = NW )

        R2 = Radiobutton(f2subc, text="Kilograms/Kgs.", bg=buttcolor, variable=self.uvar, value="KG",
                        command=unit_sel)
        R2.place(in_=f2subc, relx = 0.1, rely = 0.40, anchor = NW )

        # Next button
        self.wtnext_button = Button(f2subd, text ="Next", bg=buttcolor, command = self.switch_to_findfood)
        self.wtnext_button.place(in_= f2subd, relx = 0.5, rely = 0.4, anchor=CENTER)

    def switch_to_findfood(self):
        '''
        '''
        if self.frame is not None:
            self.frame.destroy() # remove current frame
        self.frame = Frame(self.master, background="white", width=appwidth, height=appheight) 
        self.frame.pack(side = LEFT, fill= Y)

        # Reset current meme to 1
        self.meme_count = 1

        # CREATE FRAMES
        # Create two primary rows
        f1 = Frame(self.frame, background="white", width=appwidth, height=appheight*0.1)
        f2 = Frame(self.frame, background="white", width=appwidth, height=appheight*0.9)
        f1.pack(side=TOP)
        f2.pack(side=BOTTOM)
        # Create columns within the second row
        f2suba = Frame(f2, background="white", width=appwidth * 0.2, height=appheight*0.9) # Use a multiplier in app width to allocate column width
        f2subb = Frame(f2, background="white", width=appwidth * 0.3, height=appheight*0.9)
        f2subc = Frame(f2, background="white", width=appwidth * 0.3, height=appheight*0.9)
        f2subd = Frame(f2, background="white", width=appwidth * 0.2, height=appheight*0.9)
        f2suba.pack(side=LEFT)
        f2subb.pack(side=LEFT)
        f2subc.pack(side=LEFT)
        f2subd.pack(side=LEFT)

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
            print ("Selected:",userzero.Item.Restaurant)
            for d in flist:
                Foodbox.insert('end',d)

        def fon_select(fevent):
            '''
            Food item selection from list is saved to the set of user variables
            '''
            fcurrent_selection = fevent.widget.get(fevent.widget.curselection())
            userzero.Item.Food = fcurrent_selection
            print ("Food Selected:",userzero.Item.Food) # DIAGNOSTIC

        # Pull restaurant list from Food Dictionary for use in Selection List
        restaurant_list = []
        food_dict = self.get_food_dict() # Retrieve Food dictionary
        restaurant_list = list(food_dict) # Convert dictionary to just a list of restaurants for use in the first selection list
        
        self.weight_label = Label(f1, text="STEP 3: SELECT A RESTAURANT AND FOOD ITEM/ENTREE",bg='white')
        self.weight_label.config(font=headfont)
        self.weight_label.place(in_= f1, relx = 0.5, rely = 0.5, anchor=CENTER)

        # COLUMN 1
        self.back_button = Button(f2suba, text ="Back", bg=buttcolor,command = self.switch_to_weight)
        self.back_button.place(in_= f2suba, relx = 0.5, rely = 0.4, anchor=CENTER)

        self.chooser_label = Label(f2subb, text="CHOOSE A RESTAURANT:", bg='white')
        self.chooser_label.config(font=subheadfont)
        self.chooser_label.place(in_=f2subb, relx = 0.5, rely = 0.25, anchor = CENTER)

        # COLUMN 2
        # Create Listbox of Restaurants
        Rlistbox = tk.Listbox(f2subb, exportselection=False) # NOTE: need to have the exportselection = false feature when you have two listboxes otherwise it will have problems
        Rlistbox.place(in_= f2subb, relx = 0.1, rely = 0.30, anchor=NW, height = 250, width = 180)
        #listbox.bind('<Double-Button-1>', on_select) # Not sure what this is - look it up!
        Rlistbox.bind('<<ListboxSelect>>', ron_select)
        for d in restaurant_list:
            Rlistbox.insert('end',d)
        
        # Add scrollbar to listbox https://www.geeksforgeeks.org/scrollable-listbox-in-python-tkinter/
        scrollbar = Scrollbar(f2subb)
        scrollbar.place(in_=f2subb, relx = 0.95, rely = 0.30, anchor=NW, height=250)
        Rlistbox.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = Rlistbox.yview)

        # COLUMN 3
        # Create Listbox of Food Items
        Foodbox = tk.Listbox(f2subc, exportselection=False)
        Foodbox.place(in_= f2subc, relx = 0.1, rely = 0.30, anchor=NW, height = 250, width = 180)
        Foodbox.bind('<<ListboxSelect>>', fon_select)

        # Add scrollbar to listbox https://www.geeksforgeeks.org/scrollable-listbox-in-python-tkinter/
        scrollbar = Scrollbar(f2subc)
        scrollbar.place(in_=f2subc, relx = 0.95, rely = 0.30, anchor=NW, height=250)
        Foodbox.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = Foodbox.yview)

        # COLUMN 4
        self.fdnext_button = Button(f2subd, text ="Next", bg=buttcolor, command = self.switch_to_result)
        self.fdnext_button.place(in_= f2subd, relx = 0.5, rely = 0.4, anchor=CENTER)

    def switch_to_result(self):
        if self.frame is not None:
            self.frame.destroy() # remove current frame
        self.frame = Frame(self.master, background="white", width=appwidth, height=appheight) 
        self.frame.pack(fill=BOTH)
        
        # Reset current meme to 1
        self.meme_count = 1

        exertable = self.get_exertable()
        food_dict = self.get_food_dict()

        # CREATE FRAMES
        # Create two primary rows
        f1 = Frame(self.frame, background="white", width=appwidth, height=appheight*0.1)
        f2 = Frame(self.frame, background="white", width=appwidth, height=appheight*0.9)
        f1.pack(side=TOP)
        f2.pack(side=BOTTOM)
        # Create columns within the second row
        f2suba = Frame(f2, background="white", width=appwidth * 0.2, height=appheight*0.9) # Use a multiplier in app width to allocate column width
        f2subb = Frame(f2, background="white", width=appwidth * 0.6, height=appheight*0.9)
        f2subc = Frame(f2, background="white", width=appwidth * 0.2, height=appheight*0.9)
        f2suba.pack(side=LEFT)
        f2subb.pack(side=LEFT)
        f2subc.pack(side=LEFT)

        '''
        # Add sub-frames
        f1 = Frame(self.frame, background="white", width=appwidth*.2, height=appheight)
        f2 = Frame(self.frame, background="white", width=appwidth*.6, height=appheight)
        f3 = Frame(self.frame, background="white", width=appwidth*.2, height=appheight)
        f1.pack(side=LEFT)
        f2.pack(side=LEFT)
        f3.pack(side=LEFT)
        '''

        self.weight_label = Label(f1, text="STEP 4: REVIEW RESULT SUMMARY",bg='white')
        self.weight_label.config(font=headfont)
        self.weight_label.place(in_= f1, relx = 0.5, rely = 0.5, anchor=CENTER)

        # COLUMN ONE
        self.back_button = Button(f2suba, text ="Back", bg=buttcolor,command = self.switch_to_findfood)
        self.back_button.place(in_= f2suba, relx = 0.5, rely = 0.4, anchor=CENTER)

        # COLUMN TWO
        self.chooser_label = Label(f2subb, text="RESULT:", bg='white')
        self.chooser_label.config(font=subheadfont)
        self.chooser_label.place(in_=f2subb, relx = 0.5, rely = 0.25, anchor = CENTER)

        self.food_label = Label(f2subb, text= userzero.Item.Restaurant +" "+ userzero.Item.Food, bg='white')
        self.food_label.config(font=subheadfont)
        self.food_label.place(in_=f2subb, relx = 0.5, rely = 0.30, anchor = CENTER)

        self.calories_label = Label(f2subb, text= "Calories="+str(food_dict[userzero.Item.Restaurant][userzero.Item.Food][0]), bg='white')
        self.calories_label.config(font=subheadfont)
        self.calories_label.place(in_=f2subb, relx = 0.5, rely = 0.35, anchor = CENTER)

        # Add an if statement in case they only pick one preferred exercise (note that theoretically there should always be at least one exercise chosen)
        if userzero.Pref1 != "NA":
            userzero.MinEquiv1 = self.get_minutes(userzero.Pref1, float(userzero.Weight), userzero.Units, float(food_dict[userzero.Item.Restaurant][userzero.Item.Food][0]), exertable) # Get the total numbeer of minutes
            Exer1_string = convert_time_string(userzero.MinEquiv1) # Convert integer minutes to a string that makes sense
            self.ex1equivalent_label = Label(f2subb, text=Exer1_string +" "+userzero.Pref1, bg='white')
            self.ex1equivalent_label.config(font=subheadfont)
            self.ex1equivalent_label.place(in_=f2subb, relx = 0.5, rely = 0.40, anchor = CENTER)
        if userzero.Pref2 != "NA":
            userzero.MinEquiv2 = self.get_minutes(userzero.Pref2, float(userzero.Weight), userzero.Units, float(food_dict[userzero.Item.Restaurant][userzero.Item.Food][0]), exertable)
            Exer2_string = convert_time_string(userzero.MinEquiv2)
            self.ex2equivalent_label = Label(f2subb, text=Exer2_string +" "+userzero.Pref2, bg='white')
            self.ex2equivalent_label.config(font=subheadfont)
            self.ex2equivalent_label.place(in_=f2subb, relx = 0.5, rely = 0.45, anchor = CENTER)
        if userzero.Pref3 != "NA":
            userzero.MinEquiv3 = self.get_minutes(userzero.Pref3, float(userzero.Weight), userzero.Units, float(food_dict[userzero.Item.Restaurant][userzero.Item.Food][0]), exertable)
            Exer3_string = convert_time_string(userzero.MinEquiv3)
            self.ex3equivalent_label = Label(f2subb, text=Exer3_string +" "+userzero.Pref3, bg='white')
            self.ex3equivalent_label.config(font=subheadfont)
            self.ex3equivalent_label.place(in_=f2subb, relx = 0.5, rely = 0.50, anchor = CENTER)
        
        # COLUMN THREE
        # Right hand side button to show the first card.
        self.fdnext_button = Button(f2subc, text ="Show Meme Cards", bg=buttcolor, command = self.show_memes)
        self.fdnext_button.place(in_= f2subc, relx = 0.5, rely = 0.4, anchor=CENTER)

    def show_memes(self):
        if self.frame is not None:
            self.frame.destroy() # remove current frame
        self.frame = Frame(self.master, background="white", width=appwidth, height=appheight) # A
        self.frame.pack(fill=BOTH)

        exertable = self.get_exertable()
        food_dict = self.get_food_dict()

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
            minutes = int(userzero.MinEquiv1)
            minutestring=convert_time_string(userzero.MinEquiv1)
        elif self.meme_count == 2:
            exercise=exertable[userzero.Pref2][1]
            minutes = int(userzero.MinEquiv1)
            minutestring=convert_time_string(userzero.MinEquiv2)
        elif self.meme_count == 3:
            exercise=exertable[userzero.Pref3][1]
            minutes = int(userzero.MinEquiv1)
            minutestring=convert_time_string(userzero.MinEquiv3)

        # Add code to change command button based on which meme page you're on
        self.start_button = Button(f1, text ="Previous", bg=buttcolor, command = self.prev_meme)
        self.start_button.place(in_= f1, relx = 0.5, rely = 0.4, anchor=CENTER)

        # COLUMN 2 MAIN IMAGE
        startimg = get_meme_image(food_dict, food, exercise, minutes, minutestring, self.meme_count)
        self.start_image = Label(f2, image = startimg)
        self.start_image.image = startimg # Had to add this to "anchor" image - don't know why
        self.start_image.place(in_= f2, relx = 0.5, rely = 0.4, anchor=CENTER)

        # COLUMN 3 Next button
        self.start_button = Button(f3, text ="Next", bg=buttcolor, command = self.next_meme)
        self.start_button.place(in_= f3, relx = 0.5, rely = 0.4, anchor=CENTER)

    # This function is meant to determine which meme card you are currently on, correctly route back to the function if necessary on the correct meme
    def prev_meme(self):
        '''
        Sends to prior page.
        '''
        #self.frame.destroy() # Thought this might work to refresh the frame - but it only succeeds in destroying it - it doesn't come back.
        print("Memcount before=", self.meme_count)
        if self.meme_count == 1:
            print ("going to back to result")
            self.switch_to_result() # Switch back to all results
        else:
            self.meme_count -= 1
            print ("going back one page") # go back to previous page
            self.show_memes()
        print("Memecount after=",self.meme_count)

    # This function is meant to determine which meme card you are currently on, correctly route back to the function if necessary on the correct meme
    def next_meme(self):
        '''    
        Depending on which meme, will push to next meme card, or cycle back to beginning. Thanks CH!

        '''
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

        #f1 = Frame(self.frame, background="white", width=appwidth / 3, height=appheight)
        #f2 = Frame(self.frame, background="white", width=appwidth / 3, height=appheight)
        f1 = Frame(self.frame, background="white", width=appwidth, height=appheight*0.2)
        f2 = Frame(self.frame, background="white", width=appwidth, height=appheight*0.8)
        #f3 = Frame(self.frame, background="white", width=appwidth / 3, height=appheight)
        f1.pack(side=TOP)
        f2.pack(side=BOTTOM)
        #f3.pack(side=LEFT)
        # put B label in self.frame
        #self.start_label = Label(self.frame, text="PLACEHOLDER: Logo image, example meme, call to action")
        #self.start_label.pack()

        f2suba = Frame(f2, background="white", width=appwidth * 0.4, height=appheight*0.8)
        f2subb = Frame(f2, background="white", width=appwidth * 0.4, height=appheight*0.8)
        f2subc = Frame(f2, background="white", width=appwidth * 0.2, height=appheight*0.8)


        f2suba.pack(side=LEFT)
        f2subb.pack(side=LEFT)
        f2subc.pack(side=RIGHT)
        
        self.start_label1 = Label(f1, text="Learning Important Factual Equivalents\nFast Food : Activity Equivalents", font=("Helvetica", 15, 'bold'),bg="white")
        self.start_label1.place(in_= f1, relx = 0.5, rely = 0.5, anchor=CENTER)

        startimg = ImageTk.PhotoImage(Image.open(startimgpath))
        self.start_image = Label(f2suba, image = startimg)
        self.start_image.image = startimg # Had to add this to "anchor" image - don't know why
        self.start_image.place(in_= f2suba, relx = 0.5, rely = 0.4, anchor=CENTER)

        self.start_label2 = Label(f2subb, text="This program will show you\nwhat your favorite fast food\nequivalents are in terms of\nyour preferred physical activity.", bg="white")
        self.start_label2.place(in_= f2subb, relx = 0.5, rely = 0.4, anchor=CENTER)

        self.start_button = Button(f2subc, text ="Start Now", bg=buttcolor, command = self.switch_to_setexpref)
        self.start_button.place(in_= f2subc, relx = 0.5, rely = 0.4, anchor=CENTER)

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

    def prog_exit(self):
        exit()
