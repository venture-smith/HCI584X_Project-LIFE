#-------------------------------------------------------------------------------
# Name:      lookup.py
# Purpose:   Primary program flow for LIFE webapp
# Author(s): Vincent Lin
# Created:   06/10/2020
# TODO:      XXX YYY ZZZ
# Note:      This function looks up the multiplier to be used in the calculation
#-------------------------------------------------------------------------------

# importing module  
from preferences import * 
import csv 

def pull_csv(file, delimiter=','):
    if not delimiter:
        delimiter = ','   # why not set delimiter=',' in function header (instead None?)
    readexertable = csv.DictReader(open(file), delimiter=delimiter)
    return readexertable

def convert_time_string(minutes):
    time_s = ""
    hours = minutes / 60
    rhours = minutes // 60
    mhours = minutes%60
    days = hours / 24
    rdays = hours // 24
    mdays = hours%24

    if days > 2:
        if mdays == 0:
            time_s = (str(int(rdays))+" days ")
        elif mhours == 0:
            time_s = (str(int(rdays))+" days " + str(int(rhours))+" hours ")        
        else:
            time_s = (str(int(rdays))+" days " + str(int(mdays))+" hours "+str(int(mhours))+" minutes")
    elif hours > 2:
        if mhours == 0:
            time_s = (str(int(rhours))+" hours ")
        else:
            time_s = (str(int(rhours))+" hours "+str(int(minutes%60))+" minutes")
    else:
        time_s = (str(int(minutes))+" minutes")
    return time_s

'''
print(convert_time_string(4450))
print(convert_time_string(2880))
print(convert_time_string(3000))
print(convert_time_string(3300))
print(convert_time_string(6500))
print(convert_time_string(55))
print(convert_time_string(325))

'''
'''
def lookup_multiplier(req_exercise, weight, src_calories, exertable):
    # Add a doc string
    for row in exertable:
        Multiple = row["Multiplier"]
        Exercise = row["Exercise"]
        print(Exercise," equals ",Multiple)
        if Exercise == req_exercise:
            MultiplierX = float(Multiple)
            Minutes = (src_calories) / (weight * MultiplierX)
            return Minutes
'''
'''
# Diagnostic - remove this
exertable = pull_csv(exercisefile)
myvar = lookup_multiplier(exercise, weight, src_calories, exertable)
print ("Your exercise is: ", exercise, ".")
print ("Your weight is: ", weight," lbs.")
print ("To burn ", src_calories, " calories, you'd have to")
print ("exercise for ", "{:6.2f}".format(myvar), " minutes.")
'''

# suggestion:
# - read in csv file once and store in dictionary
# - give this dict to the function and simply see if req_excercise is  a valid key, if so, get its value