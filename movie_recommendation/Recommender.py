import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity, paired_cosine_distances
from scipy.spatial.distance import cosine


class Recommender:
    # def __init__(self):
    #     self.header = ['user_id', 'item_id', 'rating', 'timestamp']
    #     df = pd.read_csv('./ml-100k/u.data', sep='\t', names=self.header)
    #     n_users = df['user_id'].unique().shape[0]
    #     n_items = df['item_id'].unique().shape[0]
    #     train_data, test_data = train_test_split(df.values, test_size=0.2)
    #     train_data_matrix = self.gen_matrix(train_data, n_users, n_items)
    #     test_data_matrix = self.gen_matrix(test_data, n_items, n_items)
    #
    #     print(train_data_matrix)
    #     user_similarity = cosine_similarity(train_data)
    #     print(user_similarity)
    #     # item_similarity = cosine_similarity(train_data.T)

    def __init__(self):
        data = pd.read_csv('lastfm-matrix-germany.csv')
        print(data.shape)
        data_germany = data
        data_ibs = pd.DataFrame(index=data_germany.columns, columns=data_germany.columns)
        print(data_ibs)

        # print(data_germany)
        # print(data_germany.T)
        item_similarity = cosine_similarity(data_germany.T)

        # print(item_similarity.head[6].ix[:6, 2:4])


    def gen_matrix(self, data, rows, cols):
        matrix = np.zeros((rows, cols))
        for line in data:
            user_id = line[0] - 1
            item_id = line[1] - 1
            rating = line[2]
            matrix[user_id][item_id] = rating
        return matrix


if __name__ == '__main__':
    Recommender()
