# -*- coding:utf-8 -*-
# coding=utf-8
import numpy as np
import tensorflow as tf
import os
import sys
import os
import copy

FLAGS1 = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string('log_dirw', "logs", 'The log  dir')
tf.app.flags.DEFINE_string("word2vec_path_2w", "",
                           "the second word2vec data path")
tf.app.flags.DEFINE_integer("max_sentence_lenw", 80,
                            "max num of tokens per query")
tf.app.flags.DEFINE_integer("embedding_sizew", 50, "embedding size")
tf.app.flags.DEFINE_integer("embedding_size_2w", 0, "second embedding size")
tf.app.flags.DEFINE_integer("num_tagsw", 19, "BMES")
tf.app.flags.DEFINE_integer("num_hiddenw", 100, "hidden unit number")
tf.app.flags.DEFINE_integer("batch_sizew", 100, "num example per mini batch")
tf.app.flags.DEFINE_integer("train_stepsw", 50000, "trainning steps")
tf.app.flags.DEFINE_float("learning_ratew", 0.001, "learning rate")



class Modelw:
    def __init__(self, embeddingSize, distinctTagNum, c2vPath, numHidden):
        self.embeddingSize = embeddingSize
        self.distinctTagNum = distinctTagNum
        self.numHidden = numHidden
        self.c2v = self.load_w2v(c2vPath, FLAGS1.embedding_sizew)
        if FLAGS1.embedding_size_2w > 0:
            self.c2v2 = self.load_w2v(FLAGS1.word2vec_path_2w, FLAGS1.embedding_size_2w)
            # self.words = tf.Variable(self.c2v, name="words")
            # if FLAGS.embedding_size_2 > 0:
            # self.words2 = tf.constant(self.c2v2, name="words2")
        with tf.variable_scope('Softmax2') as scope:
            self.W = tf.get_variable(
                shape=[numHidden * 2, distinctTagNum],
                initializer=tf.truncated_normal_initializer(stddev=0.01),
                name="weights",
                regularizer=tf.contrib.layers.l2_regularizer(0.001))
            self.b = tf.Variable(tf.zeros([distinctTagNum], name="bias"))
        self.transition_params = None
        self.transMatrix = None
        self.transParams = tf.placeholder(tf.float32)
        self.transMatr = tf.placeholder(tf.float32)
        self.inp = tf.placeholder(tf.int32,
                                  shape=[None, FLAGS1.max_sentence_lenw],
                                  name="input_placeholder")
        sentence="上海市杨浦区长白新村街道军工路516号上海理工大学四公寓四号楼".decode('utf8')
        pass

    def length(self, data):
        used = tf.sign(tf.abs(data))
        length = tf.reduce_sum(used, reduction_indices=1)
        length = tf.cast(length, tf.int32)
        return length

    def inference(self, X, reuse=None, trainMode=False):
        word_vectors = tf.nn.embedding_lookup(self.c2v, X)
        length = self.length(X)
        length_64 = tf.cast(length, tf.int64)
        if FLAGS1.embedding_size_2w > 0:
            word_vectors2 = tf.nn.embedding_lookup(self.c2v2, X)
            word_vectors = tf.concat(2, [word_vectors, word_vectors2])
        # if trainMode:
        #  word_vectors = tf.nn.dropout(word_vectors, 0.5)
        with tf.variable_scope("rnn_fwbw2", reuse=reuse) as scope:
            forward_output, _ = tf.nn.dynamic_rnn(
                tf.contrib.rnn.LSTMCell(self.numHidden),
                word_vectors,
                dtype=tf.float32,
                sequence_length=length,
                scope="RNN_forward2")
            backward_output_, _ = tf.nn.dynamic_rnn(
                tf.contrib.rnn.LSTMCell(self.numHidden),
                inputs=tf.reverse_sequence(word_vectors,
                                           length_64,
                                           seq_dim=1),
                dtype=tf.float32,
                sequence_length=length,
                scope="RNN_backword2")
        backward_output = tf.reverse_sequence(backward_output_,
                                              length_64,
                                              seq_dim=1)
        output = tf.concat([forward_output, backward_output], 2)
        output = tf.reshape(output, [-1, self.numHidden * 2])
        if trainMode:
            output = tf.nn.dropout(output, 0.5)
        matricized_unary_scores = tf.matmul(output, self.W) + self.b
        # matricized_unary_scores = tf.nn.log_softmax(matricized_unary_scores)
        unary_scores = tf.reshape(
            matricized_unary_scores,
            [-1, FLAGS1.max_sentence_lenw, self.distinctTagNum])
        return unary_scores, length

    def loss(self, X, Y):
        P, sequence_length = self.inference(X)
        log_likelihood, self.transition_params = tf.contrib.crf.crf_log_likelihood(
            P, Y, sequence_length)
        loss = tf.reduce_mean(-log_likelihood)
        return loss

    def load_w2v(self, path, expectDim):
        fp = open(path, "r")
        line = fp.readline().strip()
        ss = line.split(" ")
        total = int(ss[0])
        dim = int(ss[1])
        assert (dim == expectDim)
        ws = []
        mv = [0 for i in range(dim)]
        second = -1
        for t in range(total):
            if ss[0] == '<UNK>':
                second = t
            line = fp.readline().strip()
            ss = line.split(" ")
            vals = []
            for i, v in enumerate(ss[-50:]):
                fv = float(v)
                mv[i] += fv
                vals.append(fv)
            ws.append(vals)
        for i in range(dim):
            mv[i] = mv[i] / total
        assert (second != -1)
        # append one more token , maybe useless
        ws.append(mv)
        if second != 1:
            t = ws[1]
            ws[1] = ws[second]
            ws[second] = t
        fp.close()
        return np.asarray(ws, dtype=np.float32)

    def test_unary_score(self):
        P, sequence_length = self.inference(self.inp, reuse=True, trainMode=False)
        return P, sequence_length

    def Matrix(self):
        return self.transMatr
        # def loss(self, X, Y):
        # P, sequence_length = self.inference(X)
        # log_likelihood, self.transition_params = tf.contrib.crf.crf_log_likelihood(
        # P, Y, sequence_length)
        # loss = tf.reduce_mean(-log_likelihood)

