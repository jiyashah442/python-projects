#Name: Jiya Shah
#Description: This program is a tkinter game designed to simulate a pizza shop
#              /pizza making game. Using OOP this game was made so that the
#              player/user is able to create pizza's based on randomly generated
#              orders and collect points. Based on the fulfillment of orders
#              the score is calculated and displays as a +/- 10 based point
#              system.

#------------------------------- IMPORTANT -------------------------------------
#some things I did mention so its easier to play the code
#to add toppings after clicking sauce double click - basically when
#you intitially click a toppings button it allows for addition of topping
#but the player is meant to click the same topping button again to
#get out of topping adding mode, and return to the reg cursor
#so you can do either the above  or double click each button 

#-------------------------- Importing All Libraries ----------------------------
from tkinter import *
from tkinter import ttk
import random

#------------------------------- Creating Window -------------------------------
window = Tk()
window.title("Pizza Maker Game")
window.geometry("1100x600")

#------------------------------- Creating Canvas -------------------------------
#This game uses canvas compared to grid, since I found it more flexible and
# easier to place and display objects on

canvas = Canvas(window, width=1100, height=600) #creates the main canvas 
bg = PhotoImage(file="images/shopbg.png").subsample(1, 1) #retrieves the bg image 
canvas.create_image(0, 0, image=bg, anchor="nw") #sets the canvas to display bg

oven_img = PhotoImage(file="images/oven-nopizza.png").subsample(2, 2) #image for oven
canvas.create_image(680, 470, image=oven_img, anchor="center") #displays oven

canvas.pack() #packs canvas to display


topping_images = { #dictionary to hold all topping images and also sets sizes
    "Pepperoni": PhotoImage(file="images/pepperoni.png").subsample(11, 11),
    #changes size using subsample
    "Cheese": PhotoImage(file="images/cheese.png").subsample(2, 2),
    "Pineapple": PhotoImage(file="images/pineapple.png").subsample(10, 10),
    "Peppers": PhotoImage(file="images/pepper.png").subsample(10,10),
    "Onions": PhotoImage(file="images/onion.png").subsample(10,10),
    }

pizza_oven_img = PhotoImage(file="images/oven-pizza.png").subsample(2, 2)
#gets the image for the oven with pizza in it

size = None

#---------------------------- PizzaOrderGenerator Class ------------------------
class PizzaOrderGenerator: #defines PizzaOrderGenerator class
    '''
    PizzaOrderGenerator class manages all components to generating random
    orders for the user/player to fulfill. Primarily it updates and creates
    a order dictionary for each order.
    
    Args:
    None
    
    Returns:
    None
    
    '''
    possible_sizes = ['Small', 'Medium', 'Large'] #possible sizes to randomize
    possible_toppings = ['Pepperoni', 'Pineapple', 'Peppers',
                         'Onions'] #availible toppings to randomize
    
    order_dict = {} #dictionary to store all randomized orders based on order_num
    
    def __init__(self, order_num): #init constructur 
        
        self.order_num = order_num #order_num ex."Order 1" is defined inside class
        
        self.size = random.choice(self.possible_sizes) #chooses a random size
                                                         #from possible sizes
        
        self.num_of_toppings = random.randint(0, 4) #chooses a random num of toppings
        
        self.toppings_list = ['Cheese'] #initializes the topping list with Cheese
                                         # - since every pizza needs CHEESEEE!!
        
        while len(self.toppings_list) < self.num_of_toppings: #wile the toppings
                                         #list has less than the num of toppings
            topping = random.choice(self.possible_toppings) #continue generating
                                                               #random toppings
            
            if topping not in self.toppings_list: #if the topping is not already
                                          #in the topping list (avoids duplicates)
                self.toppings_list.append(topping) #add the topping to the list 
    
        PizzaOrderGenerator.order_dict[self.order_num] = { #for the key :
                                            #order_num create a bunch of values 
            "size" : self.size, #sets size to size selected
            "toppings" : self.toppings_list #sets toppings to topping list
            
            }
        
        #print(PizzaOrderGenerator.order_dict) #code I needed for debugging
        
    #defines a class method
    @classmethod
    def get_order_dict(cls): #since I need to retrive this class outside
                               #without accessing to self attributes
        return cls.order_dict #returns order dict 
    
    def get_size(self): #getter for size
        return self.size
    
    def get_toppings_list(self): #getter for toppings_list 
        return self.toppings_list
        
    def __str__(self): #magic method - we touched briefly on -
                                  #allows for easy formatting and returns
        
        return f"Size: {self.get_size()}\n" + "\n".join(self.get_toppings_list())
        #returns the size and toppings list

