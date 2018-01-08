from collections import Counter
import csv


def read_doc():
    with open('D:/text_mining/test_textmining.csv', 'r') as csvreader:
        csv_reader = csv.reader(csvreader)