#
# return loss
# def train(total_loss):
# return tf.train.AdamOptimizer(FLAGS.learning_rate).minimize(total_loss)
import sys
import pandas as pd

totalLine = 0
longLine = 0
MAXLEN = 80
# MAX_LEN = 80
totalChars = 0


# label -1, unknown
# 0-> 'S'
# 1-> 'B'
# 2-> 'M'
# 3-> 'E'
def predic_class(address, cvecPath, wvecPath, dicPath, classModelPath, classMatrixPath, segDicPath):
    list1 = []
    totalLine = 0
    sc = open(segDicPath, 'r')  # 分级字典
    dict = {}
    a = sc.readlines()
    for line in a:
        voblist = line.strip().split('\t')
        dict[voblist[0]] = voblist[1]
    dict['P-SHO'] = '28'
    dict1 = {}
    for line in a:
        voblist = line.strip().split('\t')
        dict1[voblist[1]] = voblist[0]
    vocab = open(dicPath, 'r')  # 词表
    dictvob = {}
    for line in vocab.readlines():
        voblist1 = line.strip().split('\t')
        dictvob[voblist1[0]] = voblist1[1]
    # out = open('result all poi.txt','w')#结果文档
    fp = copy.deepcopy(address)
    sentence = []
    target = []
    for index, sentence in enumerate(fp):
        x = []
        # y = []
        xsentence = []
        # ysentence = []
        sentence = sentence['predict_segmentation']
        for i in range(len(sentence)):
            word = sentence[i]
            if word == word:
                if word in dictvob:
                    x.append(int(dictvob[word]))
                    xsentence.append(word)
                else:
                    x.append(0)
                    xsentence.append(word)
                    # if dict.has_key(word):
                    # y.append(int(dict[word]))
                    # ysentence.append(word)
                    # else:
                    # y.append(0)
                    # ysentence.append(word)
            else:
                x.append(0)
                # y.append(0)
                # xsentence.append(fp.ix[i,j])
                # ysentence.append(fp.ix[i,j+1])
        for k in range(len(x), MAXLEN):
            x.append(0)
            # y.append(0)
        sentence.append(xsentence)
        # target.append(ysentence)
        list1.append(x)
        # if len(list1[i]) != 160:
        totalLine = totalLine + 1

    f = tf.Graph()
    with f.as_default():
        modelw = Modelw(FLAGS1.embedding_sizew, FLAGS1.num_tagsw, wvecPath,
                        FLAGS1.num_hiddenw)
        X = tf.placeholder(tf.int32, [1, 80])
        unary_score, length = modelw.inference(X, trainMode=False)
        # init = tf.initialize_all_variables()
        saver1 = tf.train.Saver()
        sess1 = tf.Session()
        # sess1.run(init)
        saver1.restore(sess1, classModelPath)
        # input_X = [[38,16,10,266,20,2,21,17,1052,80,52,9,25,25,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
        trans = np.load(classMatrixPath)
    input_x = []
    correctSentence = 0
    wrongSentence = 0
    for i in range(len(list1)):
        sentence = "上海市杨浦区长白新村街道军工路516号上海理工大学四公寓四号楼".decode('utf8')
        sentence = sentence.strip().decode('utf8')
        x = list1[i][:MAXLEN]
        y = list1[i][MAXLEN:MAXLEN*2]
        input_x = [x]
        result, len1 = sess1.run([unary_score, length], feed_dict={X: input_x})
        Y = []
        Y_target = []
        for tf_unary_scores in result:
            viterbi_sequence, _ = tf.contrib.crf.viterbi_decode(tf_unary_scores, trans)
            Y.append(viterbi_sequence)
        Y = Y[0]
        flag = 0
        for j in range(len1[0]):
            Y_target.append(str(Y[j]))
        address[i]['predict_tags'] = Y_target
        if i > 1 and (i + 1) % 20 == 0:
            print("已分级%d条地址..." % (i + 1))
    sess1.close()
    return address
