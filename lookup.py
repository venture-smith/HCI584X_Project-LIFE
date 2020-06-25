#-------------------------------------------------------------------------------
# Name:      lookup.py
# Purpose:   Primary program flow for LIFE webapp
# Author(s): Vincent Lin
# Created:   06/10/2020
# TODO:      XXX YYY ZZZ
# Note:      This function looks up the multiplier to be used in the calculation
#-------------------------------------------------------------------------------

fname="HCI584X_Project-LIFE\exercise.csv"
exercise="Water polo" # CREATE A FUNCTION TO SELECT/RANK TOP 3 ACTIVITIES
weight=135
src_calories=550

# importing module  
import csv 

def lookup_multiplier(file, req_exercise, weight, src_calories, delimiter=","):
    ''' add a doc string '''
    if not delimiter:
        delimiter = ','   # why not set delimiter=',' in function header (instead None?)
    reader = csv.DictReader(open(file), delimiter=delimiter)
    for row in reader:
        Multiple = row["Multiplier"]
        Exercise = row["Exercise"]
        #print(Exercise," equals ",Multiple)
        if exercise == req_exercise:
            MultiplierX = float(Multiple)
            Minutes = (src_calories) / (weight * MultiplierX)
            return Minutes

myvar = lookup_multiplier(fname, exercise, weight, src_calories)
print ("Your exercise is: ", exercise, ".")
print ("Your weight is: ", weight," lbs.")
print ("To burn ", src_calories, " calories, you'd have to")
print ("exercise for ", "{:6.2f}".format(myvar), " minutes.")

# suggestion:
# - read in csv file once and store in dictionary
# - give this dict to the function and simply see if req_excercise is  a valid key, if so, get its value