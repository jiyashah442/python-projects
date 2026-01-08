# Name: Jiya Shah
# ID: 918951
# File Name: JS-918951-MathFlashcardsFinalCode.py
# Description: This program performs a series of functions to create a GUI
#               application for a 'Math Flashcards' Game. It displays a
#                randomized equations onto a themed user interface / window
#                 allowing the user to answer math equations. Along with the
#                  basic levels, the user is also able to choose the type of
#                   math questions they would like, able to skip questions,
#                    change the operator, etc. 

#-------------------------------- LIBRARIES ------------------------------------

from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox
from tkinter import scrolledtext
import random

#--------------------------------- FUNCTIONS -----------------------------------


#Function corresponding to changing difficulty level button on tab2, when called
#  updates the value to maximum to become value of corresponding radio button
    # Arg: none
    # Returns: maximum 
def changed():
    global maximum, selected
    
    #maximum range is equal to the assigned lvl of the radiobutton pressed
    maximum = selected.get()

    return maximum


#Function corresponding to changing the operator on tab2, when called updates
#  the operator to corresponding radio button
    # Arg: none
    # Returns: operator
def operatorselect():
    global operator, changedop
    #the operator value is equal to the assigned op of the radiobtn pressed
    opvalue = changedop.get()
    
    #based on assigned values, corresponds which radiobutton is which operator
    if opvalue == 1:
        operator = "+"
    elif opvalue == 2:
        operator = "-"
    elif opvalue == 3:
        operator = "x"
    elif opvalue == 4:
        operator = "÷"
    else:
        operator = random.choice("+-x÷")
    
    #returns operator selected
    return operator 
    
    
#Function which will calculate the correct answer of the math equation
    # Arg: user (entry input)
    # Returns: text to display (whether answer is correct or not)
def correctanswer(user):
    global num1, num2, operator, correctnum, wrongnum, streak

    #setting a default/initial 
    correctans = -1
    
    #if the operation is addition, the answer is the two #'s added
    if operator == "+":
        correctans = num1 + num2
    #if the operation is subtraction, the ans is the first # minus second #
    elif operator == "-":
        correctans = num1 - num2
    #if the operation is multiplication, the ans is the first # times second #
    elif operator == "x":
        correctans = num1 * num2
    #otherwise, the op is division, the ans is the first # divide second #
    else:
        correctans = num1 // num2
    
    #if the users input equal the correct answer
    if user == correctans:
        #display a message to the user informing they got the correct ans
        display = "You got it!"
        #set the correct # of answers to one more than the previous
        correctnum += 1
        #add 1 more correct ans to the streak
        streak += 1
        #in the question log, add the correct equation with user's answer
        log.insert(INSERT, str(num1) + " " + operator + " " + str(num2) \
                   + " = " + str(correctans) + "\n")
    
    #if the users input is wrong (compared to the correct answer)
    else:
        #display a msg to the user informing they are wrong and the correct ans
        display = "Wrong. The correct answer to  " + str(num1) + " " \
                  + operator + " " + str(num2) + "  was " + str(correctans) \
                  + ' .'
        #add one to the number of wrong answers so far
        wrongnum += 1
        #add the equation, user's ans, and the correct ans to questions log
        log.insert(INSERT, str(num1) + " " + operator + " " + str(num2) \
                   + " ≠ " + str(user) + "  Ans: " + str(correctans) + "\n")
        #reset the streak to zero
        streak = 0
    
    #display the streak label depending on if the user is correct or not 
    streaklabel.configure(text=("Streak: " + str(streak)))
    
    #return the display text
    return display


#Function which generates random numbers and an operator to make the equation
    # Arg: none
    # Returns: num1, num2, operator
def randomgenerator():
    global num1, num2, operator, maximum, minimum
    
    #generates two random nums based on min and max range values (inclusive)
    num1 = random.randint(minimum,maximum)
    num2 = random.randint(minimum,maximum)
    
    #call function to match operator to corresponding radio btn chosen
    operator = operatorselect()
    
        #if it is subtraction making sure num1 > num2 (avoid negatives)
    if operator == "-":
        while num1 < num2:
            num1 = random.randint(minimum, maximum)
        #if it is divison, num2 cannot be 0 since division by 0 is not possible
            #rengenerating num2 until num != 0
    if operator == "÷":
        while num2 == 0:
            num2 = random.randint(minimum,maximum)
        
        #using the product of the num1 and num2, to set as num1, so num1 / num2
            #will equal the randomized number/original value of num1 
        num1 = num1 * num2
    
    #returning num1, num2, operator
    return num1, num2, operator


