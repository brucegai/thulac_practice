# -*- coding:utf-8 -*-
# coding=utf-8

import numpy as np

import os
import sys
import os
import tensorflow as tf
import pandas as pd

FLAGS = tf.app.flags.FLAGS


def w2v_generate(address, cvecPath, wvecPath, dicPath):
    # load character vec
    vec = open(cvecPath)
    dic = {}
    for line in vec.readlines()[1:]:
        voblist = line.strip().split(' ')
        dic[voblist[0]] = list(map(float, voblist[1:]))
    vec.close()
    # wordDic = open('Dic.txt','r')
    # wordDict = {}
    # for line in wordDic.readlines():
    #     voblist = line.strip().split('\t')
    #     wordDict[voblist[0]]=map(float,voblist[1])
    # wordDic.close()
    # wordVector = open('wordVec.txt','r')
    # wordvector = {}
    # for line in wordVector.readlines()[1:]:
    #     voblist = line.strip().split('\t')
    #     wordvector[voblist[0]]=map(float,voblist[1])
    # wordVector.close()
    data = address
    for sentence in data:
        sentence = sentence['predict_segmentation']
        for word in sentence:
            wordDic = open(dicPath, 'r')
            wordDict = {}
            for line in wordDic.readlines():
                voblist = line.strip().split('\t')
                wordDict[voblist[0]] = int(voblist[1])
            wordDic.close()
            if ' ' in word:
                continue
            if word in wordDict:
                continue
            else:
                wordDic = open(dicPath, 'a')
                wordVector = open(wvecPath, 'a')
                wordVec = []
                # word = word.decode('utf8')
                for i in range(len(word)):
                    if word[i] in dic:
                        if i == 0:
                            wordVec = dic[word[i]]
                        else:
                            wordVec = [wordVec[j] + dic[word[i]][j] for j in range(len(wordVec))]
                    else:
                        if i == 0:
                            wordVec = dic['<UNK>']
                        else:
                            wordVec = [wordVec[j] + dic['<UNK>'][j] for j in range(len(wordVec))]

                wordVec = [i / len(word) for i in wordVec]
                wordVector.write(word)
                wordVector.write(' ')
                for i in wordVec:
                    wordVector.write(str(i))
                    wordVector.write(' ')
                wordVector.write('\n')
                wordDic.write(word + '\t' + str(len(wordDict) + 1))
                wordDic.write('\n')
                wordDic.close()
                wordVector.close()
    wordVec = open(wvecPath, 'r+')
    f = wordVec.readlines()
    wordDic = open(dicPath, 'r')
    wordDict = {}
    for line in wordDic.readlines():
        voblist = line.strip().split('\t')
        wordDict[voblist[0]] = int(voblist[1])
    wordDic.close()
    f[0] = '%d 50\n' % len(wordDict)
    wordVec.close()
    wordVec = open(wvecPath, 'w+')
    wordVec.writelines(f)
    wordVec.close()
    return True










