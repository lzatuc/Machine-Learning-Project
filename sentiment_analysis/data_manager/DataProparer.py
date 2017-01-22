from data_manager.MySqlPersistenceHelper import MySqlPersistenceHelper


class DataPreparer:
    def __init__(self):
        self.connection = MySqlPersistenceHelper.get_connection()
        self.cursor = self.connection.cursor()
        self.tables = ['train_positive',
                       'train_neutral',
                       'train_negative',
                       'test_positive',
                       'test_neutral',
                       'test_negative']
        self.train_set_size = 3000
        self.test_set_size = 500
        self.father_table = 'movie_review'

    def create_data_repository(self, tables=''):
        if tables == '':
            tables = self.tables
        for table in tables:
            sql = 'create table if not exists {0} (commentId int(11) primary key auto_increment,' \
                  'movieName varchar(50),' \
                  'comment text,' \
                  'sentenceSegment text,' \
                  'wordSegment text,' \
                  'star double,' \
                  'commenter varchar(20),' \
                  'commentTime varchar(20))'.format(table)
            MySqlPersistenceHelper.execute_sql(self.connection,
                                               self.cursor,
                                               sql)

    def fill_data_to_repository(self, father_table, child_table, star, limit):
        sql = ''
        if len(star) == 1:
            sql = 'insert into {0} select * from {1} where star={2} limit {3}'\
                .format(child_table, father_table, star[0], limit)
        elif len(star) == 2:
            sql = 'insert into {0} select * from {1} where star={2} or star={3} limit {4}'\
                .format(child_table, father_table, star[0], star[1], limit)
        MySqlPersistenceHelper.execute_sql(self.connection,
                                           self.cursor,
                                           sql)

    # def prepare_train_test(self):
    #     tables = ['train', 'test']
    #     # self.create_data_repository(tables)
    #     sql_train = 'insert into {0} select * from {1}, {2}, {3}'\
    #         .format(tables[0], self.tables[0], self.tables[1], self.tables[2])
    #     print(sql_train)
    #     # sql_test = 'insert into {0} select * from {1}, {2}, {3}'\
    #     #     .format(tables[1], self.tables[3], self.tables[4],  self.tables[5])
    #     MySqlPersistenceHelper.execute_sql(self.connection,
    #                                        self.cursor,
    #                                        sql_train)
        # MySqlPersistenceHelper.execute_sql(self.connection,
        #                                    self.cursor,
        #                                    sql_test)


if __name__ == '__main__':
    data_preparer = DataPreparer()
    data_preparer.prepare_train_test()
    # data_preparer.create_data_repository()
    # tables = ['train_positive',
    #           'train_neutral',
    #           'train_negative',
    #           'test_positive',
    #           'test_neutral',
    #           'test_negative']
    # table_star = [[5, 4], [3], [2, 1]]*2
    # table_limit = [data_preparer.train_set_size]*3 + [data_preparer.test_set_size]*3
    #
    # for i in range(6):
    #     data_preparer.fill_data_to_repository(data_preparer.father_table, tables[i], table_star[i], table_limit[i])