#Function which corresponds to the submit button, does several processes:
# 1. checks for a valid integer input in entry box
# 2. if valid input, finds if answer is correct or not (calls correctanswer())
# 3. generates new values for num1, num2, operator (calls randomgenerator())
    # Arg: none
    # Returns: none
def submit():
    global enter, num1, num2, operator, count
    
    #if it is the first question/when application is first opened
    if count == 0:
        #randomly generate num1, num2, operator
        num1, num2, operator = randomgenerator()
        #display text is nothing/there is nothing to display
        displaylabel.configure(text = "")
        #focus the cursor onto the entry box for easy user entry
        enter.focus()
    
    #if the count is passed when the application if first opened
    elif count > 0:
        #initialize validinput var
        validinput = ""
        #try to obtain an integer input from the user entry box
        try:
            user = int(enter.get())
            #if obtained this code will be reached
            validinput = 1
            
        #if a valid integer is not obtained, display to the user to input only
            #valid integer numbers
        except:
            display = "Please enter a number."
        
        #this part will only work if a valid input is obtained, if so
        if validinput == 1:
            #initialize the correct answer as default value
            correctans = -1
            
            #obtain display text to figure out if users input equal correct ans
            display = correctanswer(user)
            
            #regenerate random equation/next question 
            num1, num2, operator = randomgenerator()
        
        #if valid input is not obtained, user cannot move onto next question
        else:
            #the equation will remain the same until a valid input is obtained
            num1 = num1
            num2 = num2
            operator = operator
            #accounts for the count += 1 in the ahead lines (to cancel them out)
            count -= 1
        
        #displays to the user their result/if they got it wrong or correct
        displaylabel.configure(text=display)
    
    #changing label text to new numbers/operator
    num1label.configure(text=num1)
    num2label.configure(text=num2)
    oplabel.configure(text=operator)
    
    #since moving onto next question, add 1 to count for completing last 
    count += 1
    
    #configuring displayed values for total, correct, and wrong
    totalattempts.configure(text = ("Total: " + str(count - 1)))
    correct.configure(text = ("Correct: " + str(correctnum)))
    wrong.configure(text = ("Wrong: " + str(wrongnum)))

    #clears the entry box after user inputs/before next question
    enter.delete(0, END)


#Function which corresponds to clear button, and resets all counts, correct, and
#  wrong answers back to original settings (0)
    # Arg: None
    # Returns: None
def reset():
    global count, correctnum, wrongnum
    
    #initialize default values
    count = 1
    correctnum = 0
    wrongnum = 0
    
    #configure so all values are back to 0 
    totalattempts.configure(text = ("Total: " + str(count - 1)))
    correct.configure(text = ("Correct: " + str(correctnum)))
    wrong.configure(text = ("Wrong: " + str(wrongnum)))
    
    #configure so label shows nothing as well
    displaylabel.configure(text = "")


#Function corresponds to the binding of the submit button and hovering over it
    # Arg: none
    # Returns: none 
def clicker(event):
    #calls submit() function - main function running everything/generating
    # equations
    submit()


#Function corresponding to Combobox on tab2 allowing the user to choose between
    #only positive numbers and the inclusion of negative numbers
    # Arg: none
    # Returns:none
def comboclick():
    global chosen1, minimum, maximum
    
    #obtains the choosen option from combobox and assigns to var chosen1
    chosen1 = combo.get()
    
    #if the chosen option is negatives included, expand range mininum to the
        #negative of the maximum 
    if chosen1 == "Negative #'s Included":
        minimum = -(maximum)
    #otherwise the option chosen is only positives, so the minimum remains 1
    else:
        minimum = 1


# Function which corresponds to the skipbutton, allowing the user to skip
    # questions they may find difficult
    # Arg: none
    # Returns: none
