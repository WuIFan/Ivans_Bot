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


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'Load {extension} Successfully')


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'Unload {extension} Successfully')

@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f'Reload {extension} Successfully. Use command "={extension}" to get list of commands')

for file in os.listdir('./cmds'):
    if file.endswith('.py'):
        bot.load_extension(f'cmds.{file[:-3]}')

if __name__ == "__main__":
    bot.run(setting['TOKEN'])
