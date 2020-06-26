from tkinter import *
from lookup import *
   
fname="HCI584X_Project-LIFE\exercise.csv"
exercise="Water polo" # CREATE A FUNCTION TO SELECT/RANK TOP 3 ACTIVITIES
weight=200
src_calories=550
exertable=pull_csv(fname,',') #initialize exercise table from CSV file
dict_list = []
for line in exertable:
    dict_list.append(line)

# Function for checking the 
# key pressed and updating 
# the listbox 
def checkkey(event): 
       
    value = event.widget.get() 
    print(value) 
      
    # get data from l 
    if value == '': 
        data = l 
    else: 
        data = [] 
        for item in l: 
            if value.lower() in item.lower(): 
                data.append(item)                 
   
    # update data in listbox 
    update(data) 
   
   
def update(data): 
      
    # clear previous data 
    lb.delete(0, 'end') 
   
    # put new data 
    for item in data: 
        lb.insert('end', item) 
  
  
# Driver code 
l = dict_list.items()
#l = ('C','C++','Java', 
#     'Python','Perl', 
#     'PHP','ASP','JS' ) 
  
root = Tk() 
  
#creating text box  
e = Entry(root) 
e.pack() 
e.bind('<KeyRelease>', checkkey) 
  
#creating list box 
lb = Listbox(root) 
lb.pack() 
update(l) 
   
root.mainloop() 