def skipquestion():
    global num1, num2, operator, correctans, streak
    
    #initialize the correct ans as an empty string
    correctans = ""
    
    #depending on the operator calculate the correct answer
    if operator == "+":
        correctans = num1 + num2
    elif operator == "-":
        correctans = num1 - num2
    elif operator == "x":
        correctans = num1 * num2
    else:
        correctans = num1 // num2
    
    #in the scrolltext widget on tab2 add the skipped question and its answer
    log.insert(INSERT, "Skipped: " + str(num1) + " " + operator + " "
               + str(num2) + " = " + str(correctans) + "\n")
    
    #regenerate equation
    num1, num2, operator = randomgenerator()
    
    #configure the labels to display the new equation
    num1label.configure(text=num1)
    num2label.configure(text=num2)
    oplabel.configure(text=operator)
    
    #configure the display msg to return to empty
    displaylabel.configure(text = "")
    
    #since the question was skipped, user lost their streak, streak resets to 0
    streak=0
    streaklabel.configure(text="Streak: " + str(streak))

    
#-------------------------------- MAIN CODE ------------------------------------
    
#creates window
window = Tk()
window.title("Math Flashcards")
window.geometry("1000x600") 

#creates tabs
mytab = ttk.Notebook(window)
tab1 = Frame(mytab, bg="#FFEBF3")
tab2 = Frame(mytab, bg="#FFEBF3")
mytab.add(tab1, text="Game")
mytab.add(tab2, text="Settings")
mytab.pack(expand=1, fill='both')

#------ Setting Background Image ------
#define the image as a file from directory/device
bg = PhotoImage(file="tab1bg.png")

#configure the label to display the bg image
bglabel1 = Label(tab1, image=bg)

#place the label onto the screen and size accordingly
bglabel1.place(x=0, y=0, relwidth = 1, relheight = 1)

#repeat but now for tab 2
bglabel2 = Label(tab2, image=bg)
bglabel2.place(x=0, y=0, relwidth = 1, relheight = 1)

#--------- Initializing Values ----------

minimum = 1 
maximum = 3
count = 0

#for the first question, display as question marks
num1 = "?"
num2 = "?"
operator = "?"


#------------------------------- ALL WIDGETS -----------------------------------
#---------------------------------- tab 1 --------------------------------------

#---- Randomized Number/Operator Labels ----
    #Define Labels
num1label = Label(tab1, text=num1, font=('Britannic Bold', 70), \
                  bg = '#A6EAEF', fg = "white")
num2label = Label(tab1, text=num2, font=('Britannic Bold', 70), \
                  bg = '#A6EAEF', fg = "white")
oplabel = Label(tab1, text=operator, font=('Britannic Bold', 50), \
               bg = '#FFC0D9', fg = "white")
equalsign = Label(tab1, text="=", font=('Britannic Bold', 50), \
                  bg = '#FFBA97', fg = "white")
    
    #Placing Labels on Grid
num1label.grid(row=3, column=1, ipadx = 27)
num2label.grid(row=3, column=3, ipadx = 27)
oplabel.grid(row=3, column=2, ipadx = 17, padx=20)
equalsign.grid(row=3, column=4, rowspan=2, ipadx=17, padx=20)
    
    #Fillers 
fill20 = Label(tab1, text=" "*20, font=('Arial', 40), bg = '#FFEBF3')
fill20.grid(row=2, column=0, columnspan=6)


#------------- User Entry Box -------------
enter = Entry(tab1, width=3, font=('Britannic Bold', 70), bg='#FFF9FB')
enter.grid(row=3, column=5, rowspan=2)


#-------------- Submit Button --------------
submitbutton = Button(tab1, text='Submit', font=('Britannic Bold', 18), \
                     bg = '#F6A2B0', fg = 'white' , command=submit)
submitbutton.grid(row=3, column=6, rowspan=2, padx=20)

#binding the submit button, so that when computer mouse hovers over it to
# carry out submit function (through function clicker)
submitbutton.bind("<Enter>", clicker)

#---------- Wrong/Correct Answer Display ------------
displaylabel = Label(tab1, text = "Welcome! Please press the submit button to \
start." , font=('Britannic Bold', 20), bg = '#FFEBF3', fg='#F6A2B0')
displaylabel.grid(row=5, column=1, columnspan=6, pady=70)


#-------- Correct, Wrong & Total Attempts Labels --------
    #Defining Variables, count/total attempts, # of correct user inputs and
        # the # of wrong user inputs as 0 
count = 0
correctnum = 0
wrongnum = 0
    
    #Defining Labels
totalattempts = Label(tab1, text=("Total: " + str(count)), \
                      font=('Britannic Bold', 17), bg = '#FFEBF3', fg='#F6A2B0')
