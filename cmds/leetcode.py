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
    solved_emoji = [':pencil:',':motor_scooter:',':blue_car:',':rocket:']
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
    async def getProfile(self,account):
        web = 'https://leetcode.com/graphql'
        query = "query getUserProfile($username: String!) { allQuestionsCount{difficulty   count} matchedUser(username: $username) { submitStats { acSubmissionNum {  difficulty   count  submissions }}}}"
        data = {"operationName":"getUserProfile","variables":{"username":"denny91002"},"query":query}        
        result = requests.post(web,json=data)
        json_result = json.loads(result.text)
        return json_result
    @commands.command()
    async def lcget(self, ctx, account):
        if not account:
            await ctx.channel.send(f'Missing [Account] Arg.')
        output = f':sunglasses:Account : {account}\n'
        profile = await self.getProfile(account)
        solved = profile['data']['matchedUser']['submitStats']['acSubmissionNum']
        total = profile['data']['allQuestionsCount']
        for i in range(len(solved)):
            if solved[i]['difficulty'] == 'All':
                output += f'{self.solved_emoji[i]}Solved Qusetions : {solved[i]["count"]}/{total[i]["count"]}\n'
            else:
                output += f'{self.solved_emoji[i]}{solved[i]["difficulty"]} : {solved[i]["count"]}/{total[i]["count"]}\n'
        await ctx.channel.send(f'{output}')
    @commands.command()
    async def lccontest(self,ctx):
        await ctx.channel.send(':pencil: Check contest in this week...')
        web = 'https://leetcode.com/graphql'
        data = {"query":"{\n currentTimestamp\n  allContests {\n containsPremium \n title \n startTime}}"}
        #{\n    containsPremium\n    title\n    cardImg\n    titleSlug\n    description\n    startTime\n    duration\n    originStartTime\n    isVirtual\n    company {\n      watermark\n      \n    }\n    \n  }\n}\n"
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