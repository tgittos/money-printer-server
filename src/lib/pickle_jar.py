import pickle
import os
import pandas

class PickleJar:

    def __init__(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.base_path = os.path.join(current_path, "../..", 'pickle_jar')

    def pickle_exists(self, filename):
        final_path = os.path.join(self.base_path, filename)
        return os.path.exists(final_path)

    def read_pickle_file(self, filename):
        final_path = os.path.join(self.base_path, filename)
        if os.path.exists(final_path):
            with open(final_path, 'rb') as f:
                return pickle.load(f)
        else:
            return []

    def read_pickle_dataframe(self, filename):
        final_path = os.path.join(self.base_path, filename)
        if os.path.exists(final_path):
            return pandas.read_pickle(final_path)
        else:
            return []

    def write_pickle_file(self, filename, data):
        final_path = os.path.join(self.base_path, filename)
        with open(final_path, 'w+b') as f:
            pickle.dump(data, f)
        return None

    def write_pickle_dataframe(self, filename, dataframe):
        final_path = os.path.join(self.base_path, filename)
        dataframe.to_pickle(final_path)
        return None
