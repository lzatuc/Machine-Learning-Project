from numpy import *
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity, paired_cosine_distances
from scipy.spatial.distance import cosine
import random


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

    # unique users 1257
    # unique music 285

    def __init__(self):
        df = pd.read_csv('lastfm-matrix-germany.csv')
        self.np_matrix = df.drop('user', 1).values

        self.total_users = self.np_matrix.shape[0]
        self.total_songs = self.np_matrix.shape[1]
        print(self.np_matrix)

        self.train, self.test = self.train_test_split()

        self.user_similarity = cosine_similarity(self.train)
        self.item_similarity = cosine_similarity(self.train.T)

        self.user_K = 5
        self.user_top_N = 10

    def train_test_split(self):
        user_listend_songs = []
        for row in self.np_matrix:
            listened_songs = []
            for i in range(self.total_songs):
                if row[i] == 1:
                    listened_songs.append(i)
            user_listend_songs.append(listened_songs)

        train = np.zeros((self.total_users, self.total_songs))
        test = np.zeros((self.total_users, self.total_songs))
        print(user_listend_songs)

        for i in range(self.total_users):
            listened_songs = user_listend_songs[i]
            total = len(listened_songs)
            half = total / 2
            random.shuffle(listened_songs)
            for j in range(0, total):
                if j <= half:
                    train[i][listened_songs[j]] = 1
                else:
                    test[i][listened_songs[j]] = 1

        for i in range(2):
            for j in range(self.total_songs):
                if train[i][j] == 1:
                    print(j)
        return train, test


        # [82, 87, 109, 114, 129, 140, 216, 220, 222, 253, 262]
        # [3, 31, 58, 60, 68, 71, 75, 94, 97, 102, 126, 129, 148, 162, 166, 193, 199, 215, 224, 242, 251, 254, 267, 274]
        # [20, 24, 94, 113, 120, 124, 188]
        # [19, 28, 33, 58, 83, 126, 145, 152, 160, 166, 173, 185, 215, 242, 250, 269, 272]
        # [28, 33, 38, 58, 71, 142, 144, 152, 215, 216, 237, 254, 268]
        # [8, 21, 33, 46, 52, 58, 63, 101, 162, 199, 219, 223]
        # [278]

    def recommend_by_user_cf(self):
        user_recommends = []
        for u_id in range(5):#self.total_users):
            nb_with_sim = []
            for nb_id in range(self.total_users):
                if nb_id == u_id:
                    continue
                nb_with_sim.append((nb_id, self.user_similarity[u_id][nb_id]))
            nb_with_sim.sort(reverse=True, key=lambda x: x[1])
            nb_with_sim = nb_with_sim[:self.user_K]
            print('closest neighbors',nb_with_sim)

            song_id_score = []

            for song_id in range(self.total_songs):
                if self.train[u_id][song_id] == 0:
                    score = 0
                    total_sim = 0
                    for k in range(self.user_K):
                        neighbor_id = nb_with_sim[k][0]
                        neighbor_similarity = nb_with_sim[k][1]
                        score_to_add = self.train[neighbor_id][song_id] * neighbor_similarity
                        score += score_to_add
                        total_sim += neighbor_similarity
                    score /= total_sim
                    song_id_score.append((song_id, score))
            song_id_score.sort(reverse=True, key=lambda x: x[1])
            print(len(song_id_score))
            recommend = [sid_score[0] for sid_score in song_id_score][:self.user_top_N]
            user_recommends.append(recommend)
        print('user_recommends', user_recommends)
        return user_recommends



    # def recommend_by_item_cf(self):
    #     item_recommends = []
    #     for u_id in range(5):
    #         for song_id in range(self.total_songs):
    #             if train[u_id][song_id] == 0:
    #                 for s_nb in range(0, self.total_songs):
    #                     pass



    def recommend_by_matrix_factorization(self):
        pass


if __name__ == '__main__':
    Recommender().recommend_by_user_cf()#.recommend_by_user_cf()
    # a = np.zeros((1,2))
    # print(a)
    # a[0][1] = 50
    # print(a)
    # list = [20, 10, 15, 2]
    # random.shuffle(list)
    # print(list)
    # a = array([[1,2,3],[4,5,6]])
    # print(a.ndim)
    # print(a.shape[1])

