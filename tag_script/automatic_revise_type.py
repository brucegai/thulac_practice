# this script used for modify type of all word segment results,especially type revise
# # -*- coding: utf-8 -*-
import csv,re


def import_data():
    word_list = []
    with open('E:/test/test_debug.csv', 'r') as csvreader:
        csv_reader = csv.reader(csvreader)
        next(csv_reader)
        for line in csv_reader:
            word_list.append(line[2].split('^')[:2])
    return word_list








