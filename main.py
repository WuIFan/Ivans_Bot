import discord
from discord.ext import commands
import json
import os

with open('setting.json', 'r') as jFile:
    setting = json.load(jFile)

bot = commands.Bot(command_prefix='=')

@bot.event
async def on_ready():
    print ('== Bot is online ==')


for file in os.listdir('./cmds'):
    if file.endswith('.py'):
        bot.load_extension(f'cmds.{file[:-3]}')

if __name__ == "__main__":
    bot.run(setting['TOKEN'])
