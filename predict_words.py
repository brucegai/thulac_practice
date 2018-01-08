# -*- coding:utf-8 -*-
# coding=utf-8

import numpy as np

import tensorflow as tf
import os
import sys
import os
from collections import Counter

FLAGS = tf.app.flags.FLAGS



tf.app.flags.DEFINE_string("word2vec_path_2p", "",
                               "the second word2vec data path")

tf.app.flags.DEFINE_integer("max_sentence_lenp", 80,
                                "max num of tokens per query")
tf.app.flags.DEFINE_integer("embedding_size_2p", 0, "second embedding size")
tf.app.flags.DEFINE_integer("num_tagsp", 72, "BMES")
tf.app.flags.DEFINE_integer("num_hiddenp", 100, "hidden unit number")
tf.app.flags.DEFINE_integer("batch_sizep", 100, "num example per mini batch")
tf.app.flags.DEFINE_integer("train_stepsp", 50000, "trainning steps")
tf.app.flags.DEFINE_float("learning_ratep", 0.001, "learning rate")


def predict_word(address, cvecPath, vobPath, wordModelPath, wordMatrixPath, wordsize, word_class_dic):
    word2vec_path_2p = ''
    max_sentence_lenp = 80
    embedding_size_2p = 0
    num_tagsp = 72
    batch_sizep = 100
    num_hiddenp = 100
    train_stepsp = 50000
    learning_ratep = 0.001

    # tf.app.flags.DEFINE_integer("embedding_size", wordsize, "embedding size")

    class Model:
        def __init__(self, embeddingSize, distinctTagNum, c2vPath, numHidden):
            #嵌入层将词转化为向量
            self.embeddingSize = embeddingSize

            #唯一标注数量
            self.distinctTagNum = distinctTagNum

            #隐藏层，hidden layer
            self.numHidden = numHidden

            # initializer 初始化工具

            # regularizer 规则化, 用于泛化其模型


            self.c2v = self.load_w2v(c2vPath, wordsize)
            if embedding_size_2p > 0:
                self.c2v2 = self.load_w2v(word2vec_path_2p, embedding_size_2p)
            self.words = tf.Variable(self.c2v, name="words")
            if embedding_size_2p > 0:
                self.words2 = tf.constant(self.c2v2, name="words2")
            with tf.variable_scope('Softmax', reuse=None) as scope:
                self.W = tf.get_variable(
                    shape=[numHidden * 2, distinctTagNum],
                    initializer=tf.truncated_normal_initializer(stddev=0.01),
                    name="weights",
                    regularizer=tf.contrib.layers.l2_regularizer(0.001))
                self.b = tf.Variable(tf.zeros([distinctTagNum], name="bias"))

            self.transition_params = None


            self.transMatrix = None

            # tensorflow 填充机制
            self.transParams = tf.placeholder(tf.float32)

            # tensorflow 填充机制
            self.transMatr = tf.placeholder(tf.float32)


            self.inp = tf.placeholder(tf.int32,
                                      shape=[None, max_sentence_lenp],
                                      name="input_placeholder")
            pass

        def length(self, data):
            used = tf.sign(tf.abs(data))
            length = tf.reduce_sum(used, reduction_indices=1)
            length = tf.cast(length, tf.int32)
            return length

        # def inference(self, X, reuse=None, trainMode=False):
        #   word_vectors = tf.nn.embedding_lookup(self.c2v, X)
        #   length = self.length(X)
        #   length_64 = tf.cast(length, tf.int64)
        #   if embedding_size_2p > 0:
        #     word_vectors2 = tf.nn.embedding_lookup(self.c2v2, X)
        #     word_vectors = tf.concat(2, [word_vectors, word_vectors2])
        #   #if trainMode:
        #   #  word_vectors = tf.nn.dropout(word_vectors, 0.5)
        #   with tf.variable_scope("rnn_fwbw", reuse=None) as scope:
        #     forward_output, _ = tf.nn.dynamic_rnn(
        #         tf.contrib.rnn.LSTMCell(self.numHidden),
        #         word_vectors,
        #         dtype=tf.float32,
        #         sequence_length=length,
        #         scope="RNN_forward")
        #     backward_output_, _ = tf.nn.dynamic_rnn(
        #         tf.contrib.rnn.LSTMCell(self.numHidden),
        #         inputs=tf.reverse_sequence(word_vectors,
        #                                    length_64,
        #                                    seq_dim=1),
        #         dtype=tf.float32,
        #         sequence_length=length,
        #         scope="RNN_backword")
        #
        #   backward_output = tf.reverse_sequence(backward_output_,
        #                                         length_64,
        #                                         seq_dim=1)
        #
        #   output = tf.concat([forward_output, backward_output], 2)
        #   output = tf.reshape(output, [-1, self.numHidden * 2])
        #   if trainMode:
        #     output = tf.nn.dropout(output, 0.5)
        #
        #   matricized_unary_scores = tf.matmul(output, self.W) + self.b
        #   # matricized_unary_scores = tf.nn.log_softmax(matricized_unary_scores)
        #   unary_scores = tf.reshape(
        #       matricized_unary_scores,
        #       [-1, max_sentence_lenp, self.distinctTagNum])
        #
        #   return unary_scores, length

        def inference(self, X, reuse=None, trainMode=False):
            word_vectors = tf.nn.embedding_lookup(self.words, X)
            length = self.length(X)
            length_64 = tf.cast(length, tf.int64)
            if embedding_size_2p > 0:
                word_vectors2 = tf.nn.embedding_lookup(self.words2, X)
                word_vectors = tf.concat(2, [word_vectors, word_vectors2])
            # if trainMode:
            #  word_vectors = tf.nn.dropout(word_vectors, 0.5)
            with tf.variable_scope("rnn_fwbw", reuse=reuse) as scope:
                forward_output, _ = tf.nn.dynamic_rnn(
                    # why reuse?
                    tf.contrib.rnn.LSTMCell(self.numHidden, reuse=tf.get_variable_scope().reuse),
                    word_vectors,
                    dtype=tf.float32,
                    sequence_length=length,
                    scope="RNN_forward")
                backward_output_, _ = tf.nn.dynamic_rnn(
                    tf.contrib.rnn.LSTMCell(self.numHidden, reuse=tf.get_variable_scope().reuse),
                    inputs=tf.reverse_sequence(word_vectors,
                                               length_64,
                                               seq_dim=1),
                    dtype=tf.float32,
                    sequence_length=length,
                    scope="RNN_backword")

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
                [-1, max_sentence_lenp, self.distinctTagNum])

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
                assert (len(ss) == (dim + 1))
                vals = []
                for i in range(1, dim + 1):
                    fv = float(ss[i])
                    mv[i - 1] += fv
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
            P, sequence_length = self.inference(self.inp, reuse=None, trainMode=False)
            return P, sequence_length

        def Matrix(self):
            return self.transMatr

            # def loss(self, X, Y):
            # P, sequence_length = self.inference(X)
            # log_likelihood, self.transition_params = tf.contrib.crf.crf_log_likelihood(
            # P, Y, sequence_length)
            # loss = tf.reduce_mean(-log_likelihood)

    # return loss

    # def train(total_loss):
    # return tf.train.AdamOptimizer(learning_ratep).minimize(total_loss)
    vob = open(vobPath)
    dic = {}
    for line in vob.readlines():
        # print(line)
        voblist = line.strip().split('\t')
        dic[voblist[0]] = voblist[1]
    vob.close()

    g = tf.Graph()
    with g.as_default():
        model = Model(wordsize, num_tagsp, cvecPath,
                      num_hiddenp)
        X = tf.placeholder(tf.int32, [1, 80])
        unary_score, length = model.inference(X)
        # init = tf.initialize_all_variables()
        saver = tf.train.Saver()
        sess = tf.Session()
        # sess.run(init)
        saver.restore(sess, wordModelPath)

        # input_X = [[38,16,10,266,20,2,21,17,1052,80,52,9,25,25,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

        trans = np.load(wordMatrixPath)
    for k in range(0, address.__len__()):
        sentence = address[k]['preprocessed_address'].strip()
        input_x = []
        a = 0
        b = []
        c = ['(', ')', ',', '-']
        for i in sentence:
            if i in c:
                b.append(a)
            else:
                if i in dic:
                    input_x.append(int(dic[i]))
                else:
                    input_x.append(1)
            a += 1
        for j in range(len(input_x), 80):
            input_x.append(0)
        input_x = [input_x]
        result, len1 = sess.run([unary_score, length], feed_dict={X: input_x})
        Y = []
        for tf_unary_scores in result:
            viterbi_sequence, _ = tf.contrib.crf.viterbi_decode(tf_unary_scores, trans)
            Y.append(viterbi_sequence)
        seg = Y[0][:len1[0]]

        fp = open(word_class_dic)
        dic1 = {}
        for line in fp.readlines():
            # print(line)
            voblist1 = line.strip().split('\t')
            dic1[voblist1[1]] = voblist1[0]
        fp.close()
        mark = []
        for i in seg:
            mark.append(dic1[str(i)])
        if mark[len1[0] - 1][-1] != '3':
            if mark[len1[0] - 1][-1] != '0':
                t = list(mark[len1[0] - 1])
                t[-1] = '3'
                t = ''.join(t)
                mark[len1[0] - 1] = t
        for m in range(len(b)):
            mark.insert(b[m], '18,0')
        sentenceSeg = []
        sentencetag = []
        tag_total = []
        new_word = ''
        for i, bmes_tag in enumerate(mark):
            if (bmes_tag[-1] == '0' or bmes_tag[-1] == '3'):
                if bmes_tag[-1] == '0':
                    if new_word != '':
                        sentenceSeg.append(new_word)
                        sentencetag.append(str(Counter(tag_total).most_common(1)[0][0]))
                        sentenceSeg.append(sentence[i])
                        sentencetag.append(str(bmes_tag.split(',')[0]))
                        tag_total = []
                        new_word = ''
                    else:
                        sentenceSeg.append(sentence[i])
                        sentencetag.append(str(bmes_tag.split(',')[0]))
                        tag_total = []
                        new_word = ''

                else:
                    new_word += sentence[i]
                    tag_total.append(int(bmes_tag.split(',')[0]))
                    sentencetag.append(str(Counter(tag_total).most_common(1)[0][0]))
                    tag_total = []
                    sentenceSeg.append(new_word)
                    new_word = ''
            else:
                new_word += sentence[i]
                tag_total.append(int(bmes_tag.split(',')[0]))
            if (i == len(mark) - 1 and (bmes_tag[-1] != '3' and bmes_tag[-1] != '0')):
                sentenceSeg.append(new_word)
                sentencetag.append(str(Counter(tag_total).most_common(1)[0][0]))
        # address[k]["predict_segmentation"] = sentenceSeg
        address[k]["predict_segmentation"] = sentenceSeg
        address[k]['predict_tags'] = sentencetag
        if k > 1 and (k + 1) % 20 == 0:
            print("已预测%d条地址..." % (k + 1))
    sess.close()
    return address


