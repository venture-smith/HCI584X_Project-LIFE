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
# May need a math module here


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

#initialize application window
# Creating Application Window using tkinter Frame class
class AppWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master) # Parameters sent through frame class
        self.master = master # Naming the master widgit
        self.init_window()
    def init_window(self):        	
        self.master.title("LIFE PROTOTYPE") #window title
        self.pack(fill=BOTH, expand=1) #sizing the main widgit
        # Create menu bar
        menu = Menu(self.master) 


        # CH this is copy/pasted from here: http://effbot.org/tkinterbook/menu.htm
        # create a pulldown menu, and add it to the menu bar
        filemenu = Menu(menu, tearoff=0)
        filemenu.add_command(label="Open", command=self.donothing)
        filemenu.add_command(label="Save", command=self.donothing)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menu.add_cascade(label="File", menu=filemenu)

        # create more pulldown menus
        editmenu = Menu(menu, tearoff=0)
        editmenu.add_command(label="Cut", command=self.donothing)
        editmenu.add_command(label="Copy", command=self.donothing)
        editmenu.add_command(label="Paste", command=self.donothing)
        menu.add_cascade(label="Edit", menu=editmenu)

        helpmenu = Menu(menu, tearoff=0)
        helpmenu.add_command(label="About", command=self.donothing)
        menu.add_cascade(label="Help", menu=helpmenu)
        '''
        # Option 1: USER LOGIN        
        loginmenu = Menu(menu)
        menu.add_cascade(label = "Login",command  = self.donothing)
        # Option 2: USER SIGN UP
        signupmenu = Menu(menu)
        menu.add_cascade(label = "Sign up",command = self.donothing)
        # Option 3: FIND FOODS
        # Option 4: OPTIONS
        optionsmenu = Menu(menu)
        menu.add_cascade(label = "Options",menu = optionsmenu)
        optionsmenu.add_command(label = "About LIFE",command = self.about())
        optionsmenu.add_command(label = "Preferences",command = self.donothing())
        optionsmenu.add_command(label = "Account settings",command = self.donothing())
        optionsmenu.add_command(label = "Logout",command = self.donothing())
        '''
        self.master.config(menu=menu)

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
    #About
    def about(self):
        msgbox.showinfo(title='LIFE', message='Learning Important Factual Equivalents: Calorie Edition')
    #Landing/Intro page with rotating content     
    def mainscreen(self):
        top_frame = tk.Frame(AppWindow, background="#FFF0C1",bd=1)
        bottom_frame = tk.Frame(AppWindow, background="#FFF0C1",bd=1)

        top_frame.grid(row=0, column=0)
        bottom_Frame.grid(row=1, column=0)
    #Login placeholder
    #Restaurant/Food Item Search Page placeholder
    #Preferences Page placeholder
    def prog_exit(self):
        exit()
        #Labels

root = Tk()
root.geometry("400x300")
app = AppWindow(root)
root.mainloop()	