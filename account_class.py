''' PRIMARY DATA STRUCTURE 

This module describes the primary user account class and includes subclass for the restaurant and food item.

'''

class Account:
    # Create user account
    def __init__(self, id, LoginId, Email, Password, FirstName, LastName, Pref1, Pref2, Pref3, Weight, Units, Item, MinEquiv1, MinEquiv2, MinEquiv3):
        self.id = id
        self.LoginId = LoginId
        self.Email = Email
        self.Password = Password
        self.FirstName = FirstName
        self.LastName = LastName
        self.Pref1 = Pref1
        self.Pref2 = Pref2
        self.Pref3 = Pref3
        self.Weight = Weight
        self.Units = Units
        self.Item = Item
        self.MinEquiv1 = MinEquiv1
        self.MinEquiv2 = MinEquiv2
        self.MinEquiv3 = MinEquiv3
 
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

    def getPref1(self):
        return self.Pref1
    
    def getPref2(self):
        return self.Pref2

    def getPref3(self):
        return self.Pref3

    def getWeight(self):
        return self.Weight

    def getUnits(self):
        return self.Units

    def getItem(self):
        return self.Item

    def getMinEquiv1(self):
        return self.MinEquiv1

    def getMinEquiv2(self):
        return self.MinEquiv2

    def getMinEquiv3(self):
        return self.MinEquiv3

class Item:
        # Create user account
    def __init__(self, Restaurant, Food, Calories):
        self.id = id
        self.Restaurant = Restaurant
        self.Food = Food
        self.Calories = Calories

    def getRestaurant(self):
        return self.Restaurant

    def getFood(self):
        return self.Food

    def getCalories(self):
        return self.Calories