#---------------------------- Order Generating Display -------------------------

#creates the rectangles to display orders
order_rect1 = canvas.create_rectangle(40, 10, 180, 180, fill="white",
                                      outline="black")  
order_rect2 = canvas.create_rectangle(233, 10, 373, 180, fill="white",
                                      outline="black")  
order_rect3 = canvas.create_rectangle(426, 10, 566, 180, fill="white",
                                      outline="black")  
order_rect4 = canvas.create_rectangle(619, 10, 759, 180, fill="white",
                                      outline="black")  

#initliazes the texts of each display
order_text1 = "Waiting for Order..."
order_text2 = "Waiting for Order..."
order_text3 = "Waiting for Order..."
order_text4 = "Waiting for Order..."

#places labels for each order
order_label1 = Label(window, text=order_text1, font=("Times New Roman", 12),
                     bg='white', justify='left') #justify=left basically shifts
                                                # all the text to lefthandside
order_label1.place(x=50, y=20) #places label

order_label2 = Label(window, text=order_text2, font=("Times New Roman", 12),
                     bg='white', justify='left')
order_label2.place(x=245, y=20)

order_label3 = Label(window, text=order_text3, font=("Times New Roman", 12),
                     bg='white', justify='left')
order_label3.place(x=435, y=20)

order_label4 = Label(window, text=order_text4, font=("Times New Roman", 12),
                     bg='white', justify='left')
order_label4.place(x=630, y=20)

#------------------------ Order Generator Function -----------------------------

def order_generator():
    '''
    This function generates random orders based on order numbers, if for a set
    amount of time the order is not there/is "Waiting for Order" then the function
    calls the PizzaOrderGenerator class to generate an order for that order num.
    
    Args:
    None
    
    Returns:
    None
    
    '''
    
    global order_text1, order_text2, order_text3, order_text4 #globalizes variables
    
    if order_text1 == "Waiting for Order...": #if any of the texts is "Waiting for Order..."
        order = PizzaOrderGenerator("Order 1") #generates a random order for that text
        order_text1 = str(order) #calling magic method to just display the order in shell
        order_label1.config(text=order_text1) #configures the text of the label to new order
    elif order_text2 == "Waiting for Order...": #repeats above for other order_nums
        order = PizzaOrderGenerator("Order 2")
        order_text2 = str(order)
        order_label2.config(text=order_text2)
    elif order_text3 == "Waiting for Order...":
        order = PizzaOrderGenerator("Order 3")
        order_text3 = str(order)
        order_label3.config(text=order_text3)
    elif order_text4 == "Waiting for Order...":
        order = PizzaOrderGenerator("Order 4")
        order_text4 = str(order)
        order_label4.config(text=order_text4)
        
    window.after(10000, order_generator) #after every 10 seconds it calls the function

order_generator() #initializes the function call, which loops it using window.after

#-------------------------------- Score Class ----------------------------------

#defines score class which takes care of adding/subtracting to the score and
# retrieving it inside other functions/classes
class Score:
    '''
    Class Score keeps track of adding_subtracting to the player's score, and
    retrieving it inside other functions/classes.
    
    Args:
    None
    
    Returns:
    None
    
    '''
    def __init__(self, score=0):
        self._score = score #initilizes score as zero
        
    def __add__(self, other): #magic method common 1 - adds points to score
        return Score(self.get_score() + other)
    
    def __sub__(self, other): #magic method common 2 - subtracts points from score
        return Score(self.get_score() - other)
    
    def get_score(self): #getter used to get the score value
        return self._score
    
#------------------------------- Pizza Classes ---------------------------------

#Base_Pizza class mainly used to show an example of inheritance
    #all base pizzas start as a size with cheese as the only topping
class Base_Pizza:
    '''
    The Base_Pizza Class initializes the pizza as a dough with its only
    topping being cheese. It is mainly used as a Parent function for Pizza
    to demonstrate an example of inheritance.
    
    Args:
    None
    
    Returns:
    None
    
    '''
    def __init__(self, size, toppings=["Cheese"]):
        self.size = size #sets size
        self.toppings = toppings #sets toppings to cheese only
        
    def get_size(self): #getter for size
        return self.size
    
    def get_toppings(self): #getter for toppings
        return self.toppings
        
    def __str__(self): #magic method to retreive string
        return f"Size: {self.get_size()}, Toppings: {', '.join(self.get_toppings())}"
    
