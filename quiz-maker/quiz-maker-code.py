#Name: Jiya Shah
#ID: 918951
#Description: This is a quiz maker program, designed to help create and play
#              short 10 question quizzes. The program has the ability to add,
#              delete, and play questions. A data file must be provided for
#              this program to be played. 

#importing needed libraries
import random
import time 

def file_opener():
    """Opens the questions data file, and reads all questions.

    Args: None

    Returns:
    all_questions(list): All the questions in the data file.
    file_name(str): Name of the questions data file.
    """
    file_name = "questions_data_2.py" #file name
    file = open(file_name, 'r') #opens to read file
    all_questions = file.readlines() #obtains all questions in file
    file.close() #closes file
    
    return all_questions, file_name #returns all questions and file_name

def main_menu():
    """Displays the main menu.

    Args: None

    Returns: None
    """
    #stores colours as variables for later use
    RED ='\033[31m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

    print(RED+("\n" + "✭"*18)+RESET) #prints main menu
    print(RED+"✭          Main Menu        ✭"+RESET)
    print(RED+("✭"*18)+RESET)
    print(RED+"\n1. Play\n2. Create\n3. Exit"+RESET)

def extra_settings(all_questions):
    """Runs all necessary input validation for extra settings.

    Args:
    all_questions(list): list of all questions in data file

    Returns:
    user_num(int): number of questions user wants to play
    time_limit(int): the time limit per question
    """
    #stores colours as variables for later use
    RED ='\033[31m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    user_num = 10 #iniatilizes number of questions as 10
    time_limit = 0 #initializes no time limit
    choices_list = ['y', 'Y', 'N', 'n'] #list of possible choices
    data_type = str 
    prompt = '\nWould you like to change settings (Y/N)? '
    #gets confirmation from the user
    confirmation = (input_validator(choices_list, data_type, prompt)).capitalize()
    
    done = False #iniatlizes done to enter and continue loop
    while not done: #while done is false
        if confirmation == 'Y': #if user confirmed yes
            try: #tru to obtain the following
                #get the number of questions from the user
                user_num = int(input("\nHow many questions would you like per quiz?: "))
                #get the time limit from the user
                time_limit = int(input("\nHow many seconds would you like the time limit to be per question?\n(Enter 0 for no time limit): "))
                #if the number of questions or time limit is not valid 
                if user_num <= 0 or time_limit < 0:
                    print("\nPlease enter a valid integer number greater than 0.")
                #elif if it is valid
                elif user_num <= len(all_questions):
                    done = True #exits loop 
                else: #if the number of questions is less than the num of questions
                    #in the file itself
                    print("\nThe number of questions exceeds the total number of \
questions in the data file. There are", len(all_questions), "in the data file.")
            except: #if invalid input
                print("\nPlease enter a integer number.")
        else: #if confirmation is No
            return user_num, time_limit #return default values of both
    else: #print quiz is starting
        print(RED+"\nStarting Quiz..."+RESET) 
        
    return user_num, time_limit #return the two values
        
        
def input_validator(choices_list, data_type, prompt):
    """Use for a variety of input validation.

    Args:
    choices_list(list): List of options the user can pick from.
    data_type: The expected data type of the user's input
    prompt(str): Prompt to get user's input.

    Returns:
    user_choice: The user's input from the choices_list.
    """
    
    done = False #iniatilizes done as false
    
    while not done: #while done is fase
        try: 
            user_choice = data_type(input(prompt)) #tries to obtain user's_input
            
            if user_choice in choices_list: #if the user's input is valid
                done = True #exit loop
            else:
                print("\nPlease choose a option from above.\n") #print error msg
        except:
            print("\nInvalid data type, please try again.\n")
    
    return user_choice #returns user choice

