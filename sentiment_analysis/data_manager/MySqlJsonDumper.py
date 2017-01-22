import json

from data_manager.MySqlPersistenceHelper import MySqlPersistenceHelper


class MySqlManager:

    file = 'review.json'

    def __init__(self):
        self.connection = MySqlPersistenceHelper.get_connection()
        self.cursor = self.connection.cursor()

    def prepare_insert_statement_with(self, item):
        movie_name = item['movie_name']
        comment = item['comment']
        star = item['star']
        commenter = item['commenter']
        comment_time = item['comment_time']
        sql = '''insert into movie_review (movieName, comment, star, commenter, commentTime) values ('{0}', '{1}',
                    {2}, '{3}', '{4}')''' \
                .format(movie_name, comment, star, commenter, comment_time)
        return sql

    def persist_json_to_mysql(self):
        with open(self.file, encoding='utf-8') as file_iterator:
            for review in file_iterator:
                item = json.loads(review)
                sql = self.prepare_insert_statement_with(item)
                MySqlPersistenceHelper.execute_sql(self.connection, self.cursor, sql)

if __name__ == '__main__':
    MySqlManager().persist_json_to_mysql()
