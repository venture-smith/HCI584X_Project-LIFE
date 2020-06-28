  
import tkinter as tk 
from tkinter import ttk 
from lookup import *
   
fname="HCI584X_Project-LIFE\exercise.csv"
exercise="Water polo" # CREATE A FUNCTION TO SELECT/RANK TOP 3 ACTIVITIES
weight=200
src_calories=550
exertable=pull_csv(fname,',') #initialize exercise table from CSV file
dict_list = []
for lines in exertable:
    dict_list.append(lines['Exercise'])

# python program demonstrating 
# Combobox widget using tkinter 
  

  
# Creating tkinter window 
window = tk.Tk() 
window.title('Combobox') 
window.geometry('500x250') 
  
# label text for title 
#ttk.Label(window, text = "GFG Combobox Widget",  
#          background = 'green', foreground ="white",  
#          font = ("Times New Roman", 15)).grid(row = 0, column = 1) 
  
# label 
ttk.Label(window, text = "Select the Month :", 
          font = ("Times New Roman", 10)).grid(column = 0, 
          row = 5, padx = 10, pady = 25) 
  
# Combobox creation 
n = tk.StringVar() 
monthchoosen = ttk.Combobox(window, width = 27, textvariable = n) 
  
# Adding combobox drop down list 
monthchoosen['values'] = (' January',  
                          ' February', 
                          ' March', 
                          ' April', 
                          ' May', 
                          ' June', 
                          ' July', 
                          ' August', 
                          ' September', 
                          ' October', 
                          ' November', 
                          ' December') 
  
monthchoosen.grid(column = 1, row = 5) 
monthchoosen.current() 
window.mainloop() 