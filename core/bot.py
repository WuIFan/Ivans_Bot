import discord
from discord.ext import commands

class Cog_Bot(commands.Cog):
    def __init__(self, bot):
       self.bot = bot