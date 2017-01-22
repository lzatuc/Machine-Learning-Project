import json
import requests
from data_manager.MySqlPersistenceHelper import MySqlPersistenceHelper
import re
from time import time

class Segmentor:

    tag_url = 'http://api.bosonnlp.com/tag/analysis?space_mode=0&oov_level=4&t2s=1&special_char_conv=0'

    headers = {'X-Token': '32LFi6iQ.12850.alDbxNKXRFp6'}

    def __init__(self):
        self.connection = MySqlPersistenceHelper.get_connection()
        self.cursor = self.connection.cursor()


    @staticmethod
    def split_text_into_sentences(text):
        splits = re.split(r'[ !！,，.。?？;；~:：]', text)
        sentences = [split for split in splits if split is not '']
        punctuation = '''！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃《》「」『』【】〔〕〖〗〘〙〚〛
                        〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'''
        exclude = set(punctuation)
        return [''.join(ch for ch in sentence if ch not in exclude) for sentence in sentences]

    @staticmethod
    def get_sentence_segment_from_boson(text):
        sentences = Segmentor.split_text_into_sentences(text)
        data = json.dumps(sentences)
        resp = requests.post(url=Segmentor.tag_url, headers=Segmentor.headers, data=data.encode('utf-8'))
        return [' '.join(dict['word']) for dict in resp.json()]

    def process_segment(self):
        table = 'movie_review'
        ran_sql = 'select * from {0} where sentenceSegment is not null'.format(table)
        self.cursor.execute(ran_sql)
        row_num = len(self.cursor.fetchall())
        begin_row_num = row_num
        restart_sql = 'select * from {0} where sentenceSegment is null'.format(table)
        self.cursor.execute(restart_sql)
        records = self.cursor.fetchall()
        total_records = len(records) + row_num

        t1 = time()

        for record in records:
            comment_id = record[0]
            comment = record[2]
            sentences = '\n'.join(Segmentor.split_text_into_sentences(comment))
            sentences_segment = '\n'.join(Segmentor.get_sentence_segment_from_boson(comment, sentences))
            sql = '''update {0} set sentenceSegment = '{1}', wordSegment = '{2}' where commentId = {3}'''\
                .format(table, sentences, sentences_segment, comment_id)
            MySqlPersistenceHelper.execute_sql(self.connection, self.cursor, sql)
            row_num += 1
            print('processing {0} ...'.format(row_num))
            if (row_num - begin_row_num) % 100 == 0:
                t2 = time()
                elapsed_time = t2 - t1
                records_to_go = total_records - row_num
                print(elapsed_time, 'sec for {0}'.format(100), 'records')
                print(records_to_go, ' records left')
                print('estimate', records_to_go / 60.0, 'min to go')
                t1 = time()
        self.cursor.close()
        self.connection.close()


if __name__ == '__main__':
    sentences = [
        '非！常！可！怕！直！男！癌！婚！姻！中！年！危！机！下！的！意！淫！基！佬！设！定！是！娘！炮！非！常！傻！逼！',
        '剧作很直男癌，看的很恶心，你国那些中年男人和家庭已经够悲惨了，这部片子却拿来调侃，而且是用最低俗的模式，没有人物，都是符号，闫妮表演还行。喜剧用一个很老的套子坚持了一个多小时。过年其实可以多出去旅游或者聚会啥的，为啥非要去电影院呢？我们的娱乐项目难道只剩下电影院了咩？奇怪。',
        '一副烂片相，却意外能看下去。直男或直男癌视角性喜剧，三观不正又会很多人不喜欢吧。不过中年男的意淫不都那样。如所有中年危机一样，都是在对生活与工作失去激情，如何被梦中女神唤醒。改编自76年法国片，豆瓣叫大象骗人，剧情基本类似，包括模仿《七年之痒》。各种误会与巧合咬的比较好，不会很出戏',
        '我是笑了呀 但是笑完觉得好讨厌男主和他的朋友们呀 已婚男出轨搞事情还理直气壮了?'
    ]
    segmentor = Segmentor()
    segmentor.process_segment()
