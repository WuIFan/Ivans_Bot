import requests
from bs4 import BeautifulSoup
import re

web = 'https://leetcode.com/denny91002/'
r = requests.get(web)
print(r.status_code)
soup = BeautifulSoup(r.text, 'lxml')
progesses = soup.find_all('li',class_="list-group-item")
prefer = ['Finished Contests','Rating','Global Ranking','Solved Question','Accepted Submission','Acceptance Rate']
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
for da in data:
    if da[0] in prefer:
        print(da)
# print(data)
    