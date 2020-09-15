
import argparse
import os
import preprocessing.util as util
import rdflib

class ProcessDataset(object):
    def __init__(self):
        self.entityNameIdMap = util.EntityNameIdMap()
        self.entityNameIdMap.init_gerbil_compatible_ent_id()
        self.unknown_ent_name = dict()
        self.no_english_uri = dict()
        self.all_gm_cnt = dict()
        self.englishuri_gm_cnt = dict()
        self.valid_gms = dict()

    def process(self, filepath, filename):
        #the name of the dataset. just extract the last part of path
        unknown_ent_name = 0
        print("Dataset", filename, filepath)
        g = rdflib.Graph()
        dataset = g.parse(filepath)
        print("graph has %s statements." % len(g))
        print(g.serialize(format='n3'))

if __name__ == "__main__":
    pass
