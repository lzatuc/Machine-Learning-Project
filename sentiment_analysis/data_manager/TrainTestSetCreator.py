from data_manager.MySqlPersistenceHelper import MySqlPersistenceHelper
import random


class TrainTestSetCreator:
    def __init__(self):
        self.connection = MySqlPersistenceHelper.get_connection()
        self.cursor = self.connection.cursor()
        self.sample_size = 3600
        self.train_size = 3000
        self.test_size = self.sample_size - self.train_size
        self.query_sqls = ['select * from movie_review where star = 1 or star = 2',
                           'select * from movie_review where star = 3',
                           'select * from movie_review where star = 4 or star = 5']
        self.insert_sqls = ['insert into train(commentId, wordSegment, star) values',
                            'insert into test(commentId, wordSegment, star) values']

    def truncate_table(self):
        truncate_sql = ['truncate train', 'truncate test']
        for sql in truncate_sql:
            MySqlPersistenceHelper.execute_sql(self.connection,
                                               self.cursor,
                                               sql)

    def trans_label(self, label):
        if label == 1 or label == 2:
            label = -1
        elif label == 3:
            label = 0
        elif label == 4 or label == 5:
            label = 1
        return label


    def get_data_from_mysql(self, sql):
        MySqlPersistenceHelper.execute_sql(self.connection,
                                           self.cursor,
                                           sql)
        rows = self.cursor.fetchall()
        sample = random.sample(rows, self.sample_size)
        return sample

    def insert_into_mysql(self, ):
        self.truncate_table()
        sample = [self.get_data_from_mysql(sql) for sql in self.query_sqls]
        train_test = [[item for sp in sample for item in sp[:self.train_size]],
                      [item for sp in sample for item in sp[self.train_size:]]]
        for data_set, insert_sql in zip(train_test, self.insert_sqls):
            for row in data_set:
                label = self.trans_label(row[5])
                sql = insert_sql + '''({0}, '{1}', {2})''' .format(row[0], row[4], label)
                MySqlPersistenceHelper.execute_sql(self.connection,
                                                   self.cursor,
                                                   sql)


if __name__ == '__main__':
    train_test_set_creater = TrainTestSetCreator()
    train_test_set_creater.insert_into_mysql()
