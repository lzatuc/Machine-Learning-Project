import queue
import math


class KNN:

    def __init__(self, training_file, testing_file):
        self.file_paths = ["", ""]
        self.file_paths[0] = training_file
        self.file_paths[1] = testing_file
        self.labels = []
        self.training_set = []
        self.testing_set = []

    def __parse_line(self, line, idx):
        pixels = line.split(",")
        if idx == 0:
            self.labels.append(int(pixels[0]))
            pixels = pixels[1:]
        sparse_rep = []
        feature_len = len(pixels)
        for i in range(feature_len):
            val = int(pixels[i])
            if val != 0:
                sparse_rep.append((val, i))
        if idx == 0:
            self.training_set.append(sparse_rep)
        else:
            self.testing_set.append(sparse_rep)

    def __read_file(self):
        for idx in range(2):
            file = open(self.file_paths[idx])
            file.readline()
            line = file.readline()
            while line:
                self.__parse_line(line, idx)
                line = file.readline()

    @staticmethod
    def __dist(vec1, vec2):
        similarity = 0.0
        idx1 = 0
        idx2 = 0
        while idx1 < len(vec1) and idx2 < len(vec2):
            tuple1 = vec1[idx1]
            tuple2 = vec2[idx2]
            idx1_at_vector = tuple1[1]
            idx2_at_vector = tuple2[1]
            if idx1_at_vector < idx2_at_vector:
                similarity += tuple1[0] ** 2
                idx1 += 1
            elif idx1_at_vector > idx2_at_vector:
                similarity += tuple2[0] ** 2
                idx2 += 1
            else:
                similarity = (tuple1[0] - tuple2[0]) ** 2
                idx1 += 1
                idx2 += 1
        while idx1 < len(vec1):
            tuple1 = vec1[idx1]
            similarity += tuple1[0] ** 2
            idx1 += 1
        while idx2 < len(vec2):
            tuple2 = vec2[idx2]
            similarity += tuple2[0] ** 2
            idx2 += 1
        return math.sqrt(similarity)

    def knn(self):
        self.__read_file()
        k = 10
        target_labels = []
        for testing_case in self.testing_set:
            vote = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            que = queue.PriorityQueue()
            for i in range(len(self.training_set)):
                training_case = self.training_set[i]
                similarity = self.__dist(training_case, testing_case)
                que.put((similarity, self.labels[i]))
            for i in range(k):
                elem = que.get()
                vote[elem[1]] += 1
            label = vote.index(max(vote))
            print(label)
            target_labels.append(label)
        return target_labels

if __name__ == '__main__':
    target_labels = KNN('train.csv', 'test.csv').knn()
    print(target_labels)

