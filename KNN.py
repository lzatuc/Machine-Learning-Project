import queue
import math

class KNN:

    def __init__(self, trainingFilePath, testingFilePath):
        self.trainingFilePath = trainingFilePath
        self.testingFilePath = testingFilePath

    def readTraining(self):
        label = []
        data = []
        file = open(self.trainingFilePath)
        file.readline()
        line = file.readline()
        while line:
            features = line.split(",")
            label.append(int(features[0]))
            feature_array = []
            for f in features[1:]:
                feature_array.append(int(f))
            data.append(feature_array)
            line = file.readline()
        return label, data

    def readTesting(self):
        data = []
        file = open(self.testingFilePath)
        file.readline()
        line = file.readline()
        while line:
            features = line.split(",")
            feature_array = []
            for f in features:
                feature_array.append(int(f))
            data.append(feature_array)
            line = file.readline()
        return data

    # def crossValidation(self):
        # label, training = (,)

    def dist(self, v1, v2):
        res = 0.0
        for i in range(len(v1)):
            res += (v1[i] - v2[i]) ** 2
        return math.sqrt(res)

    def knn(self):
        k  = 10
        label, trainingSet = self.readTraining()
        testingSet = self.readTesting()
        targetLabels = []
        for i in range(1):
            testingCase = testingSet[i]
            q = queue.PriorityQueue()
            vote = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for i in range(len(trainingSet)):
                trainingCase = trainingSet[i]
                d = self.dist(trainingCase, testingCase)
                q.put((d, label[i]))
            for i in range(k):
                elem = q.get()
                vote[elem[1]] += 1
            targetLabels.append(vote.index(max(vote)))
        return targetLabels


    def f(self):
        q = queue.PriorityQueue()
        q.put((3, 10))
        q.put((2, 11))
        q.put((5, 8))
        q.put((3, 7))
        while not q.empty():
            print(q.get())

if __name__ == '__main__':
    trainingFilePath = 'train.csv'
    testingFilePath = 'test.csv'
    KNN(trainingFilePath, testingFilePath).knn()
    targetLables = KNN(trainingFilePath, testingFilePath).knn()
    for label in targetLables:
        print(label)




