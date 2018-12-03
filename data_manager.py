import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join

class DataManager(object):

    def __init__(self, **kwargs):
        self.molecule_path = kwargs["molecule_path"]
        self.gold_path = kwargs["gold_path"]

    def load_data(self, n_files):

        self.molecule_list = [f for f in listdir(self.molecule_path) if isfile(join(self.molecule_path, f))]
        self.gold_list = [f for f in listdir(self.molecule_path) if isfile(join(self.molecule_path, f))]

        print("molecules traces found", len(self.molecule_list))
        print("gold traces found", len(self.gold_list))

        file = open(self.molecule_path + self.molecule_list[0], "r")

        self.convert_file(file)

    def convert_file(self, file):
        metadata = {}
        forward_trace = []
        backward_trace = []
        separation1_found = False
        separation2_found = False
        for i, line in enumerate(file):
            if line[0] != "@" and not separation1_found:
                if line.split(" ")[0] == "sampling":
                    meta_name = line.split("=")[0]
                    meta_name = meta_name[:-1].replace(" ", "_")
                    meta_value = line.split("=")[1].split(" ")[1]
                    metadata[meta_name] = np.float(meta_value)
                else:
                    meta_name = line.split(":")[0]
                    meta_name = meta_name[:-1].replace(" ", "_")
                    meta_value = line.split(":")[1].split(" ")[1]
                    metadata[meta_name] = np.float(meta_value)
            elif line[0] == "@":
                separation1_found = True
                #print(line)
                continue
            if separation1_found:
                row = np.array(line.split("\t")[:-1])
                forward_trace.append(row.astype(np.float))


if __name__ == "__main__":

    molecule_path = "../data/molecule/"
    gold_path = "../data/gold/"

    data_manager = DataManager(molecule_path=molecule_path,
                               gold_path=gold_path)

    data_manager.load_data(n_files=10)
