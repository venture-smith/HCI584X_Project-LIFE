#-------------------------------------------------------------------------------
# Name:      main.py
# Purpose:   Primary program flow for LIFE webapp
# Author(s): Vincent Lin
# Created:   06/10/2020
# TODO:      XXX YYY ZZZ
# Note:      Need to pull in data from this: https://exceltemplate.net/weight/calorie-tracker/
#-------------------------------------------------------------------------------

###### 1. IMPORT MODULES

# Using Tkinter to create a window to display application, will investigate creating a web app 
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.scrolledtext as tkst
import sqlite3
from tkinter import messagebox as msgbox
# May not need this module - imported from a different application.
import fileinput
from lookup import *

# Preferences
from preferences import *

###### 2. SET UP DATA STRUCTURES
# Data Hierarchy - Account - User - Preferences - Transaction history
def write_to_csv(accountfile,u_name):
    with open(accountfile, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([u_name])

class Account:
    # Create user account
    def __init__(self, id, LoginId, Email, Password, FirstName, LastName):
        self.id = id
        self.LoginId = LoginId
        self.Email = Email
        self.Password = Password
        self.FirstName = FirstName
        self.Lastname = LastName
 
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

# Application class 
class App(object):
    def __init__(self, master):

        self.master = master # Naming the master widget       	
        self.master.title("LIFE PROTOTYPE") #window title

        self.frame = None
        self.switch_to_main() # start with frame "A" Main

        # Create menu bar
        menu = Menu(self.master) 
        # CH this is copy/pasted from here: http://effbot.org/tkinterbook/menu.htm
        # create a pulldown menu, and add it to the menu bar
        mainmenu = Menu(menu, tearoff=0)
        #menu.add_cascade(label="Main", menu=mainmenu)
        menu.add_command(label="Main", command=self.switch_to_main)
        #mainmenu.add_command(label="Exit", command=root.quit)

        signupmenu = Menu(menu, tearoff=0)
        #menu.add_cascade(label="Signup", menu=signupmenu)
        menu.add_command(label="Signup", command=self.switch_to_signup)

        setexprefmenu = Menu(menu, tearoff=0)
        menu.add_command(label="Exercise Prefs", command=self.switch_to_setexpref)

        findfoodmenu = Menu(menu, tearoff=0)
        menu.add_command(label="Fast Food Match", command=self.switch_to_findfood)

        optionsmenu = Menu(menu, tearoff=0)
        optionsmenu.add_command(label="About LIFE", command=self.about)
        #optionsmenu.add_command(label="Change password", command=self.switch_to_main)
        optionsmenu.add_separator()
        optionsmenu.add_command(label="Logout", command=self.switch_to_C)

        menu.add_cascade(label="Options", menu=optionsmenu)

        self.master.config(menu=menu)

    # Based on https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter#:~:text=One%20way%20to%20switch%20frames,use%20any%20generic%20Frame%20class.
    def switch_to_signup(self):
        if self.frame is not None:
            self.frame.destroy() # remove current frame
        self.frame = Frame(self.master, background="white", width=100, height=300) # B
        self.frame.pack(fill=BOTH)

        global u_name
        global f_name
        global l_name
        global email
        global pw

        u_name = Entry(self.frame, width=30)
        u_name.grid(row=0, column=1, padx=20)
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
        self.frame = Frame(self.master, background="white", width=100, height=300) # C
        self.frame.pack(fill=BOTH)
        write_to_csv(accountfile, u_name) 
        # put C label in self.frame
        self.start_label = Label(self.frame, text="Submitted")
        self.start_label.pack()

    def switch_to_setexpref(self):
        if self.frame is not None:
            self.frame.destroy() # remove current frame
        self.frame = Frame(self.master, background="white", width=100, height=300) # C
        self.frame.pack(fill=BOTH)

        # Auto Complete Code from: https://stackoverflow.com/questions/47839813/python-tkinter-autocomplete-combobox-with-like-search
        def on_keyrelease(event):

            # get text from entry
            value = event.widget.get()
            value = value.strip().lower()

            # get data from test_list
            if value == '':
                data = test_list
            else:
                data = []
                for item in test_list:
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

        # Add sub-frames
        f1 = Frame(self.frame, background="white")
        f2 = Frame(self.frame, background="white")
        #f3 = Frame(self.frame, background="white")
        #f4 = Frame(self.frame, background="white")
        f1.pack(side=LEFT)
        f2.pack(side=LEFT)
        #f3.pack(side=LEFT)
        #f4.pack(side=LEFT)
        # Add sub-sub-frames
        f1suba = Frame(f1, background="white")
        f1subb = Frame(f1, background="white")
        f1suba.pack(side=TOP, padx=20, pady=20)
        f1subb.pack(side=BOTTOM)
        f2suba = Frame(f2, background="white")
        f2subb = Frame(f2, background="white")
        f2suba.pack(side=TOP)
        f2subb.pack(side=BOTTOM)


        #initialize exercise table from CSV file
        exertable=pull_csv(fname,',') 
        dict_list = [] # Create list for dictionary
        for lines in exertable:
            dict_list.append(lines['Exercise'])
        #test_list = ('apple', 'banana', 'Cranberry', 'dogwood', 'alpha', 'Acorn', 'Anise', 'Strawberry' )
        test_list = dict_list

        #root = tk.Tk()
        # put C label in self.frame
        self.start_label = Label(f1suba, text="Choose your top 3\n Physical Activites:")
        self.start_label.pack(side = LEFT, expand = False)

        #selectstring = "#1 Selected activity" + event.widget.get('active')
        #self.selected_label = Label(self.frame, text=selectstring)
        #self.selected_label.pack(side = RIGHT, expand = False)

        listbox = tk.Listbox(f1subb)
        listbox.pack(side = LEFT, expand = True, fill = Y)
        #listbox.bind('<Double-Button-1>', on_select)
        listbox.bind('<<ListboxSelect>>', on_select)
        listbox_update(test_list)

        entry = tk.Entry(f2suba) # Tkinter type Entry Box
        entry.pack(side = LEFT, expand = True, fill = Y)
        entry.bind('<KeyRelease>', on_keyrelease)

        self.start_button = Button(f2subb, text ="Select", command = self.switch_to_setexpref)
        self.start_button.pack(padx=20, pady=20)

    def switch_to_findfood(self):
        if self.frame is not None:
            self.frame.destroy() # remove current frame
        self.frame = Frame(self.master, background="white", width=100, height=300) # C
        self.frame.pack(side = LEFT, fill= Y)

        # put C label in self.frame
        self.start_label = Label(self.frame, text="Find Fast Food")
        self.start_label.pack()

    def switch_to_C(self):
        if self.frame is not None:
            self.frame.destroy() # remove current frame
        self.frame = Frame(self.master, background="white", width=100, height=300) # C
        self.frame.pack(fill=BOTH)

        # put C label in self.frame
        self.start_label = Label(self.frame, text="Frame C")
        self.start_label.pack()

    def switch_to_main(self):
        if self.frame is not None:
            self.frame.destroy() # remove current frame
        self.frame = Frame(self.master, background="white", width=300, height=300) # A
        self.frame.pack(fill=BOTH)

        f1 = Frame(self.frame, background="white")
        f2 = Frame(self.frame, background="white")
        f1.pack(side=LEFT)
        f2.pack(side=RIGHT)
        # put B label in self.frame
        #self.start_label = Label(self.frame, text="PLACEHOLDER: Logo image, example meme, call to action")
        #self.start_label.pack()

        self.start_label = Label(f1, text="This program will show you\nwhat your favorite fast food\nequivalents are in terms of\nyour preferred physical activity.", bg="white")
        self.start_label.pack(padx=20, pady=20)

        self.start_button = Button(f2, text ="Start Now", command = self.switch_to_setexpref)
        self.start_button.pack(padx=20, pady=20)

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

    # NOTE - Implement Different "Pages"
  
    #Login placeholder
    #Restaurant/Food Item Search Page placeholder
    #Preferences Page placeholder

    def prog_exit(self):
        exit()
        #Labels

root = Tk()
root.geometry("400x300")
app = App(root)
root.mainloop()	