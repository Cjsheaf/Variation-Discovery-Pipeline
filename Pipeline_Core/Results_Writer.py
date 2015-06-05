__author__ = 'Cjsheaf'

import csv
from threading import Lock


class ResultsWriter:
    """ This class is designed to take out-of-order result data from multiple threads and write
        them to an organized csv-format file.

        All data is written to disk at the very end via the "write_results" method, since there
        is no way to know how many results there will be ahead of time, and they will not arrive
        in any particular order.
    """
    def __init__(self, csv_filename):
        self.csv_filename = csv_filename
        self.entries = {}

    def put_rmsd(self, entry_name, rmsd):
        if self.entries.get(entry_name) is None:
            self.entries[entry_name] = Entry(entry_name)
        self.entries.rmsd = rmsd

    def put_compound_scores(self, entry_name, compound_name, scores):
        """ Argument 'scores' should be a 5-item tuple (or any iterable) containing numbers. """
        if len(scores) is not 5:
            raise ValueError(
                'Attempted to save results for a compound "{compound}" in entry "{entry}"'
                'with {num_scores} number of scores. Expected 5 scores.'.format(
                    compound=compound_name,
                    entry=entry_name,
                    num_scores=len(scores)
                )
            )

        if self.entries.get(entry_name) is None:
            self.entries[entry_name] = Entry(entry_name)

    def sanity_check_entry(self):
        for e in self.entries:
            if e.rmsd is None:
                raise RuntimeError('Entry "{entry}" has no RMSD!'.format(entry=e.name))
            if len(e.compounds) is 0:
                raise RuntimeError('Entry "{entry}" has no compounds!'.format(entry=e.name))

            for c in e.compounds:
                if c.mseq is None:
                    raise NotImplementedError

    def write_results(self):
        csv_file = open(self.csv_filename, 'w', newline='')
        writer = csv.writer(self.csv_file)


class Entry:
    def __init__(self, name):
        self.name = name
        self.rmsd = None
        self.compounds = {}

    def add_compound(self, compound_name, compound):
        self.compounds[compound_name] = compound


class Compound:
    def __init__(self, name):
        self.name = name
        self.rseq = None
        self.mseq = None
        self.rmsd_refine = None
        self.e_conf = None
        self.e_place = None
        self.e_score1 = None
        self.e_score2 = None
        self.e_refine = None
