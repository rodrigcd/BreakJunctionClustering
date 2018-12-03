import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join


class DataManager(object):

    def __init__(self, **kwargs):
        self.molecule_path = kwargs["molecule_path"]
        self.gold_path = kwargs["gold_path"]

    def load_data(self, n_files):

        self.gold_data = {}
        self.molecule_data = {}

        self.molecule_list = [f for f in listdir(self.molecule_path) if isfile(join(self.molecule_path, f))]
        self.gold_list = [f for f in listdir(self.gold_path) if isfile(join(self.gold_path, f))]

        print("molecules traces found", len(self.molecule_list))
        print("gold traces found", len(self.gold_list))

        for molecule in self.molecule_list[:n_files]:
            file = open(self.molecule_path + molecule, "r")
            meta, forward, backward = self.convert_file(file)
            name = molecule.split(".")[0]
            self.molecule_data[name] = {"metadata": meta,
                                           "forward_trace": forward,
                                           "backward_trace": backward}

        for gold in self.gold_list[:n_files]:
            file = open(self.gold_path + gold, "r")
            meta, forward, backward = self.convert_file(file)
            name = gold.split(".")[0]
            self.gold_data[name] = {"metadata": meta,
                                    "forward_trace": forward,
                                    "backward_trace": backward}

        return self.molecule_data, self.gold_data

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
                if separation1_found:
                    separation2_found = True
                    continue
                separation1_found = True
                continue
            if separation1_found and not separation2_found:
                row = np.array(line.split("\t")[:-1])
                forward_trace.append(row.astype(np.float))
            elif separation1_found and separation2_found:
                row = np.array(line.split("\t")[:-1])
                backward_trace.append(row.astype(np.float))

        forward_trace = np.stack(forward_trace)
        backward_trace = np.stack(backward_trace)
        return metadata, forward_trace, backward_trace


if __name__ == "__main__":

    molecule_path = "../data/molecule/"
    gold_path = "../data/gold/"

    data_manager = DataManager(molecule_path=molecule_path,
                               gold_path=gold_path)

    data_manager.load_data(n_files=10)
