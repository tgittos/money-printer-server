import os

import pickle
import pandas

from lib.pickle_jar import PickleJar

class StonkJar(PickleJar):

    def __init__(self, ticker):
        PickleJar.__init__(self)
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.base_path = os.path.join(current_path, "../..",
                'pickle_jar',
                ticker.upper())
        if (not os.path.exists(self.base_path)):
            os.mkdir(self.base_path)

    def read_pickle_dataframe(self, filename):
        final_path = os.path.join(self.base_path, filename)
        if os.path.exists(final_path):
            return pandas.read_pickle(final_path)
        else:
            return []

    def write_pickle_dataframe(self, filename, dataframe):
        final_path = os.path.join(self.base_path, filename)
        dataframe.to_pickle(final_path)
        return None
