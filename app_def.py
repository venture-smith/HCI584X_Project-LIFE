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
    ''' Main application

    Bulk of navigation and display functions are located in this module. A handful of primary rendering functions and string conversion functions are
    in a separate module (see lookup.py)

    '''
    def __init__(self, master):

        # SETUP WINDOW
        self.master = master # Naming the master widget       	
        self.master.title("LIFE PROTOTYPE") #window title
        master.geometry(appresolution)
        self.frame = None
        self.switch_to_main() # start with main screen

        # CREATE WINDOW BAR
        # Window Bar code from: http://effbot.org/tkinterbook/menu.htm
        # create a pulldown menu, and add it to the menu bar
        menu = Menu(self.master) 
        mainmenu = Menu(menu, tearoff=0)
        menu.add_command(label="Main", command=self.switch_to_main)
        # MENU ITEM 1
        setexprefmenu = Menu(menu, tearoff=0)
        menu.add_command(label="Exercise Prefs", command=self.switch_to_setexpref)
        # MENU ITEM 2
        weigntmenu = Menu(menu, tearoff=0)
        menu.add_command(label="Set Weight", command=self.switch_to_weight)
        # MENU ITEM 3
        findfoodmenu = Menu(menu, tearoff=0)
        menu.add_command(label="Fast Food Match", command=self.switch_to_findfood)
        # MENU ITEM 4
        optionsmenu = Menu(menu, tearoff=0)
        optionsmenu.add_command(label="About LIFE", command=self.about)
        optionsmenu.add_separator()
        optionsmenu.add_command(label="Exit", command=self.prog_exit)
        menu.add_cascade(label="Options", menu=optionsmenu)
        self.master.config(menu=menu)

        # INITIALIZE VALUES
        self.fss = 0 # Set count of selected exercises - this is necessary to make sure the meme function doesn't try to show more than the number specified
        self.meme_count = 1 # Defaults the current Meme that is being displayed as the first one
        global dItem # Ensures that the Food Item is seen across all functions
        global userzero # Ensures that the current user is seen across all functions 
        dItem = Item(dRestaurant, dFood, dCalories) # Initializes the Item with the default restaurant, food, and calorie values in preferences.py
        userzero = Account(did, dLoginId, dEmail, dPassword, dFirstName, dLastName, 
                    dPref1, dPref2, dPref3, dWeight, dUnits, dItem, dMinEquiv1, dMinEquiv2, dMinEquiv3) # Initializes the current user with the default values

    def get_food_dict(self):
        '''
        
        Gets the Food table from foodfile from Preferences.py. Uses csv Dictreader to convert into an orderedred dictionary of DictReader type.
        Converts the DictReader to a nested Dictionary, with the outer Dictionary with the "Restaurant" as key, and the Food "Item" as the value.
        In the nested dictionary, the Food "Item" is the key, and each item has a tuple as the value, with the "Calories" being the first item, and the
        "Image" path being the second item. Will likely move this out to lookup.py at some point.
        
        Returns: food_dict - Dictionary

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
        
        Gets Exercise table from exfile path from Preferences.py. Uses csv Dictreader to convert into an ordered dictionary of DictReader type.
        Converts the DictReader to a Dictionary with the string value 'Exercise' as the key. The Values are tuples with the 'Multiplier' as the first 
        item, and the 'Phrase' - a shorthand version of the exercise as the second item in the list. Will likely move this to lookup.py at some point.
        
        Returns: exertable - Dictionary

        '''
        exertable = {}
        with open(exfile, 'r') as data_file:
            data = csv.DictReader(data_file, delimiter=",")
            for row in data:
                exertable.update({row["Exercise"]:[row["Multiplier"],row["Phrase"]]}) # This version assumes three columns, but the "value" is a list of two items.
        return exertable

    def get_minutes(self, req_exercise, weight, units, src_calories, exertable):
        ''' Calorie to Minutes Exercise Converter

        This function takes the calories of the food item, and converts it to the number of minutes equivalent of a specific exercise for a person of a specified weight.
        Will likely move this to the lookup.py module.

        Args:
        req_exercise: string the exercise descriptor key
        weight: integer, given units
        units: LB or KG of the given weight
        src_calories: integer, the calories of the food item
        exertable: dict, is the entire exercise weight conversion table (exercise calories burned per minute by weight)
        
        Returns:
        Minutes: Integer, the number of minutes equivalent of the specified exercise needed to equate to the number of calories in the food item

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
    
    ##########
    # STEP ONE
    ##########

    def switch_to_setexpref(self):
        ''' Select Preferred Activities

        This function shows a scrollable list of exercises/physical activities, and allows the user to select up to 3 preferred exercises.
        Stores the 3 preferred activities as Pref1, Pref2, Pref3.
        
        '''
        if self.frame is not None:
            self.frame.destroy() # remove current frame
        self.frame = Frame(self.master, background="white", width=appwidth, height=appheight) 
        self.frame.pack(fill=BOTH)
        
        # Auto Complete Code from: https://stackoverflow.com/questions/47839813/python-tkinter-autocomplete-combobox-with-like-search
        def on_keyrelease(event):
            '''


            '''
            # get text from entry
            entry_widget = event.widget.get() 
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
            '''

            Eliminates the filtered out items from the displayed sub-list and displays remaining items.
            
            '''
            # delete previous data
            listbox.delete(0, 'end')
            # sorting data 
            data = sorted(data, key=str.lower)
            # put new data
            for item in data:
                listbox.insert('end', item)

        def on_select(event):
            '''

            Event handler that assigns the clicked on item to the target variable - in this case
            assigns the preferred exercise/activity to the user class variables Pref1, Pref2, and Pref3.
            
            '''
            print('(event) previous:', event.widget.get('active')) # Diagnostic
            print('(event)  current:', event.widget.get(event.widget.curselection()))
            print('---')
            current_selection = event.widget.get(event.widget.curselection()) # Get the selected item from the widget
        
            # If this is the first time running and not reset STATE 0, look for the first empty slot to add one - indicate the slot just filled STATE X (slot just filled)
            
            if userzero.Pref1 == "NA":  # Look for the first open slot - default from first run or reset will have all Pref = "NA"
                self.fa1.set(current_selection)
                userzero.Pref1 = current_selection # Set Pref1 to what is indicated in the widget
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
        
        def reset():
            ''' Clear exercise entries

            Clears the entries back to their default state by setting them to what is in the preferences file.
            Resets the number of total possible entries (fss) to 0.

            '''
            print('reset pressed')
            userzero.Pref1 = dPref1 # Reset to default specified in preferences
            userzero.Pref2 = dPref2 
            userzero.Pref3 = dPref3
            self.fss = 0 
            self.fa1.set(userzero.Pref1)
            self.fa2.set(userzero.Pref2)
            self.fa3.set(userzero.Pref3)

        # CREATE FRAMES
        # Create two primary rows
        f1 = Frame(self.frame, background="white", width=appwidth, height=appheight*0.2)
        f2 = Frame(self.frame, background="white", width=appwidth, height=appheight*0.8)
        f1.pack(side=TOP)
        f2.pack(side=BOTTOM)

        # Create a sub-row for title and status
        f1suba = Frame(f1, background="white", width=appwidth, height=appheight*0.2*0.8)
        f1subb = Frame(f1, background=statuscolor, width=appwidth, height=appheight*0.2*0.2)
        f1suba.pack(side=TOP)
        f1subb.pack(side=BOTTOM)

        # Create sub-columns within the second row
        f2suba = Frame(f2, background="white", width=appwidth * 0.4, height=appheight*0.8)
        f2subb = Frame(f2, background="white", width=appwidth * 0.4, height=appheight*0.8)
        f2subc = Frame(f2, background="white", width=appwidth * 0.2, height=appheight*0.8)
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
        self.start_label = Label(f1suba, text="STEP 1: Choose your TOP 3 PREFERRED Physical Activites:",bg='white')
        self.start_label.config(font=headfont)
        self.start_label.place(in_= f1suba, relx = 0.5, rely = 0.5, anchor=CENTER)

        self.exer_instruct_label = Label(f2suba, text="Scroll down the list to find your activity\nof interest. Select the activity by clicking on it.\n\nTry typing the first few characters describing\nyour activity to filter the list.",justify=LEFT,bg='white')
        self.exer_instruct_label.place(in_= f2suba, relx = 0.1, rely = 0.05, anchor=NW)

        entry = tk.Entry(f2suba) # Tkinter type Entry Box
        entry.place(in_= f2suba, relx = 0.1, rely = 0.25, anchor = NW, width=220)
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

        self.exreset_button = Button(f2subb, text ="RESET", bg='white', fg ='black', command = reset)
        self.exreset_button['font'] = ('arial', 10)
        self.exreset_button.place(in_= f2subb, relx = 0.5, rely = 0.70, anchor=CENTER)

        # COLUMN 3: NEXT BUTTON
        
        self.exnext_button = Button(f2subc, text ="NEXT>", bg=buttcolor, fg =butttextcolor, command = self.switch_to_weight)
        self.exnext_button['font'] = buttonfont
        self.exnext_button.place(in_= f2subc, relx = 0.5, rely = 0.4, anchor=CENTER)

    ##########
    # STEP TWO
    ##########

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
        f1 = Frame(self.frame, background="white", width=appwidth, height=appheight*0.2)
        f2 = Frame(self.frame, background="white", width=appwidth, height=appheight*0.8)
        f1.pack(side=TOP)
        f2.pack(side=BOTTOM)

        # Create a sub-row for title and status
        f1suba = Frame(f1, background="white", width=appwidth, height=appheight*0.2*0.8)
        f1subb = Frame(f1, background=statuscolor, width=appwidth, height=appheight*0.2*0.2)
        f1suba.pack(side=TOP)
        f1subb.pack(side=BOTTOM)

        # Create sub-columns within the second row
        f2suba = Frame(f2, background="white", width=appwidth * 0.2, height=appheight*0.8) # Use a multiplier in app width to allocate column width
        f2subb = Frame(f2, background="white", width=appwidth * 0.4, height=appheight*0.8)
        f2subc = Frame(f2, background="white", width=appwidth * 0.2, height=appheight*0.8)
        f2subd = Frame(f2, background="white", width=appwidth * 0.2, height=appheight*0.8)
        f2suba.pack(side=LEFT)
        f2subb.pack(side=LEFT)
        f2subc.pack(side=LEFT)
        f2subd.pack(side=LEFT)

        # HEADING
        self.weight_label = Label(f1suba, text="STEP 2: ENTER YOUR WEIGHT (in Pounds or Kilograms):",bg='white')
        self.weight_label.config(font=headfont)
        self.weight_label.place(in_= f1suba, relx = 0.5, rely = 0.5, anchor=CENTER)
        
        # COLUMN 1
        self.back_button = Button(f2suba, text ="<BACK", bg=buttcolor, fg=butttextcolor, command = self.switch_to_setexpref)
        self.back_button['font'] = buttonfont
        self.back_button.place(in_= f2suba, relx = 0.5, rely = 0.4, anchor=CENTER)
        
        # COLUMN 2
        self.start_fact = Label(f2subb, text="DID YOU KNOW\nthat the average American male\nweighs 197 pounds?\n\nThe average American female\n weighs 157 pounds.", bg='white')
        self.start_fact.config(font=subheadfont)
        self.start_fact.place(in_=f2subb, relx = 0.5, rely = 0.15, anchor = CENTER)

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
        R1 = Radiobutton(f2subc, text="Pounds/Lbs.", bg='white', variable=self.uvar, value="LB",
                        command=unit_sel)
        R1.place(in_=f2subc, relx = 0.1, rely = 0.35, anchor = NW )

        R2 = Radiobutton(f2subc, text="Kilograms/Kgs.", bg='white', variable=self.uvar, value="KG",
                        command=unit_sel)
        R2.place(in_=f2subc, relx = 0.1, rely = 0.40, anchor = NW )

        # Next button
        self.wtnext_button = Button(f2subd, text ="NEXT>", bg=buttcolor, fg=butttextcolor, command = self.switch_to_findfood)
        self.wtnext_button['font'] = buttonfont
        self.wtnext_button.place(in_= f2subd, relx = 0.5, rely = 0.4, anchor=CENTER)

    def switch_to_findfood(self):
        ''' Select Fast Food Restaurant & Item

        This function allows the user to select a fast food restaurant among a few popular chains, and then select from a limited set of popular menu items.
        The function also checks to see if the user has entered a value for each step before allowing the user to see the summary and the Meme Cards.

        '''
        if self.frame is not None:
            self.frame.destroy() # remove current frame
        self.frame = Frame(self.master, background="white", width=appwidth, height=appheight) 
        self.frame.pack(side = LEFT, fill= Y)

        # Initialize Variables
        self.meme_count = 1 # Reset current meme to 1
        self.errorstring = StringVar()
        #foodnextbuttcolor = 'gray33' # Try "chartreuse2", "green2", "green yellow"
        #foodnextbutttextcolor = 'gray75'

        # CREATE FRAMES
        # Create two primary rows
        f1 = Frame(self.frame, background="white", width=appwidth, height=appheight*0.2) # The multiplier for height added should equal 1.
        f2 = Frame(self.frame, background="white", width=appwidth, height=appheight*0.8)
        f1.pack(side=TOP)
        f2.pack(side=BOTTOM)

        # Create a sub-row for title and status
        f1suba = Frame(f1, background="white", width=appwidth, height=appheight*0.2*0.8) # Multiplier added equals 1, but a fraction of the original row
        f1subb = Frame(f1, background=statuscolor, width=appwidth, height=appheight*0.2*0.2)
        f1suba.pack(side=TOP)
        f1subb.pack(side=BOTTOM)

        # Error String - this is where the error message appears
        self.f1subb_label = Label(f1subb, textvariable = self.errorstring, bg = statuscolor)
        self.f1subb_label.place(in_= f1subb, relx = 0.5, rely = 0.5, anchor=CENTER)

        # Create columns within the second row
        f2suba = Frame(f2, background="white", width=appwidth * 0.2, height=appheight*0.8) # Use a multiplier in app width to allocate column width (must equal 1)
        f2subb = Frame(f2, background="white", width=appwidth * 0.3, height=appheight*0.8)
        f2subc = Frame(f2, background="white", width=appwidth * 0.3, height=appheight*0.8)
        f2subd = Frame(f2, background="white", width=appwidth * 0.2, height=appheight*0.8)
        f2suba.pack(side=LEFT)
        f2subb.pack(side=LEFT)
        f2subc.pack(side=LEFT)
        f2subd.pack(side=LEFT)

        def foodbox_update(data):
            '''

            Eliminates filtered items from the list and re-sorts.

            '''
            # delete previous data
            foodbox.delete(0, 'end')
            # sorting data 
            data = sorted(data, key=str.lower)
            # put new data
            for item in data:
                foodbox.insert('end', item)

        def ron_select(event):
            '''
            
            Registers the restaurant and filters and feeds the food item list 

            '''
            # 
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

            Registers the Food item selection from list is saved to the set of user variables
            
            '''
            fcurrent_selection = fevent.widget.get(fevent.widget.curselection())
            userzero.Item.Food = fcurrent_selection
            precheck() # update the button color if the completion conditions are met
            print ("Food Selected:",userzero.Item.Food) # DIAGNOSTIC
        
        def precheck():
            ''' 
            
            Check to see if all conditions are met to show meme results, show error in status bar.

            '''
            if (userzero.Item.Food == "") or (userzero.Pref1 == "NA"): 
                fdnext_Button_Color = 'gray33'
                fdnext_ButtonText_Color = 'gray75'
            else:
                fdnext_Button_Color = 'dark green' # Try "chartreuse2", "green2", "green yellow"
                fdnext_ButtonText_Color = 'white'
            self.fdnext_button.configure(bg = fdnext_Button_Color, fg=fdnext_ButtonText_Color)

        def checkcomplete():
            ''' 
            
            Check to see if all conditions are met to show meme results, show error in status bar.

            '''
            errstring = "" # Clear errorstring
            self.errorstring.set(errstring) 
            error = 0
            if userzero.Item.Food == "":
                errstring = errstring + "No food item selected. Please select a food item. "
                print("ERROR: NO FOOD ITEM SELECTED")
                error = 1
            if userzero.Pref1 == "NA":
                errstring = errstring + "No activity selected. Please select at least one activity. "
                print("ERROR: NO ACTIVITY SELECTED")
                error = 1    
            if (userzero.Units == "LB") and ((userzero.Weight < 50) or (userzero.Weight > 500)):
                errstring = errstring + "Weight out of bounds. Please adjust weight (50 - 500 LBS)."
                print("ERROR: OUT OF LB TOLERANCE")
                error = 1 
            if (userzero.Units == "KG") and ((userzero.Weight < 25) or (userzero.Weight > 250)):
                errstring = errstring + "Weight out of bounds. Please adjust weight (25 - 250 KGS)."
                print("ERROR: OUT OF KG TOLERANCE")
                error = 1 
            if error == 1: 
                self.errorstring.set(errstring) 
            else:
                self.switch_to_result()
        
        # Pull restaurant list from Food Dictionary for use in Selection List
        restaurant_list = []
        food_dict = self.get_food_dict() # Retrieve Food dictionary
        restaurant_list = list(food_dict) # Convert dictionary to just a list of restaurants for use in the first selection list
        
        self.weight_label = Label(f1suba, text="STEP 3: SELECT A RESTAURANT AND FOOD ITEM/ENTREE",bg='white')
        self.weight_label.config(font=headfont)
        self.weight_label.place(in_= f1suba, relx = 0.5, rely = 0.5, anchor=CENTER)

        # COLUMN 1
        self.back_button = Button(f2suba, text ="<BACK", bg=buttcolor, fg=butttextcolor, command = self.switch_to_weight)
        self.back_button['font'] = buttonfont
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
        self.fdnext_button = Button(f2subd, text ="NEXT>", bg=fdnext_Button_Color, fg=fdnext_ButtonText_Color, command = checkcomplete)
        self.fdnext_button['font'] = buttonfont
        #self.fdnext_button = Button(f2subd, text ="Next", bg=buttcolor, command = self.switch_to_result)
        self.fdnext_button.place(in_= f2subd, relx = 0.5, rely = 0.4, anchor=CENTER)

        precheck() # Check to see if the conditions are met, if so change the next button color


    def switch_to_result(self):
        ''' Show Summary Results

        This function was originally created as a diagnostic to make sure the data was correctly being passed. It now shows
        basic data of what was selected and what equivalents there are to each food to exercise.

        '''
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
        f1 = Frame(self.frame, background="white", width=appwidth, height=appheight*0.2)
        f2 = Frame(self.frame, background="white", width=appwidth, height=appheight*0.8)
        f1.pack(side=TOP)
        f2.pack(side=BOTTOM)

        # Create a sub-row for title and status
        f1suba = Frame(f1, background="white", width=appwidth, height=appheight*0.2*0.8)
        f1subb = Frame(f1, background=statuscolor, width=appwidth, height=appheight*0.2*0.2)
        f1suba.pack(side=TOP)
        f1subb.pack(side=BOTTOM)

        # Create columns within the second row
        f2suba = Frame(f2, background="white", width=appwidth * 0.2, height=appheight*0.8) # Use a multiplier in app width to allocate column width
        f2subb = Frame(f2, background="white", width=appwidth * 0.6, height=appheight*0.8)
        f2subc = Frame(f2, background="white", width=appwidth * 0.2, height=appheight*0.8)
        f2suba.pack(side=LEFT)
        f2subb.pack(side=LEFT)
        f2subc.pack(side=LEFT)

        self.weight_label = Label(f1suba, text="STEP 4: REVIEW RESULT SUMMARY",bg='white')
        self.weight_label.config(font=headfont)
        self.weight_label.place(in_= f1suba, relx = 0.5, rely = 0.5, anchor=CENTER)

        # COLUMN ONE
        self.back_button = Button(f2suba, text ="<BACK", bg=buttcolor, fg=butttextcolor, command = self.switch_to_findfood)
        self.back_button['font'] = buttonfont
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
        self.fdnext_button = Button(f2subc, text ="SHOW>", bg=buttcolor, fg=butttextcolor, command = self.show_memes)
        self.fdnext_button['font'] = buttonfont
        self.fdnext_button.place(in_= f2subc, relx = 0.5, rely = 0.4, anchor=CENTER)

    def show_memes(self):
        ''' Display Meme Cards

        This function is the page that shows each MemeCard. It formats the page and calls the MemeCard renderer. Future version will allow
        you change the font, font color, and to save out or share the MemeCard.

        '''
        if self.frame is not None:
            self.frame.destroy() # remove current frame
        self.frame = Frame(self.master, background="white", width=appwidth, height=appheight) # A
        self.frame.pack(fill=BOTH)

        exertable = self.get_exertable()
        food_dict = self.get_food_dict()

        print("--Showing Memes--")

        # Create two primary rows
        f1 = Frame(self.frame, background="white", width=appwidth, height=appheight*0.2)
        f2 = Frame(self.frame, background="white", width=appwidth, height=appheight*0.8)
        f1.pack(side=TOP)
        f2.pack(side=BOTTOM)

        # Create a sub-row for title and status
        f1suba = Frame(f1, background="white", width=appwidth, height=appheight*0.2*0.8)
        f1subb = Frame(f1, background=statuscolor, width=appwidth, height=appheight*0.2*0.2)
        f1suba.pack(side=TOP)
        f1subb.pack(side=BOTTOM)

        f2suba = Frame(f2, background="white", width=appwidth * 0.2, height=appheight*0.8)
        f2subb = Frame(f2, background="white", width=appwidth * 0.6, height=appheight*0.8)
        f2subc = Frame(f2, background="white", width=appwidth * 0.2, height=appheight*0.8)
        f2suba.pack(side=LEFT)
        f2subb.pack(side=LEFT)
        f2subc.pack(side=LEFT)
        
        food=userzero.Item
        if self.meme_count == 1: # Depending on which meme currently being shown, set the exercise and minutes string to the correct one. 
            exercise=exertable[userzero.Pref1][1]
            minutes = int(userzero.MinEquiv1)
            minutestring=convert_time_string(userzero.MinEquiv1)
            prevtext = "<Results"
            if self.fss > 1:
                nexttext = "See Card #2>"
            else:
                nexttext = "Start over"
        elif self.meme_count == 2:
            exercise=exertable[userzero.Pref2][1]
            minutes = int(userzero.MinEquiv1)
            minutestring=convert_time_string(userzero.MinEquiv2)
            prevtext = "<See Card #1"
            if self.fss > 2:
                nexttext = "See Card #3>"
            else:
                nexttext = "Start over"
        elif self.meme_count == 3:
            exercise=exertable[userzero.Pref3][1]
            minutes = int(userzero.MinEquiv1)
            minutestring=convert_time_string(userzero.MinEquiv3)
            prevtext = "<See Card #2"
            nexttext = "Start over"

        self.memecard_label = Label(f1suba, text="MEME CARD #"+str(self.meme_count)+":",bg='white')
        self.memecard_label.config(font=headfont)
        self.memecard_label.place(in_= f1suba, relx = 0.5, rely = 0.5, anchor=CENTER)

        self.memecardb_label = Label(f1suba, text=food.getFood() + " : " + exercise,bg='white')
        self.memecardb_label.config(font=headfont)
        self.memecardb_label.place(in_= f1suba, relx = 0.5, rely = 0.75, anchor=CENTER)

        # Add code to change command button based on which meme page you're on
        self.prev_button = Button(f2suba, text =prevtext, bg=buttcolor, fg=butttextcolor, command = self.prev_meme)
        self.prev_button['font'] = buttonfont
        self.prev_button.place(in_= f2suba, relx = 0.5, rely = 0.4, anchor=CENTER)

        # COLUMN 2 MAIN IMAGE
        startimg = get_meme_image(food_dict, food, exercise, minutes, minutestring, self.meme_count)
        self.start_image = Label(f2subb, image = startimg)
        self.start_image.image = startimg # Had to add this to "anchor" image - don't know why
        self.start_image.place(in_= f2subb, relx = 0.5, rely = 0.5, anchor=CENTER)

        # COLUMN 3 Next button
        self.next_button = Button(f2subc, text =nexttext, bg=buttcolor, fg=butttextcolor, command = self.next_meme)
        self.next_button['font'] = buttonfont
        self.next_button.place(in_= f2subc, relx = 0.5, rely = 0.4, anchor=CENTER)

    # This function is meant to determine which meme card you are currently on, correctly route back to the function if necessary on the correct meme
    def prev_meme(self):
        '''
        
        This function is meant to determine which meme card you are currently on, correctly route back to the function if necessary on the correct meme or
        send to prior Results page.
        
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

    def next_meme(self):
        '''    
        
        This function is meant to determine which meme card you are currently on, correctly route back to the function if necessary on the correct meme.
        Depending on which meme, will push to next meme card, or cycle back to beginning. Thanks CH!

        '''
        self.meme_count += 1
        if (self.meme_count > 3) or (self.meme_count > self.fss):
            self.meme_count == 1
            self.switch_to_main()
        else:
            self.show_memes()

    def switch_to_main(self):
        ''' Main Page

        This page is the first page of the program. It explains the purpose of the program and shows an example of the output.

        '''
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
        
        self.start_label1 = Label(f1, text="Learning Important Factual Equivalents\nFast Food Items : Time Spent on Physical Activity", font=("Helvetica", 15, 'bold'),bg="white")
        self.start_label1.place(in_= f1, relx = 0.5, rely = 0.5, anchor=CENTER)

        startimg = ImageTk.PhotoImage(Image.open(startimgpath))
        self.start_image = Label(f2suba, image = startimg)
        self.start_image.image = startimg # Had to add this to "anchor" image - don't know why
        self.start_image.place(in_= f2suba, relx = 0.5, rely = 0.4, anchor=CENTER)

        self.start_label2 = Label(f2subb, text="This program will show you\nwhat your favorite fast food\nequivalents are in terms of\nyour preferred physical activity.", bg="white")
        self.start_label2.place(in_= f2subb, relx = 0.5, rely = 0.4, anchor=CENTER)

        self.start_button = Button(f2subc, text ="Start Now >", bg=buttcolor, fg=butttextcolor, command = self.switch_to_setexpref)
        self.start_button['font'] = buttonfont
        self.start_button.place(in_= f2subc, relx = 0.5, rely = 0.4, anchor=CENTER)

    #About
    def about(self):
        '''

        Shows name of the program, contact information, and version information.

        '''
        if self.frame is not None:
            self.frame.destroy() # remove current frame
        self.frame = Frame(self.master, background="white", width=300, height=100) # A
        self.frame.pack(fill=BOTH)

        # put B label in self.frame
        self.start_label = Label(self.frame, text="ABOUT LIFE: A fastfood, exercise meme generator")
        self.start_label.pack()

    def donothing(self):
        '''
        
        A stub for further expansion/adding functions

        '''
        msgbox.showinfo(title='DO NOTHING', message='PLACEHOLDER')

    def prog_exit(self):
        ''' End program

        A function to end the program

        '''
        exit()
