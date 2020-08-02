#-------------------------------------------------------------------------------
# Name:      main.py
# Purpose:   Primary program flow for LIFE webapp
# Author(s): Vincent Lin
# Created:   06/10/2020
# TODO:      XXX YYY ZZZ
# Note:      Caloric burn rate by exercise source data
#               https://exceltemplate.net/weight/calorie-tracker/
#            Restaurant and food item calorie source data
#               http://fastfoodmacros.com/
#-------------------------------------------------------------------------------

###### 1. IMPORT MODULES

# Required External Modules
from tkinter import filedialog # Using Tkinter to create a window to display application, will investigate creating a web app 
from tkinter import simpledialog
from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.scrolledtext as tkst
from tkinter import messagebox as msgbox
from PIL import ImageTk, Image # Using Pillow to composite and render images and handle text overlays.

# Program Modules
from app_def import App
from account_class import Account

# Preferences
from preferences import *

# Initialize Window
root = Tk()
root.geometry("400x300")

# Run program loop
app = App(root)
root.mainloop()	