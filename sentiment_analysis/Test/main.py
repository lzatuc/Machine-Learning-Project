import urllib
from urllib.request import urlopen
from urllib.request import ProxyHandler
import requests

# from douban.douban.settings import MYSQL_DBNAME
# from douban.douban.settings import MYSQL_HOST
# from douban.douban.settings import MYSQL_PASSWORD
from douban.douban.settings import MYSQL_USER
import pymysql
import sys
from douban.douban.items import DoubanItem
import json

if __name__ == '__main__':
    file_name = 'data.json'
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='douban', charset='utf8')
    cursor = db.cursor()
    with open(file_name, encoding='utf-8') as file:
        for line in file:
            item = json.loads(line)
            movie_name = item['movie_name']
            comment = item['comment']
            star = item['star']
            commenter = item['commenter']
            comment_time = item['comment_time']
            sql = '''insert into movie_review (movieName, comment, star, commenter, commentTime) values ('{0}', '{1}',
                    {2}, '{3}', '{4}')''' \
                .format(movie_name, comment, star, commenter, comment_time)
            print(sql)
            cursor.execute(sql)
            db.commit()
            # content = file.readlines()

            # # db = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME)

            # sql = '''insert into movie_review (movieName, comment, star, commenter, commentTime) values ('情圣', '女主好美', 5,
            #         '豆瓣人', '2017-01-05')'''
            # res = cursor.execute(sql)
            # db.commit()
            # for row in cursor:
            #     print(row)
            # print(res)
            # proxies = ["http://111.76.129.144:808",
            #            "http://182.134.11.249:8118",
            #            "http://123.166.218.160:8118",
            #            "http://125.46.64.91:8080",
            #            "http://183.129.151.130:80",
            #            "http://222.134.134.250:8118",
            #            "http://123.66.214.34:8118"]
            # for proxy in proxies:
            #     response = requests.get('https://movie.douban.com/subject/26879060/comments?start=40&limit=20&sort=new_score&status=P', proxies={"http": proxy})
            #     print(response.content)
