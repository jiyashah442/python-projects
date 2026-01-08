import random
import pandas as pd
from dotenv import load_dotenv
import os
from discord import Client, Intents
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = Intents.default()
intents.message_content = True  # allow the bot to read messages
client = Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)

# --------------------------------------------------------------------------

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# ------------------------------------------------------------------------

# Command to make a guess
@bot.command(name='guess', help="You can make a guess with this command!")
async def guess(ctx, *, message=None): #defines function, sets default message to None

    global current_word, scrambled_word, allowed_turns, user_turns, hints_used  #makes all variables needed global, allowing function to access them

    if message is None: #if the message is None, the bot will send a reminder to the user
        await ctx.send(f'Make a guess, the scrambled word is: {scrambled_word}')

    elif message.lower() == current_word: #if the user guesses the correct word
        await ctx.send(f'YAY! You got it! The word was: {current_word}') #bot sends out a congrats and what the word was
        save_words_played(current_word) #saves the current word to the words_played CSV before rechoosing the next word
        current_word = word_picker() #rechooses current word
        scrambled_word = word_scrambler(current_word) #scrambles the current word chosen
        user_turns = 1 #resets the users current turn to 1

        # all update the game_state dictionary, which automatically updates the progress of the user
        game_state['current_word'] = current_word
        game_state['scrambled_word'] = scrambled_word
        game_state['rounds_won'] += 1
        game_state['words_guessed'] = []
        game_state['turns_left'] = 3
        game_state['rounds_played'] += 1
        game_state['user_streak'] += 1

        # sets the hints used back to 0, for the next round
        hints_used = 0

        # sends a congrats message to the user if the streak has reached a certain number
        if game_state['user_streak'] == 3:
            await ctx.send('Three in a row, you are on fire! 🔥')
        if game_state['user_streak'] == 5:
            await ctx.send('Halfway to ten! WooHoo! 🥳')
        if game_state['user_streak'] == 15:
            await ctx.send('You have hit a streak of 15! That calls for some cake! 🎂')

        await ctx.send(f'The new scrambled word is: {scrambled_word}') #sends out message of the new scrambled word for user to guess

    else: # otherwise the user's previous guess must be wrong
        if user_turns < allowed_turns: # if the user has not exceeded number of allowed turns, let them re guess
            user_turns += 1 # update the user turn

            # adds the previous word guessed to the game_state / progress and reduces 1 turn
            game_state['words_guessed'].append(message.lower())
            game_state['turns_left'] -= 1

            await ctx.send(f'Nope, guess again! The scrambled word is: {scrambled_word}')

        else:  # if the user has exceeded the number of allowed turns, tells them they lost, sets user turn back to 1,
                # saves the word played to the words_played csv, resets the game for the next round
            user_turns = 1
            save_words_played(current_word)
            old_word = current_word
            current_word = word_picker()
            scrambled_word = word_scrambler(current_word)

            # updates the progress/game_state dictionary and hints used
            game_state['current_word'] = current_word
            game_state['scrambled_word'] = scrambled_word
            game_state['rounds_lost'] += 1
            game_state['words_guessed'] = []
            game_state['turns_left'] = 3
            game_state['rounds_played'] += 1
            game_state['user_streak'] = 0

            hints_used = 0

            await ctx.send(f"Sorry you lost, the word was: {old_word}.\nThe new scrambled word is: {scrambled_word}")

#command to check progress
@bot.command(name='progress', help='This command shows you the progress of your game, including the current word,'
                                   'scrambled word, words guessed recently, number of correct guesses and incorrect '
                                   'guesses')
async def progress(ctx, message=None):

    # sends the user their progress
    await ctx.send(f'Scrambled Word: {game_state['scrambled_word']}\n'
                    f'Words Guessed So Far This Round: {', '.join(game_state['words_guessed'])}\n'
                    f'Rounds Won: {game_state['rounds_won']}\n'
                    f'Rounds Lost: {game_state['rounds_lost']}\n'
                    f'Tries Left: {game_state['turns_left']}\n'
                    f'Rounds Played: {game_state['rounds_played']}\n'
                    f'Streak: {game_state['user_streak']}')

# command which allows the user to cheat, and see the answer to the current word
@bot.command(name='cheat', help='This command gives you the answer to the current word.')
async def cheat(ctx, message=None):

    await ctx.send(f'Current Word: {game_state['current_word']}')

#command that gives the user hints
@bot.command(name='hint', help='This command gives you a hint of what the word is.')
async def hint(ctx, message=None):
    global current_word, hints_used

    # checks how many hints the user has used, if 0, gives them the first hint
    if hints_used == 0:
        hints_used += 1
        await ctx.send(f'The first letter of the word is: {current_word[0]}')
    # if the user has already used the first hint in the round, gives them the second hint
    elif hints_used == 1:
        hints_used += 1
        await ctx.send(f'The last letter of the word is: {current_word[-1]}')
    # otherwise, if the user already used both hints, tells the user they have no hints left
    else:
        await ctx.send(f'Sorry you have run out of hints.\nRemember the first letter of the '
                       f'word is: {current_word[0]} and the last letter is: {current_word[-1]}')