class Pizza(Base_Pizza): #example of inheritance, Pizza inherits size, toppings
    #from class Base_Pizza
    '''
    The class Pizza mainly controls and adds to the pizza_dict which is a
    dictionary that contains all the info of the players movement and
    creation of pizzas.
    
    Args:
    None
    
    Returns:
    None
    
    '''
    
    pizza_dict = {} #initializes pizza dictionary as empty dict
    
    def __init__(self, size, toppings=["Cheese"]):
        super().__init__(size, toppings) #references parent class base pizza
        #and gets size and toppings from class
        
        self.pizza_id = f"pizza{len(Pizza.pizza_dict) + 1}" #the pizza id is the
        #len of the pizza dict + 1
        #ensures theres not infinite number of pizza_ids instead its only pizza1,
        #pizza2, pizza3
        
        self.status = "Counter" #initlaizes status of pizza to "Counter" aka on
        #the counter 

    def get_toppings(self): #getter for toppings
        return self.toppings
    
    def get_pizza_id(self): #getter for pizza id
        return self.pizza_id
    
    def get_size(self): #getter for size
        return self.size
    
    def get_status(self): #getter for status
        return self.status
        
    @classmethod #class method used to add a new pizza to the pizza dict to keep
    #track of it
    def add_pizza(cls, size): #defines method, attribute size
        
        new_pizza = cls(size) #creates a new instance of class method
        
        cls.pizza_dict[new_pizza.get_pizza_id()] = {"size": new_pizza.get_size(),
         "status": new_pizza.get_status(), "toppings": [], "canvas_objects": []}
        #stores new_pizza into pizza_dict by assigning it a pizza_id
        #for the pizza_id which is the key in the dict
        #it creates a corresponding value in the dictionary with all the values
        #for the pizza info
        
        #print('done') debugging statements i needed
        #print(cls.pizza_dict)
        
        return new_pizza.get_pizza_id() #returns the pizza_id for the new pizza
    
    @classmethod #class method to change the status of where the pizza is 
    def update_status(cls, new_status, pizza_id):
        cls.pizza_dict[pizza_id]["status"] = new_status
        
    @classmethod
    def get_pizza_dict(cls): #getter for pizza_dict, access to pizza_dict directly
                                                 #instead of dealing with classes
        return cls.pizza_dict
        
        
    def __eq__(self, order_info): #comparison magic method - __eq__ 
        return self.get_size() == order_info["size"] and sorted(self.get_toppings()) == sorted(order_info["toppings"])
        #returns Boolean value True/False if both the size and the toppings list 
        # of the order made by the user and the order_dict is the same
        
