import discord
from discord.ext import commands
from core.bot import Cog_Bot

import requests
import re
import json
import datetime
from bs4 import BeautifulSoup
from ast import literal_eval

class LeetCode(Cog_Bot):
    emoji = [':ballot_box_with_check:',':arrow_upper_right:',':chart_with_upwards_trend:',':bar_chart:',':white_check_mark:',':writing_hand:']
    rating_emoji = [':thumbsdown:',':punch:',':thumbsup:']
    prefer = ['Finished Contests','Rating','Global Ranking','Solved Question','Accepted Submission','Acceptance Rate']
    cmds = ['lcping','lcget [Account]','lccontest']
    # difficulty_format = ['easy','medium','hard']
    @commands.command()
    async def leetcode(self, ctx):
        cmd_lsit = 'Commands:\n'
        for i in range(0,len(self.cmds)):
            cmd_lsit += f'{str(i+1)}. {self.cmds[i]}\n'
        await ctx.channel.send(f'{cmd_lsit}')
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
        if not account:
            await ctx.channel.send(f'Missing [Account] Arg.')
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
        output = f':sunglasses:Account : {account}\n'
        for da in data:
            if da[0] in self.prefer:
                print(da)
                if da[0] == 'Rating':
                    r_emoji = 2 if rating_variation > 0 else 0 if rating_variation < 0 else 1
                    output += f'{self.emoji[self.prefer.index(da[0])]} {da[0]} : {da[1]}({rating_variation}{self.rating_emoji[r_emoji]})\n'
                else:
                    output += f'{self.emoji[self.prefer.index(da[0])]} {da[0]} : {da[1]}\n'
        await ctx.channel.send(f'{output}')
    @commands.command()
    async def lccontest(self,ctx):
        await ctx.channel.send(':pencil: Check contest in this week...')
        web = 'https://leetcode.com/graphql'
        data = {"query":"{\n currentTimestamp\n  allContests {\n containsPremium \n title \n startTime}}"}
        #{\n    containsPremium\n    title\n    cardImg\n    titleSlug\n    description\n    startTime\n    duration\n    originStartTime\n    isVirtual\n    company {\n      watermark\n      __typename\n    }\n    __typename\n  }\n}\n"
        result = requests.post(web,json=data)
        json_result = json.loads(result.text)
        # print(json_result)
        contest_card = ''
        cur_time = json_result['data']['currentTimestamp']
        for contest in json_result['data']['allContests']:
            if contest['startTime'] < cur_time:
                break
            else:
                start = datetime.datetime.fromtimestamp(contest['startTime']).isoformat()
                title = contest['title']
                delta = datetime.timedelta(seconds=contest['startTime'] - cur_time)
                contest_card += f'```{title}\nStarts at {start}\nStarts in {delta}\n```'
        await ctx.channel.send(contest_card)
    def pick(self):
        web = 'https://leetcode.com/problems/random-one-question/all'
        result = requests.get(web)
        print(datetime.datetime.now())
        question_name = result.url.split('/')[-2]
        lcapi = 'https://leetcode.com/graphql'
        data = {"operationName":"questionData","variables":{"titleSlug":question_name},"query":"query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n questionId\n  title\n  isPaidOnly\n difficulty\n likes\n dislikes\n similarQuestions\n}\n}\n"}
        r = requests.post(lcapi,json=data)
        print(datetime.datetime.now())
        json_result = json.loads(r.text)
        question = json_result['data']['question']
        return result.url, question
    @commands.command()
    async def lcpick(self, ctx):
        print(datetime.datetime.now())
        await ctx.channel.send('Pick One Random Question...')
        url, question = self.pick()
        '''
        if difficulty.lower() in self.difficulty_format:
            while question["difficulty"].lower() != difficulty.lower():
                await ctx.channel.send(f'Because you don\'t like {question["difficulty"]} problem, pick another one random question...')
                url, question = self.pick()
        '''
        question_card = f':scroll: Title : {question["questionId"]}. {question["title"]}\n'\
                        f':trophy: Difficulty : {question["difficulty"]}\n'\
                        f':slight_smile: Likes : {question["likes"]}\n'\
                        f':upside_down: Dislikes : {question["dislikes"]}\n'\
                        f':link: Url : {url}'
        await ctx.channel.send(question_card)
        
def setup(bot):
    bot.add_cog(LeetCode(bot))