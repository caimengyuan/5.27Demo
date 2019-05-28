'''
爬虫代码：
    主要爬取内容：评论用户ID
                评论内容
                评分
                评论日期
                用户所在城市
'''
import pandas as pd
import random
import re

import requests
import time
from tqdm import tqdm
from lxml import etree

name_list, content_list, date_list, score_list, city_list = [], [], [], [], []
movie_name = ""


def get_city(url, i):
    time.sleep(round(random.uniform(1, 2), 2))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    cookies = {'cookie': 'bid=LAxcVnynmoY; gr_user_id=471d9c43-4122-4148-b984-7dfb6be799b6; _'
                         'vwo_uuid_v2=D1456FF1C84E9855D8AE5F497BC1A890D|cd1dea90d96780cc321884cf355e52b8; viewed="30276769"; ll="118254"; _'
                         'pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1558941424%2C%22https%3A%2F%2Fwww.google.com.hk%2F%22%5D; _'
                         'pk_ses.100001.8cb4=*; __utma=30149280.675515535.1539938544.1540100975.1558941427.3; __utmc=30149280; __'
                         'utmz=30149280.1558941427.3.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __'
                         'utmt=1; ap_v=0,6.0; __yadk_uid=EMWS9h4T90GuxrERyfsQNRArJZnwBnr7; __'
                         'gads=ID=b08b6c87d3e72570:T=1558941509:S=ALNI_MZ1SmWmiDSSvl7XL2fveUHKAxD8Iw; dbcl2="191266139:bHGKTShkoPQ"; '
                         'ck=SBbK; _pk_id.100001.8cb4=43039b8ad73694fb.1558941424.1.1558941695.1558941424.; push_noty_num=0;'
                         ' push_doumail_num=0; __utmv=30149280.19126; __utmb=30149280.5.10.1558941427'}
    res = requests.get(url, cookies=cookies, headers=headers)

    if(res.status_code == 200):
        print("\n成功获取第{}个用户城市信息！".format(i))
    else:
        print("\n第{}个用户城市信息获取失败".format(i))
    pattern = re.compile('<div class="user-info">.*?<a href=".*?">(.*?)</a>', re.S)
    # 返回和pattern模式匹配的全部字符串
    item = re.findall(pattern, res.text)   # 返回list类型
    return (item[0])  # 只有一个元素，所以直接返回


def get_content(id, page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    cookies = {'cookie': 'bid=LAxcVnynmoY; gr_user_id=471d9c43-4122-4148-b984-7dfb6be799b6; _'
                         'vwo_uuid_v2=D1456FF1C84E9855D8AE5F497BC1A890D|cd1dea90d96780cc321884cf355e52b8; viewed="30276769"; ll="118254"; _'
                         'pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1558941424%2C%22https%3A%2F%2Fwww.google.com.hk%2F%22%5D; _'
                         'pk_ses.100001.8cb4=*; __utma=30149280.675515535.1539938544.1540100975.1558941427.3; __utmc=30149280; __'
                         'utmz=30149280.1558941427.3.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __'
                         'utmt=1; ap_v=0,6.0; __yadk_uid=EMWS9h4T90GuxrERyfsQNRArJZnwBnr7; __'
                         'gads=ID=b08b6c87d3e72570:T=1558941509:S=ALNI_MZ1SmWmiDSSvl7XL2fveUHKAxD8Iw; dbcl2="191266139:bHGKTShkoPQ"; '
                         'ck=SBbK; _pk_id.100001.8cb4=43039b8ad73694fb.1558941424.1.1558941695.1558941424.; push_noty_num=0;'
                         ' push_doumail_num=0; __utmv=30149280.19126; __utmb=30149280.5.10.1558941427'}
    url = "https://movie.douban.com/subject/" +str(id)+"/comments?start="+str(page * 10)+"&limit=20&sort=new_score&status=P"
    res = requests.get(url, cookies=cookies, headers=headers)

    #re.S表示可以换行匹配
    pattern = re.compile('<div id="wrapper">.*?<div id="content">.*?<h1>(.*?) 短评</h1>', re.S)
    global movie_name
    movie_name = re.findall(pattern, res.text)[0]

    res.encoding = "utf-8"
    if(res.status_code == 200):
        print("\n第{}页短评爬取成功！".format(page + 1))
        print(url)
    else:
        print("\n第{}页爬取失败！".format(page + 1))

    with open('html.html', 'w', encoding='utf-8') as f:
        f.write(res.text)
        f.close()
    x = etree.HTML(res.text)
    for i in range(1, 21): # 每页20个评论用户
        name = x.xpath('//*[@id="comments"]/div[{}]/div[2]/h3/span[2]/a/text()'.format(i))
        score = x.xpath('//*[@id="comments"]/div[{}]/div[2]/h3/span[2]/span[2]/@title'.format(i))
        date = x.xpath('//*[@id="comments"]/div[{}]/div[2]/h3/span[2]/span[3]/@title'.format(i))
        m = '\d{4}-\d{2}-\d{2}'
        try:
            match = re.compile(m).match(score[0])
        except IndexError:
            break
        if match is not None:
            date = score
            score = ["null"]
        else:
            pass
        content = x.xpath('//*[@id="comments"]/div[{}]/div[2]/p/span/text()'.format(i))
        id = x.xpath('//*[@id="comments"]/div[{}]/div[2]/h3/span[2]/a/@href'.format(i))
        try:
            city = get_city(id[0], i)  # 调用评论用户的ID城市信息获取
        except IndexError:
            city = ''
        name_list.append(str(name[0]))
        score_list.append(str(score[0]).strip('[]\''))
        date_list.append(str(date[0]).strip('[\'').split(' ')[0])
        content_list.append(str(content[0]).strip())
        city_list.append(city)


def main(ID, pages):
    global movie_name
    for i in tqdm(range(0, pages)):  # 豆瓣只开放500条评论
        get_content(ID, i)  # 第一个参数是豆瓣电影对应的id序号，第二个参数是爬取的评论页数
        time.sleep(round(random.uniform(1, 2), 2))
    infos = {'name': name_list, 'city':city_list, 'content':content_list, 'score':score_list, 'date':date_list}
    data = pd.DataFrame(infos, columns=['name', 'city', 'content', 'score', 'date'])
    data.to_csv(movie_name + ".csv")


if __name__ == '__main__':
    main(26683723, 5)
