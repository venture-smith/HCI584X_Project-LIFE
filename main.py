#-------------------------------------------------------------------------------
# Name:      main.py
# Purpose:   Primary program flow for LIFE webapp
# Author(s): Vincent Lin
# Created:   06/10/2020
# TODO:      XXX YYY ZZZ
# Note:      More on this later
#-------------------------------------------------------------------------------

###### 1. IMPORT MODULES

# Using Tkinter to create a window to displaya application, will investigate creating a web app 
from tkinter import filedialog
from tkinter import simpledialog
import tkinter as tk
import tkinter.scrolledtext as tkst
from tkinter import messagebox as msgbox
# May not need this module - imported from a different application.
import fileinput
# May need a math module here


###### 2. SET UP DATA STRUCTURES
# Data Heirarchy - Account - User - Preferences - Transaction history

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
 
class AppWindow:
	#initialize application window
	def __init__(self,rt):
		if rt == None:
			self.t = tk.Tk() # This creates the window
		else:
			self.t = tk.Toplevel(rt)
			
		self.t.title("LIFE PROTOTYPE")
		self.bar = tk.Menu(rt)

		self.loginmenu = tk.Menu(self.bar, tearoff=0) #Setup login option
		self.loginmenu.add_command(label = "Placeholder",command = self.donothing)
        
		self.signupmenu = tk.Menu(self.bar, tearoff=0)
		self.signupmenu.add_command(label = "Sign up",command = self.donothing)
		
		self.optionsmenu = tk.Menu(self.bar, tearoff=0)
		self.optionsmenu.add_command(label = "About LIFE",command = self.about)
		self.optionsmenu.add_command(label = "Options",command = self.donothing)

		self.bar.add_cascade(label = "Login",menu = self.loginmenu)
		self.bar.add_cascade(label = "Sign up",menu = self.signupmenu)
		self.bar.add_cascade(label = "Options",menu = self.optionsmenu)
    
		self.t.config(menu = self.bar)

		self.f = tk.Frame(self.t,width = 512)
		self.f.pack(expand =1)

		self.texteditor = tkst.ScrolledText(self.t)
		self.texteditor.pack(expand = 1)
	
    #Close AppWindow
	def close(self):
		self.t.destroy()

	#Do nothing Placeholder
	def donothing(self):
		msgbox.showinfo(title='DO NOTHING', message='PLACEHOLDER')

	#About
	def about(self):
		msgbox.showinfo(title='LIFE', message='Learning Important Factual Equivalents: Calorie Edition')
		
if __name__ == "__main__": # Not sure what this is doing
	app = []
	root = None
	app.append(AppWindow(root))
	root = app[0].t
	root.mainloop() # This is the main loop

# 3. Set up modules / functions