correct = Label(tab1, text=("Correct: " + str(correctnum)) , \
                            font=('Britannic Bold', 17), bg = '#FFEBF3', \
                                fg='#F6A2B0')
wrong = Label(tab1, text=("Wrong: " + str(wrongnum)),
              font=('Britannic Bold', 17), bg = '#FFEBF3', fg = '#F6A2B0')

    #Placing Labels on Grid
totalattempts.grid(row=1, column=1)
correct.grid(row=1, column=3)
wrong.grid(row=1, column=5)

    #Fillers (empty labels placed where needed to create grid)
fill00 = Label(tab1, text="       ", font=('Arial', 20), bg = '#FFEBF3')
fill02 = Label(tab1, text=(""), font=('Arial', 20), bg = '#FFEBF3')
fill04 = Label(tab1, text=(""), font=('Arial', 20), bg = '#FFEBF3')
fill12 = Label(tab1, text="              ", font=('Britannic Bold', 15), \
           bg = '#FFEBF3')
        #placing fillers 
fill00.grid(row=0, column=0)
fill02.grid(row=0, column=2)
fill04.grid(row=0, column=4)
fill12.grid(row=1, column=2)


#-------------- Clear Button --------------
clear = Button(tab1, text="Clear Counts", font=('Britannic Bold', 15), \
               bg = "#FFBA97", fg = 'white', command=reset)
clear.grid(row=10, column=5)


#--------------------------------- ALL WIDGETS ---------------------------------
#------------------------------------ tab 2 ------------------------------------

#------------ Game Settings Label --------------
settingslabel = Label(tab2, text="GAME SETTINGS", font=('Britannic Bold', 20), \
                      bg = "#FFEBF3", fg = '#F6A2B0')
settingslabel.grid(row=0, column=0, columnspan=6,pady=30)


#-------------- Label for Radiobuttons --------------
changelabel = Label(tab2, text="Select your difficulty level.", \
                    font=('Britannic Bold', 15), bg = "#FFEBF3", fg = '#F6A2B0')
changelabel.grid(row=1, column=1, pady=15, sticky=W+E)

#Radio Buttons: to change the range/level of difficulty of questions
    #defining all radiobuttons with a corresponding value, and a variable
        # selected to be assigned to that value 
selected = IntVar()

lvl1 = Radiobutton(tab2, text="Level 1 - numbers between 1-3", \
                   font=('Britannic Bold', 11), bg='white', fg = "#FFBA97", \
                   value = 3, variable = selected)
lvl2 = Radiobutton(tab2, text="Level 2 - numbers between 1-6", \
                   font=('Britannic Bold', 11), bg='white', fg = "#FFBA97", \
                   value = 6, variable = selected)
lvl3 = Radiobutton(tab2, text="Level 3 - numbers between 1-9", value = 9, \
                   font=('Britannic Bold', 11), bg='white', fg = "#FFBA97", \
                   variable = selected)
lvl4 = Radiobutton(tab2, text="Level 4 - numbers between 1-12", value = 12, \
                   font=('Britannic Bold', 11), bg='white', fg = "#FFBA97", \
                   variable = selected)

    #placing all buttons
lvl1.grid(row=2, column=1, pady=10, padx=5, sticky=W, ipadx=5, ipady=5)
lvl2.grid(row=3, column=1, pady=10, padx=5, sticky=W, ipadx=5, ipady=5)
lvl3.grid(row=4, column=1, pady=10, padx=5, sticky=W, ipadx=5, ipady=5)
lvl4.grid(row=5, column=1, pady=10, padx=5, sticky=W, ipadx=1, ipady=5)


#--------- Corresponding button to Radiobuttons ----------
lvlbutton = Button(tab2, text="Click to Change Level", \
                   font=('Britannic Bold', 11), bg = "#FFBA97", fg='white', \
                   command=changed)
lvlbutton.grid(row=6, column=1, pady=10, padx=20, ipadx=5, ipady=5)

    # Fillers
fill002 = Label(tab2, text="", font=('Arial', 30), bg = '#FFEBF3')
fill102 = Label(tab2, text="", font=('Arial', 30), bg = '#FFEBF3')
    #place fillers
fill002.grid(row=0, column=0)
fill102.grid(row=1,column=0, padx=20)


