import discord
from discord.ext import commands
from core.bot import Cog_Bot

class Base(Cog_Bot):
    @commands.command()
    async def ping(self, ctx):
        await ctx.channel.send(f'{round(self.bot.latency*1000)}(ms)')
def setup(bot):
    bot.add_cog(Base(bot))