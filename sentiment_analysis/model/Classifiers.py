import pandas as pd
from data_manager.MySqlPersistenceHelper import MySqlPersistenceHelper
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV, RandomizedLogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn import metrics
from sklearn.metrics import classification_report, roc_curve, auc
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC, LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import label_binarize
from sklearn.neural_network import MLPClassifier
from sklearn.multiclass import OneVsRestClassifier


class Classifiers:
    def __init__(self):
        self.connection = MySqlPersistenceHelper.get_connection()

    def get_data(self, sql):
        df = pd.read_sql(sql, self.connection)
        return df['wordSegment'].values, df['star'].values

    def classify(self, clf, train_feature, train_label, test_feature, test_label):
        clf.fit(train_feature, train_label)
        predictions = clf.predict(test_feature)
        return metrics.classification_report(test_label, predictions)

    def make_prediction(self):
        sql = 'select wordSegment, star from train'
        train_corpus, train_label = self.get_data(sql)

        train_label = label_binarize(train_label, classes=[-1,0,1])


        vectorizer = CountVectorizer(token_pattern=r'(?u)\b\w+\b', ngram_range=(1,2))
        train_count = vectorizer.fit_transform(train_corpus)
        tfidf_transformer = TfidfTransformer()
        train_tfidf = tfidf_transformer.fit_transform(train_count)

        sql = 'select wordSegment, star from test'
        test_corpus, test_label = self.get_data(sql)
        test_label = label_binarize(test_label, classes=[-1, 0, 1])
        test_count = vectorizer.transform(test_corpus)

        test_tfidf = tfidf_transformer.transform(test_count)

        n_classes = train_label.shape[1]



        #'newton-cg','sag' and 'lbfgs'
        clfs = [#LogisticRegression(),
                # MultinomialNB(),
                LinearSVC()]
                # KNeighborsClassifier(n_neighbors=30, weights='uniform')]
                # MLPClassifier(hidden_layer_sizes=3)]


        for clf in clfs:
            y_score = OneVsRestClassifier(clf.fit(train_tfidf, train_label)).decision_function()

            fpr = dict()

            tpr = dict()

            roc_auc = dict()

            for i in range(n_classes):
                fpr[i], tpr[i], _ = roc_curve(test_label[:, i], y_score[:, i])
                roc_auc[i] = auc(fpr[i], tpr[i])

            # Compute micro-average ROC curve and ROC area
            fpr["micro"], tpr["micro"], _ = roc_curve(test_label.ravel(), y_score.ravel())
            roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

            # for i in range()

            # summary = self.classify(clf=clf,
            #                         train_feature=train_tfidf,
            #                         train_label=train_label,
            #                         test_feature=test_tfidf,
            #                         test_label=test_label)
            # print(summary)
            

if __name__ == '__main__':
    Classifiers().make_prediction()
    # for i in range(10):
    #     print()
#              precision    recall  f1-score   support
#
#          -1       0.74      0.74      0.74       190
#           0       0.82      0.85      0.84       500
#           1       0.60      0.47      0.53        96
#
# avg / total       0.77      0.78      0.77       786

#              precision    recall  f1-score   support
#
#          -1       0.77      0.73      0.75       190
#           0       0.82      0.88      0.85       500
#           1       0.65      0.46      0.54        96
#
# avg / total       0.79      0.79      0.79       786