def play(): 
    """Displays the play menu.

    Args: None

    Returns: None
    """
    
    #stores colours as variables for later use
    RED ='\033[31m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    PURPLE = '\033[35m'
    
    print("\n" + PURPLE+"♥♡"*11+RESET) #prints decorative border
    print(PURPLE+"♥     Play Menu    ♥"+RESET)
    print(PURPLE+"♥♡"*11+RESET)
    #prints play menu
    print(BOLD+PURPLE+"\n1. Start a New Quiz\n2. Back to Main Menu"+RESET) #prints play menu
        
    
def create():
    """Displays the create menu.

    Args: None

    Returns: None
    """
    #stores colours as variables for later use
    BLUE = '\033[34m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

    print(BLUE+("\n"+ "✧✦"*8)+RESET) #prints decorative border
    print(BLUE+"✧       Create Menu      ✦"+RESET)
    print(BLUE+("✧✦"*8)+RESET)

    #prints create menu
    print(BLUE+BOLD+"\n1. Add Question\n2. Delete Question\n3. Back to Main Menu"+RESET)
    
def do_quiz():
    """Starts a new quiz for the user, displays questions, gets answers,
displays score.

    Args: None

    Returns: None
    """
    
    #stores colours as variables for later use
    BOLD = '\033[1m'
    RESET = '\033[0m'
    RED ='\033[31m'
    GREEN = '\033[32m'
    PURPLE = '\033[35m'

    
    all_questions, file_name = file_opener() #calls function to obtain file info
    if len(all_questions)<10:
        print("\nQuestion file must have a minimum of 10 questions.")
        return
    
    num_of_questions, time_limit = extra_settings(all_questions) #obtains
    #other extra settings from the user 

    random.shuffle(all_questions) #shuffles all questions
    ten_questions = all_questions[:num_of_questions] #gets a list of 10 questions
    correct_count = 0 #iniatilizes count as 0
             
    for i in ten_questions: #for every question in the ten questions
        question, a, b, c, d, ans = i.split(" | ") #obtain parts
        choice_list = [a, b, c, d] #choices list user can choose from
        
        wrong_choices = [] #initalizes list of incorrect choices
        for option in choice_list: #for every option in the choicelist
            if option != ans: #if the option is not the right answer
                wrong_choices.append(option) #add it to wrong choices list
                
        random.shuffle(choice_list) #shuffles all multiple choice for more
        #challenging randomization
        a = choice_list[0] #iniatlizes variables 
        b = choice_list[1]
        c = choice_list[2]
        d = choice_list[3]
        
        if time_limit != 0: #if the time_limit is not set to 0 by user
            start_time = time.time() #start time recording
        
        print(BOLD+"\n", question+RESET, sep="") #prints question
        print(BOLD+"\n[A]"+RESET, a, BOLD+"\n[B]"+RESET, b, BOLD+"\n[C]"+RESET, c, BOLD+"\n[D]"+RESET, d) #prints choices
        
        choices_list = ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', "hint", "Hint"]
        #list of possible choices for input validation

        choices_dict = { #dictionary to reference user's choices 
            'a': a,
            'b': b,
            'c': c,
            'd': d
            }
        
        reverse_choices_dict = { #opposite dictionary to get printing letters 
            a: '[A]',
            b: '[B]',
            c: '[C]',
            d: '[D]'
            }
        
        data_type = str #needed for input validator 
        prompt = "\nEnter answer or Enter 'hint' for a clue: " 
        
        #obtain user answer and validates it
        user_answer = input_validator(choices_list, data_type, prompt).lower()
        
        idx = 0 #default index to 0
        hint_used = False #no hints used yet
        
        while user_answer == 'hint': #if the user's input is hint
            if user_answer == 'hint' and hint_used == False:
                #choose an inccorect choice to remove
                removed_choice = random.choice(wrong_choices)
                print("One Choice Eliminated.") 
                print(BOLD+"\n", question+RESET, sep="") #reprint question
                for i in choice_list: #reprint all choices except removed one
                    if i != removed_choice: #print all choices but removed one
                        print(BOLD+reverse_choices_dict[i]+RESET, i)
                        idx += 1 #next index
                hint_used = True #hint is used, set to True
                #get input again from user
                user_answer = input_validator(choices_list, data_type, prompt).lower()
            else: #if the user asks for hint a second time, display no 
                print(RED+"\nYou've already used your hint."+RESET)
                #get input from user until user_answer != 'hint'
                user_answer = input_validator(choices_list, data_type, prompt).lower()
            
        if time_limit != 0: #again if time limit is not 0
            end_time = time.time() #stop recording time
        
            time_passed = end_time - start_time #calculate time passed
            
            if time_passed > time_limit: #if the time that has passed is
                #greater than the limit
                #print user didnt enter in time
                print(RED+"\nYou didn't answer in time! No points earned."+RESET)
                print(BOLD+"The answer was:", ans+RESET) #print correct ans
            else:
                print(f"\nYou answered in {time_passed:.2f} seconds!") #print how long
                #it took user to answer
                if choices_dict[user_answer].strip() == ans.strip():
                #if the answer in the dict is the same as the ans 
                    print(GREEN+BOLD+"\nCorrect!"+RESET) #print correct statement
                    correct_count += 1 #increase correct count
                else: #else the answer was incorrect, display correct answer
                    print(RED+BOLD+"\nIncorrect! The answer was:", ans+RESET)
        else: 
            if choices_dict[user_answer].strip() == ans.strip():
                #if the answer in the dict is the same as the ans 
                print(GREEN+BOLD+"\nCorrect!"+RESET) #print correct statement
                correct_count += 1 #increase correct count
            else: #else the answer was incorrect, display correct answer
                print(RED+BOLD+"\nIncorrect! The answer was:", ans+RESET)
    
    percentage = (correct_count / num_of_questions) * 100 #calculate the percentage mark
    print(BOLD+"\nYou got", correct_count, "out of", num_of_questions, "correct."+RESET)
    #display correct count
    print(BOLD+"\nYour score is ", percentage, "%\n"+RESET, sep="")

def add_question():
    """Adds question to the data file.

    Args: None

    Returns: None
    """
    
    BOLD = '\033[1m'
    RESET = '\033[0m'
    RED ='\033[31m'
    
    all_questions, file_name = file_opener() #obtain all_questions from file 
    
    question = input(BOLD+"\nAdd the text for the question you would like to add. \
Press enter when done.\n"+RESET)
    #gets user input for question text
    print(BOLD+"\nNow enter the options for choice A, B, C, D. Press enter after \
each entry."+RESET)
    a = input("[A] ") #gets user input for all variables 
    b = input("[B] ")
    c = input("[C] ")
    d = input("[D] ")
    
    choices_list = ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd']
    #list of possible choices
    data_type = str
    prompt = "\nNow enter the answer (A, B, C or D): "
    #gets user input for correct choice
    
    ans = (input_validator(choices_list, data_type, prompt)).capitalize()
    #gets answer
    
    choices_list = ['y', 'Y', 'N', 'n'] #confirms if user wants to add the question
    prompt = RED+BOLD+'\nWould you like to add this question to the database (Y/N)? '+RESET
    confirmation = (input_validator(choices_list, data_type, prompt)).capitalize()
    
    if confirmation == 'Y': #if yes, continues to add 
        question_to_add = f'"{question}" | "{a}" | "{b}" | "{c}" | "{d}" | "{ans}"'
        
        file = open(file_name, 'a') #opens file for appending
        file.write(question_to_add + '\n') #appends question
        file.close()
        print(BOLD+"\nQuestion added to ", file_name, "!"+RESET, sep="") #displays added
        
    else:
        return #if user doesn't want to add question returns to play menu
    
def delete_question():
    key = input("\nTo delete a question, you will need to enter a key phrase \
to search for in the database. The first question to contain this key phrase \
will be deleted. Press enter when done.\n")
    
    BOLD = '\033[1m'
    RESET = '\033[0m'
    RED ='\033[31m'
    GREEN = '\033[32m'
    
    all_questions, file_name = file_opener() #obtain all questions from the file
    
    question_matches = [] #initialize question matches 
    confirmation = None
    
    for question in all_questions: #for every question in the file
        if key.lower() in question.lower(): #if the key word is in the file
            question_matches.append(question) #add to matches list
    
    if question_matches == []: #if the matches list is empty
        print(RED+"\nSorry, no question matches your key phrase in the \
database. \nNo question was deleted."+RESET)
        return #exit function
             
    print(GREEN+"\nMatches found: "+RESET)
    match_index = 1
    for i in range(len(question_matches)): #for the length of the matches list
        #print all matched questions in nice format
        print(match_index, ".", question_matches[i].split(" | ")[0], sep="")
        match_index += 1 #running total
        
    choices_list = [] #list of options for user to choose from
    for i in range(len(question_matches)): #for every number in the length of matches
        choices_list.append(i+1) #add number to the choices list
        #print(choices_list)
            
    data_type = int
    prompt = BOLD+"\nPlease choose question # you would like to delete: "+RESET
    #gets user choice for which question to delete
    user_choice = (input_validator(choices_list, data_type, prompt)) - 1
            
    choices_list = ['Y', 'y', 'N', 'n'] #confirmation list
    data_type = str
    prompt = RED+'\nWould you like to delete the above question(s) (Y/N)?:'+RESET
    #gets confirmation from the user
    confirmation = input_validator(choices_list, data_type, prompt).lower()
        
    if confirmation == 'y': #if confirmation is yes
        with open(file_name, 'w') as file: #open file to overwrite
            for question in all_questions: #for every question in the orig. file
                if question != question_matches[user_choice]: #if the q is not
                    #the question to be deleted
                    file.write(question) #add it to the file
            print(RED+BOLD+"\nQuestion deleted."+RESET) #print it is deleted
            return
    else: #if the user choses no, print no question deleted
        print(BOLD+"\nNo question was deleted."+RESET)
        return #exit function
            
def main():
    """Main function, calls all other functions.

    Args: None

    Returns: None
    """
    
    try: #try to obtain all questions from file 
        all_questions, file_name = file_opener()

    except: #if no file is found, error msg 
        print("Data File not found. Please create a questions data file first.")

    prompt = "\nMy option is: " 
    program_playing = True
    while program_playing == True: #while the program is playing
            
        main_menu() #display main menu
        choices_list = [1, 2, 3]
        data_type = int
        prompt = "\nMy option is: "
    
        user_choice = input_validator(choices_list, data_type, prompt) #get users choice from list
        
        done = False 
        while not done: #loop to enter secondary options after main menu 
            if user_choice == 1: #if user choice is one enter play menu
                choice2 = None
                while choice2 != 2:
                    
                    play() #displays play
                    choices_list = [1, 2]
                    data_type = int
                    
                    choice2 = input_validator(choices_list, data_type, prompt)
                    #gets choice2 from user
                                
                    if choice2 == 1:
                        if len(all_questions) < 10: #if the length of the questions is less than 10
                            print("\nQuestion file must have a minimum of 10 questions.\n")
                        else:
                            do_quiz() #play quiz
                                        
                done = True #exit loop
                
            elif user_choice == 2: #enter create menu
                choice2 = ""
                while choice2 != 3: 
                    create()
                    choices_list = [1, 2, 3]
                    data_type = int
                    
                    choice2 = input_validator(choices_list, data_type, prompt) 
                    #gets choice2
                    
                    if choice2 == 1: #if the choice is to add a question
                        add_question()

                    elif choice2 == 2: #if choice is to delete question
                        delete_question()
                        
                done = True #exit loop
            else: #exit 
                print("\nThanks for playing!")
                program_playing = False #exit main program playing loop
                done = True #exit second loop 

if __name__ == '__main__':
    main()