#-------------------------- Toppings Class -------------------------------------
#define topping class, used to manage topping placement and addition to pizza_dict
class Toppings:
    '''
    Toppings class manages all placement and addition of toppings on the pizzas.
    
    Args:
    None
    
    Returns:
    None
    
    '''
    def __init__(self, canvas):
        self.canvas = canvas #allows access to canvas within class
        self._topping_mode = False #weak private attribute for topping mode,
                                                      #if True allows placement
        # of toppings if false does not
        self._active_topping = None #weak private attribute for storing
                                                     #currently selected topping
        
    #setter - sets the selected topping/active topping
    def set_active_topping(self, topping_name):
        self._active_topping = topping_name #sets the selected topping to topping name 
        self._topping_mode = not self._topping_mode
        #changes the topping mode to opp value to allow/deny placement depending on button
        
    #getter - retrives the correponding topping image from topping_images dictionary
    def get_topping_image(self):
        return topping_images.get(self.get_active_topping(), None)
        #.get() prevents crash, if not topping image is found it returns None
    
    @property #property for tooggling topping mode
    def topping_mode(self): #returns the topping mode
        return self._topping_mode
    
    #getter for selected topping
    def get_active_topping(self):
        return self._active_topping
    
    #method for placing toppings - event used to pass data of users x,y coordinates when
    #the user clicks anything in the GUI
    def place_topping(self, event):
                
        if self.topping_mode == True: #this variable checks if a topping button
            #double clicked topping_mode is set to True, this avoids placing toppings
            #when user is trying to click other areas in the GUI
            topping_name = self.get_active_topping() #recieves the name of
            #the selected topping
                                
            pizza_id = None #initializes pizza_id as none
                    
            for key, pizza_id_dict in Pizza.pizza_dict.items(): #for every pizza_id in pizza_dict
                #it gets the items/values under thant pizza id as pizza_id_dict
                if pizza_id_dict.get("status") == "Counter": #if the value corresponding to "status"
                    #is counter (aka the pizza is located at the counter)
                    pizza_id = key #we know it is that pizza that toppings
                    #are being added to, the key is set as the pizza_id
    
            if pizza_id != None: #as long as the pizza_id is found
                pizza_id_dict = Pizza.pizza_dict.get(pizza_id) #retrive the dict values/items
                #that correspond to key pizza id without direct accessing
                    
                if topping_name == "Sauce": #if the topping name is sauce
                    #it conducts a seperate code place the sauce
                    #since it requires more if/else statements
                        
                    size = pizza_id_dict.get("size") #get the size from the values corresponding to pizza_id
                    
                    #based on the size it creates a circle that fits inside that size pizza
                    
                    if size == "Large": #checks for certain size
                        #creates a sauce circle in a specific position
                        sauce_object = self.canvas.create_oval(305, 365, 480, 535, fill="red")  

                    if size == "Medium":
                        sauce_object = self.canvas.create_oval(325, 385, 460, 515, fill="red")  

                    if size == "Small":
                        sauce_object = self.canvas.create_oval(345, 405, 440, 495, fill="red")  
                        
                    pizza_id_dict.get("canvas_objects").append(sauce_object)
                    #from the pizza_id_dict it retrieves the list corresponding to
                    #canvas_objects, and to that list it appends this new sauce_object

        
                else: #if the topping is not sauce, follows this code for all other
                    #toppings
                    topping_image = self.get_topping_image() #gets the topping_image
                    #corresponding to topping name
                    
                    topping_id = self.canvas.create_image(event.x, event.y,
                                                          image=topping_image,
                                                          anchor="center")
                    #the topping_id is the canvas object created for the topping
                    #displaying the image
                    #it tracks where the object was placed using event.x, event.y and
                    #saves it as a temp variable under topping_id
                    
                    pizza_id_dict.get("canvas_objects").append(topping_id)
                    #it then retrieves the list corresponding to "canvas_objects"
                    #and appends the canvas_object placed for topping to the list
                    #to keep track of it
                    
                                        
                if topping_name not in pizza_id_dict.get("toppings"):
                    #if the topping is not already registered under toppings list
                    #in the pizza dict for the specific pizza_id
                    
                    #print(pizza_id_dict.get("toppings")) #debugging statement used
                    pizza_id_dict.get("toppings").append(topping_name)
                    #gets the list value correponding to toppings in the dict and
                    #appends the topping_name/new topping to it so
                    #that it is used we cross referencing if the order
                    #submitted is correct
                    
                    #print(pizza_id_dict.get("toppings")) #debugging statement i used
                    
    @staticmethod #static method - instead of a seperate function I used a
    #static method to control the button binding and setting the active topping
    def place_topping_active(topping_instance, topping_name, canvas):
        topping_instance.set_active_topping(topping_name) #for the instance
        #topping instance set the active topping to the topping_name
        
        canvas.bind("<Button-1>", topping_instance.place_topping) #binds the
        #mouse click to the place_topping method so whenever the user clicks
        #the canvas the topping is placed and recorded
        
#--------------------------- Pizza_Game Class ----------------------------------
                
topping_instance = Toppings(canvas) #creates the instance used to manage topppings
dough_occupied = False #iniatlizes no dough in counter area
oven_full = False #initializes oven as empty
packing_full = False #initializes the packing area as empty
player_score = Score() #player_score instance
count= 0 #count used to keep track of
#the pizzas the user has submitted 

