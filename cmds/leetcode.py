import discord
from discord.ext import commands
from core.bot import Cog_Bot

import requests
from bs4 import BeautifulSoup
import re

class LeetCode(Cog_Bot):
    emoji = [':ballot_box_with_check:',':arrow_upper_right:',':chart_with_upwards_trend:',':bar_chart:',':white_check_mark:',':writing_hand:']
    prefer = ['Finished Contests','Rating','Global Ranking','Solved Question','Accepted Submission','Acceptance Rate']
    @commands.command()
    async def leet(self, ctx):
        await ctx.channel.send(f'{round(self.bot.latency*1000)}(ms)')
    @commands.command()
    async def get(self, ctx, account):
        web = 'https://leetcode.com/' + account
        r = requests.get(web)
        print(r.status_code)
        await ctx.channel.send(f'status: {r.status_code}')
        soup = BeautifulSoup(r.text, 'lxml')
        progesses = soup.find_all('li',class_="list-group-item")
        data = []
        for pro in progesses:
            texts = pro.text.split()
            d,t = '',''
            for text in texts:
                if text[0].isalpha():
                    t += text + ' '
                else:
                    d += text
            data.append([t.rstrip(),d])
        output = ''
        for da in data:
            if da[0] in self.prefer:
                print(da)
                output += f'{self.emoji[self.prefer.index(da[0])]} {da[0]} : {da[1]}\n'
        await ctx.channel.send(f'{output}')

# print(data)
def setup(bot):
    bot.add_cog(LeetCode(bot))