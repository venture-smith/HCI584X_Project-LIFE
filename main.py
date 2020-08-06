#-------------------------------------------------------------------------------
# Name:      main.py
# Purpose:   Primary program flow for LIFE Fast Food Equivalency Calculator
# Author(s): Vincent Lin
# Created:   06/10/2020
# TODO:      XXX
# Note:      Caloric burn rate by exercise source data
#               https://exceltemplate.net/weight/calorie-tracker/
#            Restaurant and food item calorie source data
#               http://fastfoodmacros.com/
#            Thanks to Professor Chris Harding, Iowa State University for
#               Guidance, Support, and Edits
#-------------------------------------------------------------------------------

# Required External Modules
from tkinter import *

# Program Modules
from app_def import App

# Initialize Window
root = Tk()
root.geometry("400x300")

# Run program loop
app = App(root)
root.mainloop()	