class Pizza_Game_Controller: #class to controll game movement - mostly
    #to call other classes and methods
    
    '''
    This class is probably largest and most versatile, it controls all
    game movement, and is mainly used to call other classes and methods. It
    behaves like the main function, controlling all basic game logistics.
    
    Args:
    None
    
    Returns:
    None
    
    '''
    
    def __init__(self, canvas): 
        self.canvas = canvas
        self.dough_occupied = False #initializes variables inside class
        self.oven_full = False
        self.packing_full = False
        
    #the variables below are used to ensure multiple canvas_objects/pizzas
        #cannot be placed in the same area
    def get_dough_occupied(self): #getters/setters for all variables
        return self.dough_occupied
    def set_dough_occupied(self, value):
        self.dough_occupied = value
        return self.dough_occupied
    def get_oven_full(self):
        return self.oven_full
    def set_oven_full(self, value):
        self.oven_full = value
        return self.oven_full
    def get_packing_full(self):
        return self.packing_full
    def set_packing_full(self, value):
        self.packing_full = value
        return self.packing_full
        
    def add_dough(self, size): #method 
        
        if self.get_dough_occupied() == False: #a dough can only
            #be added if the counter area is empty
            
            #based on the sizes the user chooses a dough canvas object is created
            if size == "Large":
                dough = self.canvas.create_oval(290, 350, 495, 550, fill="wheat")  
            if size == "Medium":
                dough = self.canvas.create_oval(310, 370, 475, 530, fill="wheat")  
            if size == "Small":
                dough = self.canvas.create_oval(330, 390, 455, 510, fill="wheat")  
                        
            new_pizza_id = Pizza.add_pizza(size) #a new pizza id is retrieved
            #and a place in the pizza_dict is created for the pizza
            
            Pizza.pizza_dict[new_pizza_id].get("canvas_objects").append(dough)
            self.set_dough_occupied(True)
            #from the values corresponding to the pizza_id in the dict
            #get the list corresponding to "canvas_objects" and append
            #the new dough canvas
            
        else:
            print("Dough Already There!!") #prints if there is another pizza
            #in the counter area 
    
    #method for placing the pizza into the oven - undergone
            #if user clicks "Bake" button
    def place_pizza_in_oven(self):
        
        #if the oven is not full and the counter area has a pizza on it
        if self.get_oven_full() == False and self.get_dough_occupied() == True:
        #only then will the below code run
            
            pizza_id = None #initializes pizza_id as None
                    
            for key, pizza_id_dict in Pizza.pizza_dict.items():
                #for every pizza_id in pizza_dict, accesses the
                #values corresponding to that pizza_id
                
                if pizza_id_dict.get("status") == "Counter": #from that
                    #pizza_id values "dict"/set it gets the specific
                    #value corresponding to "status"
                    #ex "status" : "Counter"
                    
                    pizza_id = key #if that status value is "Counter"
                    #for that pizza id it is the pizza we are looking for
                    
            if pizza_id != None: #as long as the pizza id is not none
                    
                for item in Pizza.pizza_dict.get(pizza_id).get("canvas_objects"):
                    self.canvas.move(item, 270, 0)
                #get the values corresponding to pizza_id, then from that
                    #get the list corresponding to "canvas_objects" value
                    #under pizza_id key, and for every canvas_object in that
                    #list more the object 270 pixels to the right so that
                    #it hides behind the oven image
                
                self.canvas.create_image(680, 470, image=pizza_oven_img, anchor="center")
                #to cover the canvas_objects cover them with an image overlay
                #this overlay is an image of an oven with a pizza in it
                #to simulate a better "GUI" enhancement
                
                Pizza.update_status("Oven", pizza_id) #update that status
                #of the pizza under such pizza_id to now in the Oven
                
                self.set_oven_full(True) #set the values to the opposite
                #since the pizza has been moved
                self.set_dough_occupied(False)
                      
        else:
            print("No Dough found or Oven is Full!!") #if no pizza on the counter
            #or the oven has a pizza in it display
            
    #method just like place_pizza_in_oven but this time to remove it
            #from oven and trasnfer it to the packing station
    def remove_pizza_from_oven(self):
        
        #only if the oven has a pizza in it and the packing area is not full
        #will the below code run
        if self.get_oven_full() == True and self.get_packing_full() == False:
            
            pizza_id = None #initializes pizza id as none
                    
            for key, pizza_id_dict in Pizza.pizza_dict.items():
                #for every pizza_id in pizza_dict, accesses the
                #values corresponding to that pizza_id
                if pizza_id_dict.get("status") == "Oven":
                    #pizza_id values "dict"/set it gets the specific
                    #value corresponding to "status"
                    #ex "status" : "Oven"
                    
                    pizza_id = key #gets the pizza id of the
                    #pizza that is in the oven!
                    
            if pizza_id != None: #as long as the pizza id is not None
                
                #objects that need to be later deleted are collected under this variable
                #first get the values corresponding to pizza_id, then specifically
                #get the list corresponding under the value "canvas_objects"
                packed_canvas_objects = Pizza.pizza_dict.get(pizza_id).get("canvas_objects")
               
                for items in packed_canvas_objects:
                    #for every object in the list 
                    self.canvas.move(items, 285, 0)
                    #move it to the packing area 
                
                #create an image over the oven once again, or an empty oven
                    #for better gui screen visuals
                self.canvas.create_image(680, 470, image=oven_img, anchor="center")
                
                Pizza.update_status("Packing", pizza_id) #update the
                #status in pizza_dict for the pizza_id that is now in packing 
                
                self.set_oven_full(False) #set to opp to allow other pizzas to
                #enter oven/not enter packing area
                self.set_packing_full(True)
                
        else:
            print("Oven Empty or Packing Area Full!!") #print if full
            
    def decorator_pizzas_submitted(func): #decorator method to help
        #keep track of pizza submissions
        def wrap(self, order_id):
            global count
            
            order_texts = {
                "Order 1": order_text1,
                "Order 2": order_text2,
                "Order 3": order_text3,
                "Order 4": order_text4
                }
            
            if order_texts[order_id] != "Waiting for Order...": #as long
                #as the user submits to an valid order the submissions
                #count increases
                count+= 1
                label_pizza_count.config(text=f"Total Pizzas Submitted: {count}")
                #changes the count dislay
                func(self, order_id) #enables the submit_order method
            else:
                print("Error, Order does not Exist.")
        
        return wrap #returns 
        
    @decorator_pizzas_submitted #this function is part of the decorator
    def submit_order(self, order_id):
        global order_text1, order_text2, order_text2, order_text3, order_text4, player_score
        if self.get_packing_full() == True: #as long as there
            #is a pizza in the packing area
            
            pizza_id = None #intialize
                    
            for key, pizza_id_dict in Pizza.pizza_dict.items(): #same thing
                #as above to get the pizza_id which has a status of Packing
                if pizza_id_dict.get("status") == "Packing":
                    pizza_id = key
                
            if pizza_id != None: #as long as pizza_id not none
                pizza_dict = Pizza.get_pizza_dict()
                #gets the pizza_dict
                
                order_dict = PizzaOrderGenerator.get_order_dict()
                #gets the order_dict
                
                pizza_info = pizza_dict.get(pizza_id) #gets the values
                #only specific to pizza_id in the dict
                order_info = order_dict.get(order_id) #same thing
                #values only specific to an order_id
                
                order_info.get("toppings").append("Sauce") #since sauce
                #isnt explicity displayed in the order its added now
                #to ensure that a sauce topping is added by user
                    
                pizza_instance = Pizza(pizza_info.get("size"),
                                       pizza_info.get("toppings"))
                #pizza imstance for the specific pizza
                    
                if pizza_instance == order_info: #if the info
                    #is the same, calls __eq__ compares the two
                    #and if returns True
                    print("YAYAYAY!!") #prints YAYAYAYA 
                    player_score += 10 #adds to score
                else: #else if not the same
                    print("Wrong Order :(")
                    player_score -= 10
                    
                #print(player_score.get_score()) #debugging
                    
                #change score display
                score_label.config(text=f"Score: {player_score.get_score()}")

                        
                for item in Pizza.pizza_dict.get(pizza_id).get("canvas_objects"):
                    #for ever item in "canvas_objects" list udner that pizza_id key
                    
                    self.canvas.delete(item) #deletes each canvas object one by one
                        
                Pizza.pizza_dict.pop(pizza_id) #removes info of the pizza_id
                #and all its values from list
                    
                #changes the order_texts to regenrate order
                if order_id == "Order 1":
                    order_text1 = "Waiting for Order..."
                    order_label1.config(text=order_text1)
                elif order_id == "Order 2":
                    order_text2 = "Waiting for Order..."
                    order_label2.config(text=order_text2)
                elif order_id == "Order 3":
                    order_text3 = "Waiting for Order..."
                    order_label3.config(text=order_text3)
                elif order_id == "Order 4":
                    order_text4 = "Waiting for Order..."
                    order_label4.config(text=order_text4)
                        
                self.set_packing_full(False)   #sets packing back to false        
                