#----------- Label for Operator Combobox -----------
selectop = Label(tab2, text="Select your operator.", \
                 font=('Britannic Bold', 15), bg = "#FFEBF3", fg = '#F6A2B0')
selectop.grid(row=1, column=4, padx=40)


#------------ Selecting the Operator Combobox ------------
#set the variable changeop to the selected value of the radiobutton selected
changedop = IntVar()

#defining all radio buttons
randomizedop = Radiobutton(tab2, text="Randomized", value = 0, \
                   font=('Britannic Bold', 11), bg='white', fg = '#78D2D8', \
                        variable = changedop)
addop = Radiobutton(tab2, text="Addition", value = 1, \
                   font=('Britannic Bold', 11), bg='white', fg = '#78D2D8', \
                        variable = changedop)
subtractop = Radiobutton(tab2, text="Subtraction", value = 2, \
                   font=('Britannic Bold', 11), bg='white', fg = '#78D2D8', \
                         variable = changedop)
multiplyop = Radiobutton(tab2, text="Multiplication", value = 3, \
                   font=('Britannic Bold', 11), bg='white', fg = '#78D2D8', \
                         variable = changedop)
divisionop = Radiobutton(tab2, text="Division", value = 4, \
                   font=('Britannic Bold', 11), bg='white', fg = '#78D2D8', \
                         variable = changedop)

#placing all radiobuttons
randomizedop.grid(row=2, column=4, padx=40, ipadx=40, ipady=5, sticky=W)
addop.grid(row=3, column=4, padx=40, ipadx=52, ipady=5, sticky=W)
subtractop.grid(row=4, column=4, padx=40, ipadx=40, ipady=5, sticky=W)
multiplyop.grid(row=5, column=4, padx=40, ipadx=34, ipady=5, sticky=W)
divisionop.grid(row=6, column=4, padx=40, ipadx=53, ipady=5, sticky=W)


#------------- Selecting Operator Main Button -------------
selectopbutton = Button(tab2, text="Click to Change Operator", \
                        font=('Britannic Bold', 11), bg = '#A6EAEF', \
                        fg = 'white', command=operatorselect)
selectopbutton.grid(row=7, column=4, pady=10, ipady=5, ipadx=5)


    #Fillers
fill152 = Label(tab2, text="             ", font=('Arial', 30), bg = '#FFEBF3')
fill152.grid(row=1, column=5)


#---------- Label for Special/Other Settings -----------
specialsettings = Label(tab2, text="Special Settings", \
                 font=('Britannic Bold', 15), bg = "#FFEBF3", fg = '#F6A2B0')
specialsettings.grid(row=1, column=5, sticky=W)


#------------- Combobox for Negative Numbers -------------
#define
combo = Combobox(tab2, font=('Britannic Bold', 11))
#define the values of the box in a list
combo['values'] = ["Only Positive #'s", "Negative #'s Included"]
#set the current value selected as position 0 in list above
combo.current(0)
#place combobox onto grid
combo.grid(row=2, column=5, ipady=10, sticky=W)


#------------- Button for Combobox -------------
combobutton = Button(tab2, text="Click to Change #'s", \
                     font=('Britannic Bold', 11), bg = '#FFC0D9', \
                     fg='white', command=comboclick)
combobutton.grid(row=3, column=5, ipady=6, sticky=W)


#----------------- Skip Button -------------------
skipbutton = Button(tab1, text="Skip Question", font=('Britannic Bold', 15), \
                    bg = '#A6EAEF', fg = 'white', command=skipquestion)
skipbutton.grid(row=10, column=3)


#------------ Label for Questions Log -------------
loglabel = Label(tab2, text="Question Log", font=('Britannic Bold', 15), \
                    bg = '#FFEBF3', fg='#F6A2B0')
loglabel.grid(row=1, column=6, padx=35, sticky=W)


#-------- Questions Log Scrolled Text Widget --------
log = scrolledtext.ScrolledText(tab2,width=22,height=20)
log.grid(row=2, column=6, padx=15, rowspan=6)


#----------------- Streak Label -------------------
#initializing streak to 0
streak = 0
#defining label
streaklabel = Label(tab1, text=("Streak: " + str(streak)), \
                    font=('Britannic Bold', 15), bg = '#C3E2C2', fg = 'white')
#placing label
streaklabel.grid(row=10, column=1, ipadx=7, ipady=5)


#carry out loop for everything (keep at end)
window.mainloop()