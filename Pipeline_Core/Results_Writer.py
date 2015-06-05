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

    def put_compound_scores(self, entry_name, scores):
        """ Argument 'scores' should be a 9-item tuple or list. """
        if len(scores) is not 9:
            raise ValueError(
                'Attempted to save results for a compound "{compound}" in entry "{entry}"'
                'with {num_scores} number of results. Expected 9 results.'.format(
                    compound=scores(0),
                    entry=entry_name,
                    num_scores=len(scores)
                )
            )

        if self.entries.get(entry_name) is None:
            self.entries[entry_name] = Entry(entry_name)
        self.entries[entry_name].compounds.append(
            Compound(scores[1], scores[2], scores[3], scores[4], scores[5], scores[6], scores[7],
                     scores[8], scores[9])
        )

    def _sanity_check_entry(self):
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
        writer.writerow('name', 'rmsd', 'compound', 'rseq', 'mseq', 'rmsd_refine', 'e_conf',
                        'e_place', 'e_score1', 'e_score2', 'e_refine')

        for e in self.entries:
            writer.writerow(e.name, e.rmsd)
            for c in e.compounds:
                writer.writerow('', '', c.name, c.rseq, c.mseq, c.rmsd_refine, c.e_conf, c.e_place,
                                c.e_score1, c.e_score2, c.e_refine)


class Entry:
    def __init__(self, name):
        self.name = name
        self.rmsd = None
        self.compounds = []

    def add_compound(self, compound_name, compound):
        self.compounds[compound_name] = compound


class Compound:
    def __init__(self, name, rseq, mseq, rmsd_refine, e_conf, e_place, e_score1, e_score2, e_refine):
        self.name = name
        self.rseq = rseq
        self.mseq = mseq
        self.rmsd_refine = rmsd_refine
        self.e_conf = e_conf
        self.e_place = e_place
        self.e_score1 = e_score1
        self.e_score2 = e_score2
        self.e_refine = e_refine
