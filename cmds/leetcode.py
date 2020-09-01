import discord
from discord.ext import commands
from core.bot import Cog_Bot

import requests
import re
from bs4 import BeautifulSoup
from ast import literal_eval

class LeetCode(Cog_Bot):
    emoji = [':ballot_box_with_check:',':arrow_upper_right:',':chart_with_upwards_trend:',':bar_chart:',':white_check_mark:',':writing_hand:']
    rating_emoji = [':thumbsdown:',':punch:',':thumbsup:']
    prefer = ['Finished Contests','Rating','Global Ranking','Solved Question','Accepted Submission','Acceptance Rate']
    @commands.command()
    async def lcping(self, ctx):
        await ctx.channel.send(f'{round(self.bot.latency*1000)}(ms)')
    def checkRating(self, soup: BeautifulSoup):
        try:
            element = soup.find('div',class_='puiblic-profile-base')
            rating = literal_eval(element['ng-init'].replace('pc.init',''))
            print(rating[11][-1][0])
            return int(rating[11][-1][0]) - int(rating[11][-2][0])
        except Exception as e:
            print(e)
            return 0
    @commands.command()
    async def lcget(self, ctx, account):
        web = 'https://leetcode.com/' + account
        r = requests.get(web)
        print(r.status_code)
        await ctx.channel.send(f'status: {r.status_code}')
        soup = BeautifulSoup(r.text, 'lxml')
        rating_variation = self.checkRating(soup)
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
                if da[0] == 'Rating':
                    r_emoji = 2 if rating_variation > 0 else 0 if rating_variation < 0 else 1
                    output += f'{self.emoji[self.prefer.index(da[0])]} {da[0]} : {da[1]}({rating_variation}{self.rating_emoji[r_emoji]})\n'
                else:
                    output += f'{self.emoji[self.prefer.index(da[0])]} {da[0]} : {da[1]}\n'
        await ctx.channel.send(f'{output}')

# print(data)
def setup(bot):
    bot.add_cog(LeetCode(bot))