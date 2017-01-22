from FileIOManager import FileIOManager
from math import log


class NaiveBayes:
    """
    p(c|vec) = p(c, vec) / p(vec) = p(vec|c) * p(c) / p(vec) ∝ p(c) * p(v1, v2, ..., vn | c) = p(c) * p(v1|c) *...* p(vn|c)

    log(p(c|vec)) = log(p(c)) + log(p(v1|c) + ... + log(p(vn|c))

    """
    num_of_labels = 10

    def __init__(self, training_path, testing_path):
        self.file_io_manager = FileIOManager(training_path, testing_path)
        self.file_io_manager.read_file()

    def __get_class_prob(self, labels):
        probs = [0 for i in range(NaiveBayes.num_of_labels)]
        total = len(labels)
        class_count = [0 for i in range(NaiveBayes.num_of_labels)]
        for label in labels:
            class_count[label] += 1
        for i in range(len(probs)):
            probs[i] = class_count[i] / total
        return probs

    def __get_within_label_count_and_label_count(self, training_set, labels):
        within_class_count = [{} for i in range(NaiveBayes.num_of_labels)]
        label_count = [0 for i in range(NaiveBayes.num_of_labels)]
        for i in range(len(training_set)):
            label = labels[i]
            training_case = training_set[i]
            label_count[label] += len(training_case)
            for val in training_case:
                if val in within_class_count[label]:
                    within_class_count[label][val] += 1
                else:
                    within_class_count[label][val] = 1
        # for label in range(labels):
        #     dict = within_class_prob[label]
        #     for key, item in dict.items():
        #         dict[key] = (item + 1) / (label_count[label] + 1)
        return within_class_count, label_count

    def __predict(self, probs, within_label_count, label_count, testing_case):
        predict_probs = [0 for i in range(10)]
        for label in range(NaiveBayes.num_of_labels):
            prob = log(probs[label])
            for val in testing_case:
                if val in within_label_count[label]:
                    count = within_label_count[label][val]
                else:
                    count = 1
                prob += log((count + 1) / (label_count[label] + 1))
            predict_probs[label] = prob
        return predict_probs.index(max(predict_probs))

    def naive_bayes(self):
        labels = self.file_io_manager.labels
        training_set = self.file_io_manager.training_set
        testing_set = self.file_io_manager.testing_set
        probs = self.__get_class_prob(labels)
        within_label_count, label_count = self.__get_within_label_count_and_label_count(training_set, labels)
        target_labels = []
        for testing_case in testing_set:
            predict_label = self.__predict(probs, within_label_count, label_count, testing_case)
            target_labels.append(predict_label)
        return target_labels


if __name__ == '__main__':
    target_labels = NaiveBayes('train.csv', 'test.csv').naive_bayes()
    print(target_labels)