from dotenv import load_dotenv
import os
from discord import Client, Intents
from discord.ext import commands
import random

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = Intents.default()
intents.message_content = True # allow the bot to read messages
client = Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

#main code
colours = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'brown', 'black', 'white']

colour = random.choice(colours)

@bot.command(name='colourgame', help="Lets play a colour guessing game!")
async def colourgame(ctx, message=None):
    global colour, colours
    if message is None:
        await ctx.send("You can guess a colour to start the game!")
        return
    if message.lower() in colours:
        if message.lower() == colour:
            await ctx.send("Yes, you got it!")
        else:
            await ctx.send("Guess again!")
        return
    else:
        await ctx.send("That colour is not in my list. Guess again!")
        return
bot.run(TOKEN)