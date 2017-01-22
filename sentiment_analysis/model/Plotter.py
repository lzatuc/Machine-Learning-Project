from matplotlib import pyplot
from numpy import *

from data_manager.MySqlPersistenceHelper import MySqlPersistenceHelper


class Plotter:
    def __init__(self):
        self.connection = MySqlPersistenceHelper.get_connection()
        self.cursor = self.connection.cursor()

    def draw(self):
        table = 'movie_review'
        sql = 'select distinct(commentTime) from {0} order by commentTime'.format(table)
        MySqlPersistenceHelper.execute_sql(connection=self.connection,
                                           cursor=self.cursor,
                                           sql=sql)
        rows = self.cursor.fetchall()
        commentTimes = [row[0] for row in rows]
        star_count_group = []
        for commentTime in commentTimes:
            sql = '''select star, count(comment) from movie_review where commentTime = '{0}' group by star '''\
                .format(commentTime)
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            star_count_group.append(list(rows))

        index = 0
        for date, star_count in zip(commentTimes, star_count_group):
            dic = dict(star_count)
            colors = {1: 'b', 2: 'g', 3: 'r', 4: 'c', 5: 'm'}
            for star in [1.0, 2.0, 3.0, 4.0, 5.0]:
                if star in dic:
                    pyplot.bar(index, dic[star], width=1, facecolor=colors[int(star)])
                index += 1
            index += 2
        pyplot.show()

if __name__ == '__main__':
    Plotter().draw()
