from FileIOManager import FileIOManager
from math import e

class LogisticRegression:

    def __init__(self, training_path, testing_path):
        self.file_io_manager = FileIOManager(training_path, testing_path)
        self.file_io_manager.read_file()

    @staticmethod
    def sigmoid(x):
        return 1.0 / (1 + e ** (-x))

