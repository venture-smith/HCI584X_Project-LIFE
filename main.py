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


###### 2. SET UP DATA STRUCTURES
# Data Hierarchy - Account - User - Preferences - Transaction history

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
        menu.add_command(label="Signup", command=self.switch_to_B)

        setexprefmenu = Menu(menu, tearoff=0)
        menu.add_command(label="Exercise Prefs", command=self.switch_to_B)

        findfoodmenu = Menu(menu, tearoff=0)
        menu.add_command(label="Fast Food Match", command=self.switch_to_B)

        optionsmenu = Menu(menu, tearoff=0)
        optionsmenu.add_command(label="About LIFE", command=self.about)
        optionsmenu.add_command(label="Set preferences", command=self.switch_to_B)
        optionsmenu.add_separator()
        optionsmenu.add_command(label="Logout", command=self.switch_to_C)

        menu.add_cascade(label="Options", menu=optionsmenu)

        self.master.config(menu=menu)

    # Based on https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter#:~:text=One%20way%20to%20switch%20frames,use%20any%20generic%20Frame%20class.
    def switch_to_B(self):
        if self.frame is not None:
            self.frame.destroy() # remove current frame
        self.frame = Frame(self.master, background="white", width=100, height=300) # B
        self.frame.pack(fill=BOTH)

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

        # put B label in self.frame
        self.start_label = Label(self.frame, text="Frame B")
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

        # put B label in self.frame
        self.start_label = Label(self.frame, text="PLACEHOLDER: Logo image, example meme, call to action")

        self.start_label.pack()

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