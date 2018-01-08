import csv,re,sys,os
from gensim.models import Word2Vec
import tensorflow as tf
import keras as ks
import word2vec as wvc


def generate_vec():
    correct_split_word=[]
    with open('D:/word_train_2.csv', 'r') as csvreader2:
        csv_reader_2 = csv.reader(csvreader2)
        for item in csv_reader_2:
            if item[2].find('|')>0:
                front_word=item[2].split('|')[0].split('^')[0]
                rear_word=item[2].split('|')[1].split('^')[0]
                print(front_word,rear_word)
                correct_split_word.append(front_word)
                correct_split_word.append(rear_word)

            else:
                whole_word=item[2].split('^')[0]
                print(whole_word)
                correct_split_word.append(whole_word)






        # wvc.word2phrase('D:/word_train_3.txt','D:/word2vec_train_output.txt',verbose=True)
        # wvc.word2vec('D:/word2vec_train_output.txt','D:/train_result_2.bin',size=100,verbose=True)

        # mode=wvc.load('D:/train_result.bin')
        # print(mode.vectors)
        # raw_word_list = []
        # Word2Vec.load_word2vec_format()

def main():
    generate_vec()

if __name__ == '__main__':
    main()