game_instance = Pizza_Game_Controller(canvas) #game_instance used to access for buttons

#----------------------------- All Buttons -------------------------------------

btn_add_dough = Button(window, text="Add Dough", command=lambda:
                       game_instance.add_dough(combo.get()))
#lambda is used to pass arguments in the functions/methods called

btn_add_dough.place(x=280, y=565) #places button

cheese_img = PhotoImage(file="images/cheese_image.png").subsample(6, 6) #subsample to
#reduce sizes of images displayed

btn_add_cheese = Button(window, image=cheese_img, command=lambda:
                        Toppings.place_topping_active(topping_instance,
                                                      "Cheese", canvas),
                                                         bg="white")
btn_add_cheese.place(x=130, y=425)

pepperoni_img = PhotoImage(file="images/pepperoni_image.png").subsample(5,5)

btn_add_pepperoni = Button(window, image=pepperoni_img, command=lambda:
                           Toppings.place_topping_active(topping_instance,
                                                         "Pepperoni", canvas),
                                                                  bg = "white")
btn_add_pepperoni.place(x=130, y=340)

sauce_img = PhotoImage(file="images/sauce_image.png").subsample(6, 6)

btn_add_sauce = Button(window, image=sauce_img, command=lambda:
                       Toppings.place_topping_active(topping_instance, "Sauce",
                                                     canvas), bg="white")