# command to start new game and resets all game progress back to default
@bot.command(name='new_game', help='This command resets all progress and starts a new game.')
async def new_game(ctx, message=None):
    global current_word, scrambled_word, user_turns, hints_used

    current_word = word_picker()  # sets the new current word
    scrambled_word = word_scrambler(current_word)  # scrambles the new current word

    # resets game_state to beginning of new game
    game_state['current_word'] = current_word
    game_state['scrambled_word'] = scrambled_word
    game_state['rounds_won'] = 0
    game_state['rounds_lost'] = 0
    game_state['words_guessed'] = []
    game_state['turns_left'] = 3
    game_state['rounds_played'] = 0
    game_state['user_streak'] = 0

    hints_used = 0

    # clears the words_played df and updates the csv back to empty
    cleared_words_played_df = pd.DataFrame(columns=['words_played'])
    cleared_words_played_df.to_csv('words_played.csv', index=False)

    await ctx.send(f'You have started a new game! Your new scrambled word is: {scrambled_word}')

#command to change the category of words
@bot.command(name='change_category', help='This command allows you to choose from a category of words to play from.\n'
                                          'Categories Include; 4_letter_words, 5_letter_words, 6_letter_words, '
                                          'long_words, foods, animals, countries & randomized.\nTo choose a category'
                                          'please use: !change_category category_name_here')
async def change_category(ctx, message=None):
    global category
    # initializes the list of categories availible
    list_of_categories = ['4_letter_words', '5_letter_words', '6_letter_words',
                          'long_words', 'foods', 'animals', 'countries', 'randomized']
    # if users message is none, reminds them to reply with a category name
    if message is None:
        await ctx.send(f'If you would like to change the category, please reply using this command with one of the '
                       f'following categories:\n4_letter_words, 5_letter_words, 6_letter_words, long_words, foods, '
                       f'animals, countries or randomized\nThe current category is: {category}')
    # if the message is in the list, updates the category for the next round to the user's pick
    elif message.lower() in list_of_categories:
        category = str(message.lower())
        await ctx.send(f'Category successfully changed!\nThe new category is: {category}.\nThe new scrambled'
                       f' word is: {scrambled_word}')
    # otherwise reminds the user to only reply with a category in the list
    else:
        await ctx.send(f'Category not found. Please try again\nRemember to use exactly the name of one of these categories:\n '
                       f'4_letter_words, 5_letter_words, 6_letter_words, long_words, foods, animals, '
                       f'countries or randomized\nThe current category is: {category}')

    return

#function that picks the word from the csv and returns it under variable current_word
def word_picker():
    global category, current_word

    words_csv = pd.read_csv('words.csv')

    words = words_csv[category].tolist()

    current_word = random.choice(words)

    # reads the words_played csv, and converts all the words played in the csv to a list
    try:
        words_played_df = pd.read_csv('words_played.csv')
        played_words = words_played_df['words_played'].tolist()
    # if none are found the words played are set to a empty list
    except FileNotFoundError:
        played_words = []

    # if the word is in the list, and its the same word chosen, recalls the function to choose a new word
    for word in played_words:
        if word == current_word:
            word_picker()

    # otherwise word is returned
    return current_word

#function that scrambles the current word
def word_scrambler(current_word):

    # makes all the characters in the word into a list, so it can be shuffled and then joined as 1 string
    word_list = list(current_word)
    random.shuffle(word_list)
    scrambled_word = ''.join(word_list)

    # if by chance the scrambled word is not scrambled properly, recalls the function to scramble it again
    if scrambled_word == current_word:
        word_scrambler(current_word)
    else: # otherwise the scrambled word is returned
        return scrambled_word

# function to append the current word to 'words_played.csv'
def save_words_played(current_word):
    words_played_df = pd.read_csv('words_played.csv')

    # appends the previously played word
    new_data = pd.DataFrame({'words_played': [current_word]})
    updated_df = pd.concat([words_played_df, new_data], ignore_index=True)

    # converts the df into the csv
    updated_df.to_csv('words_played.csv', index=False)

# ---------------------------------------- MAIN CODE ----------------------------------------

#initializes the first current word and default category
category = 'randomized'
current_word = word_picker()

#iniatializes the scrambled version of the first current word
scrambled_word = word_scrambler(current_word)

#iniatializes the users turn to 1 and number of allowed turns to 3
user_turns = 1
allowed_turns = 3

#initialize game state
game_state = {
    'current_word': current_word,
    'scrambled_word': scrambled_word,
    'words_guessed': [],
    'rounds_won': 0,
    'rounds_lost': 0,
    'turns_left': 3,
    'rounds_played': 0,
    'user_streak': 0

}

#initialize hints used
hints_used = 0

# ---------------------------------------------------------------------------------------------------------------------
bot.run(TOKEN)