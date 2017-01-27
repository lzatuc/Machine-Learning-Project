import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.linear_model.logistic import LogisticRegression, LogisticRegressionCV
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report

class Classifier:
    # def __init__(self):
        # df = pd.read_csv('./train.csv')
        # print(df.head())

    def read_df(self, path):
        df = pd.read_csv(path)
        return df.values

    def gen_train_test(self, array):
        data = array[:, 1:]
        label = array[:, :1]
        train_data, train_label, test_data, test_label = train_test_split(data, label, test_size=0.2)
        return train_data, train_label, test_data, test_label

    def reduce_dimension(self, train_data, train_label, test_data, test_label):
        # for ncomponents in range(1, 2):
            ncomponents = 64
            pca = PCA(n_components=ncomponents)
            # print(train_data)
            train_data = pca.fit_transform(train_data)
        #     print(train_data)
            clf = AdaBoostClassifier()#KNeighborsClassifier(n_neighbors=15)#LogisticRegression()
            clf.fit(train_data, train_label)
            test_data = pca.transform(test_data)
            predictions = clf.predict(test_data)
            report = classification_report(test_label, predictions)
            print(report)




if __name__ == '__main__':
    path = './train.csv'
    classifier = Classifier()
    df = classifier.read_df(path)
    x_train, y_train, x_test, y_test = classifier.gen_train_test(df)
    classifier.reduce_dimension(x_train, x_test, y_train, y_test)
    # matrix = FeatureExtractor().read_df(path)[:, 1:]
    # print(matrix)
    # pca = PCA(n_components=2)
    # pca.fit(matrix)
    # print(pca.explained_variance_ratio_)


#LinearSVC with PCA
#
#              precision    recall  f1-score   support
#
#           0       0.89      0.91      0.90       841
#           1       0.83      0.94      0.88       932
#           2       0.83      0.82      0.83       876
#           3       0.70      0.88      0.78       840
#           4       0.69      0.87      0.77       830
#           5       0.78      0.55      0.65       765
#           6       0.89      0.80      0.84       830
#           7       0.85      0.88      0.87       845
#           8       0.73      0.63      0.67       834
#           9       0.82      0.63      0.71       807
#
# avg / total       0.80      0.80      0.79      8400

#Decision tree wtih PCA
#              precision    recall  f1-score   support
#
#           0       0.87      0.89      0.88       851
#           1       0.96      0.95      0.95       953
#           2       0.82      0.83      0.83       805
#           3       0.79      0.80      0.79       868
#           4       0.81      0.80      0.81       876
#           5       0.74      0.78      0.76       731
#           6       0.86      0.85      0.86       832
#           7       0.85      0.84      0.84       870
#           8       0.80      0.76      0.78       823
#           9       0.75      0.74      0.74       791
#
# avg / total       0.83      0.83      0.83      8400

#Random forest with PCA
#              precision    recall  f1-score   support
#
#           0       0.91      0.97      0.94       805
#           1       0.98      0.97      0.98       951
#           2       0.89      0.92      0.90       837
#           3       0.85      0.88      0.86       884
#           4       0.90      0.92      0.91       826
#           5       0.88      0.87      0.88       742
#           6       0.95      0.95      0.95       823
#           7       0.92      0.93      0.92       878
#           8       0.90      0.83      0.86       805
#           9       0.91      0.84      0.88       849
#
# avg / total       0.91      0.91      0.91      8400

#GradientBoostingClassifier with PCA
#              precision    recall  f1-score   support
#
#           0       0.95      0.96      0.95       829
#           1       0.97      0.97      0.97       915
#           2       0.92      0.92      0.92       841
#           3       0.91      0.89      0.90       887
#           4       0.91      0.91      0.91       821
#           5       0.89      0.89      0.89       750
#           6       0.96      0.95      0.96       852
#           7       0.94      0.92      0.93       888
#           8       0.89      0.90      0.89       791
#           9       0.88      0.91      0.89       826
#
# avg / total       0.92      0.92      0.92      8400

#Adaboosting with PCA
#              precision    recall  f1-score   support
#
#           0       0.91      0.74      0.82       842
#           1       0.86      0.95      0.90       949
#           2       0.67      0.71      0.69       831
#           3       0.71      0.62      0.66       901
#           4       0.59      0.57      0.58       829
#           5       0.48      0.50      0.49       753
#           6       0.80      0.75      0.77       794
#           7       0.80      0.69      0.74       830
#           8       0.64      0.75      0.69       821
#           9       0.48      0.56      0.52       850
#
# avg / total       0.70      0.69      0.69      8400

#rerun GradientBoostingClassifier with PCA
#              precision    recall  f1-score   support
#
#           0       0.97      0.96      0.96       812
#           1       0.98      0.97      0.97       927
#           2       0.91      0.91      0.91       809
#           3       0.93      0.88      0.91       943
#           4       0.92      0.92      0.92       783
#           5       0.88      0.91      0.89       753
#           6       0.94      0.96      0.95       811
#           7       0.94      0.94      0.94       910
#           8       0.90      0.91      0.91       843
#           9       0.89      0.90      0.89       809
#
# avg / total       0.93      0.93      0.93      8400