btn_add_sauce.place(x=130, y=505)

pineapple_img = PhotoImage(file="images/pineapple_image.png").subsample(18, 19)

btn_add_pineapple = Button(window, image=pineapple_img, command=lambda:
                           Toppings.place_topping_active(topping_instance,
                                                         "Pineapple", canvas),
                                                                    bg="white")
btn_add_pineapple.place(x=30, y=510)

peppers_img = PhotoImage(file="images/peppers_image.png").subsample(11, 11)

btn_add_peppers = Button(window, image=peppers_img, command=lambda:
                         Toppings.place_topping_active(topping_instance,
                                                       "Peppers", canvas),
                                                                   bg="white")
btn_add_peppers.place(x=30, y=420)

onion_img = PhotoImage(file="images/onion_image.png").subsample(7,7)

btn_add_onions = Button(window, image=onion_img, command=lambda:
                        Toppings.place_topping_active(topping_instance,
                                                      "Onions", canvas),
                                                                   bg="white")
btn_add_onions.place(x=30, y=340)

btn_add_to_oven = Button(window, text="Bake",
                         command=game_instance.place_pizza_in_oven)
btn_add_to_oven.place(x=600, y=570)

btn_remove_from_oven = Button(window, text="Remove from Oven",
                              command=game_instance.remove_pizza_from_oven)
btn_remove_from_oven.place(x=650, y=570)

btn_submit_order = Button(window, text="Submit Order",
                          command=lambda: game_instance.submit_order(combo_order.get())) 
btn_submit_order.place(x=830, y=565)

label_pizza_count = Label(window, text="Total Pizzas Submitted: 0",
                          font=("Times New Roman", 12), bg="white")
label_pizza_count.place(x=830, y=20)

score_label = Label(window, text="Score: 0", font=("Times New Roman", 13),
                    bg="white")
score_label.place(x=830, y=60)

combo = ttk.Combobox(window)
combo['values'] = ["Large", "Medium", "Small"] #adds values as a list
combo.current(1) #set the selected item.
combo.place(x=360, y=565)

combo_order = ttk.Combobox(window)  
combo_order['values'] = ["Order 1", "Order 2", "Order 3", "Order 4"]
# Set order options
combo_order.current(0)  # Default selection is "Order 1"
combo_order.place(x=930, y=565)  # Position it in the UI

order_1_label = Label(window, text="Order 1", font=("Times New Roman", 12),
                      bg="white")
order_1_label.place(x=120, y=155)

order_2_label = Label(window, text="Order 2", font=("Times New Roman", 12),
                      bg="white")
order_2_label.place(x=315, y=155)

order_3_label = Label(window, text="Order 3", font=("Times New Roman", 12),
                      bg="white")
order_3_label.place(x=510, y=155)

order_4_label = Label(window, text="Order 4", font=("Times New Roman", 12),
                      bg="white")
order_4_label.place(x=700, y=155)

window.mainloop() #runs everything!!