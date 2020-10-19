import discord
from discord.ext import commands
import os
import json

#Grabbing Token & Prefix from Config
with open('./utilities/config.json') as f:
  data = json.load(f)

#Defining them in each variable for an efficient use.
token = data["token"] 
prefix = data["prefix"]


#Base Code to start up the bot.
client = commands.Bot(command_prefix = prefix)
client.remove_command('help')


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')




@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run(token)
