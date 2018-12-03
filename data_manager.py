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

if __name__ == "__main__":

    molecule_path = "../data/molecule/"
    gold_path = "../data/gold/"

    data_manager = DataManager(molecule_path=molecule_path,
                               gold_path=gold_path)

    data_manager.load_data(n_files=10)
