import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error


class MovieRecommender:
    def __init__(self):
        self.header = ['user_id', 'item_id', 'rating', 'timestamp']

        self.n_users = 943  # df.user_id.unique().shape[0]
        self.n_items = 1682  # df.item_id.unique().shape[0]

        self.train_user_item = self.get_item_user_matrix('./ml-100k/ua.base')
        self.test_user_item = self.get_item_user_matrix('./ml-100k/ua.test')

        self.train_user_similarity = cosine_similarity(self.train_user_item)
        self.train_item_similarity = cosine_similarity(self.train_user_item.T)

    def predict_by_user(self, top_n_user):
        predictions = []
        for user_id in range(self.n_users):
            sorted_nb = np.argsort(-self.train_user_similarity[user_id])[1:]
            user_item_pred = []
            for item_id in range(self.n_items):
                if self.test_user_item[user_id][item_id] != 0:
                    cf_score = 0
                    n_rated_nb = 0
                    total_similarity = 0
                    for nb_id in sorted_nb:
                        nb_score = self.train_user_item[nb_id][item_id]
                        if nb_score != 0:
                            n_rated_nb += 1
                            nb_similarity = self.train_user_similarity[user_id][nb_id]
                            total_similarity += nb_similarity
                            cf_score += nb_score * nb_similarity
                            if n_rated_nb == top_n_user:
                                break
                    if total_similarity > 1e-5:
                        cf_score /= total_similarity
                    user_item_pred.append([cf_score, self.test_user_item[user_id][item_id]])
            predictions.append(user_item_pred)
        return predictions

    def predict_by_item(self, top_n_item):
        predictions = []
        for item_id in range(self.n_items):
            sorted_nb = np.argsort(-self.train_item_similarity[item_id])[1:]
            item_user_pred = []
            for user_id in range(self.n_users):
                if self.test_user_item[user_id][item_id] != 0:
                    cf_score = 0
                    n_similar_item = 0
                    total_similarity = 0
                    for nb_id in sorted_nb:
                        nb_score = self.train_user_item[user_id][nb_id]
                        if nb_score != 0:
                            n_similar_item += 1
                            nb_similarity = self.train_item_similarity[nb_id][item_id]
                            total_similarity += nb_similarity
                            cf_score += nb_score * nb_similarity
                            if n_similar_item == top_n_item:
                                break
                    if total_similarity > 1e-5:
                        cf_score /= total_similarity
                    item_user_pred.append([cf_score, self.test_user_item[user_id][item_id]])
            predictions.append(item_user_pred)
        return predictions



    def predict_by_svd(self):
        pass

    def evaluate_by_mse(self, predict_way, predictions=None, top_n=5):
        if predictions is None:
            if predict_way == 'user':
                predictions = self.predict_by_user(top_n_user=top_n)
            elif predict_way == 'item':
                predictions = self.predict_by_item(top_n_item=top_n)
            else:
                predictions = self.predict_by_svd()
        score_pred = [pred_true[0] for prediction in predictions for pred_true in prediction]
        score_true = [pred_true[1] for prediction in predictions for pred_true in prediction]
        return mean_squared_error(score_true, score_pred)

    def get_item_user_matrix(self, path):
        df = pd.read_csv(path, sep='\t', names=self.header)
        user_item = np.zeros((self.n_users, self.n_items))
        for row in df.itertuples():
            user_id = row[1] - 1
            item_id = row[2] - 1
            score = row[3]
            user_item[user_id][item_id] = score
        return user_item


if __name__ == '__main__':
    recommender = MovieRecommender()
    for top_n_user in range(1, 31):
        mse = recommender.evaluate_by_mse('item', top_n=top_n_user)
        print('top_n_item', top_n_user, 'mse', mse)

# top_n_user 1 mse 1.86352067869
# top_n_user 2 mse 1.43509009623
# top_n_user 3 mse 1.28949073857
# top_n_user 4 mse 1.21758272334
# top_n_user 5 mse 1.17545894283
# top_n_user 6 mse 1.14567680069
# top_n_user 7 mse 1.12923215515
# top_n_user 8 mse 1.11917204283
# top_n_user 9 mse 1.10812529743
# top_n_user 10 mse 1.09952008497
# top_n_user 11 mse 1.09447045468
# top_n_user 12 mse 1.08826169953
# top_n_user 13 mse 1.0839178645
# top_n_user 14 mse 1.08146412238
# top_n_user 15 mse 1.07733671617
# top_n_user 16 mse 1.07525558736
# top_n_user 17 mse 1.07317589781
# top_n_user 18 mse 1.07125458993
# top_n_user 19 mse 1.0691780544
# top_n_user 20 mse 1.06664466379
# top_n_user 21 mse 1.06535945287
# top_n_user 22 mse 1.06336137125
# top_n_user 23 mse 1.06281472653
# top_n_user 24 mse 1.06227274349
# top_n_user 25 mse 1.06151871985
# top_n_user 26 mse 1.06049965468
# top_n_user 27 mse 1.05936691561
# top_n_user 28 mse 1.05870122742
# top_n_user 29 mse 1.05780313809
# top_n_user 30 mse 1.05776037002

# top_n_item 1 mse 1.59628844115
# top_n_item 2 mse 1.23286640715
# top_n_item 3 mse 1.12034656208
# top_n_item 4 mse 1.07545181538
# top_n_item 5 mse 1.04913000654
# top_n_item 6 mse 1.03320428289
# top_n_item 7 mse 1.02017350322
# top_n_item 8 mse 1.01240616927
# top_n_item 9 mse 1.00588016076
# top_n_item 10 mse 1.00218082779
# top_n_item 11 mse 0.998927626871
# top_n_item 12 mse 0.998895673509
# top_n_item 13 mse 0.99715640989
# top_n_item 14 mse 0.995633314789
# top_n_item 15 mse 0.997369156851
# top_n_item 16 mse 0.997483537193
# top_n_item 17 mse 0.997782966563
# top_n_item 18 mse 0.996986379468
# top_n_item 19 mse 0.997187008719
# top_n_item 20 mse 0.997538441836
# top_n_item 21 mse 0.997264866152
# top_n_item 22 mse 0.998927882717
# top_n_item 23 mse 1.00082085101
# top_n_item 24 mse 1.00138279904
# top_n_item 25 mse 1.00297986909
# top_n_item 26 mse 1.00482073872
# top_n_item 27 mse 1.00503474873
# top_n_item 28 mse 1.0054530053
# top_n_item 29 mse 1.00614304427
# top_n_item 30 mse 1.00750068693