class FileIOManager:

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

    def read_file(self):
        for idx in range(2):
            file = open(self.file_paths[idx])
            file.readline()
            line = file.readline()
            while line:
                self.__parse_line(line, idx)
                line = file.readline()
