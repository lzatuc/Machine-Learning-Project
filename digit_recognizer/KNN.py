import queue
import math
from FileIOManager import FileIOManager


class KNN:
    def __init__(self, training_path, testing_path):
        self.file_io_manager = FileIOManager(training_path, testing_path)
        self.file_io_manager.read_file()

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

    def knn(self,):
        k = 10
        target_labels = []
        for testing_case in self.file_io_manager.testing_set:
            vote = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            que = queue.PriorityQueue()
            for i in range(len(self.file_io_manager.training_set)):
                training_case = self.file_io_manager.training_set[i]
                similarity = self.__dist(training_case, testing_case)
                que.put((similarity, self.file_io_manager.labels[i]))
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
