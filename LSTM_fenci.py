# -*- coding: utf-8 -*-
# @Author: Koth Chen
# @Date:   2016-07-26 13:48:32
# @Last Modified by:   Koth
# @Last Modified time: 2017-01-14 09:44:40

import numpy as np

import tensorflow as tf
import os

FLAGS = tf.app.flags.FLAGS


#
# tf.app.flags.DEFINE_string("word2vec_path_2l"+str(lerate), "",
#                            "the second word2vec data path")
#
# tf.app.flags.DEFINE_integer("max_sentence_len"+str(lerate), 80,
#                             "max num of tokens per query")
# tf.app.flags.DEFINE_integer("embedding_size"+str(lerate), 50, "embedding size")
# tf.app.flags.DEFINE_integer("embedding_size_2"+str(lerate), 0, "second embedding size")
# tf.app.flags.DEFINE_integer("num_tags"+str(lerate), 72, "BMES")
# tf.app.flags.DEFINE_integer("num_hidden"+str(lerate), 100, "hidden unit number")
# tf.app.flags.DEFINE_integer("batch_size"+str(lerate), 100, "num example per mini batch")
# tf.app.flags.DEFINE_integer("train_steps"+str(lerate), 20, "trainning steps")
# tf.app.flags.DEFINE_float("learning_rate", 0.001, "learning rate")

def fenci_train(res, charvecpath, pathfenci):
    # print('bbb')
    # global word2vec_path_2l,max_sentence_len,embedding_size,embedding_size_2,num_tags,batch_size,num_hidden,train_steps,learning_rate,train_data_path,test_data_path,log_dir,word2vec_path
    word2vec_path_2l = ''
    max_sentence_len = 80
    embedding_size = 50
    embedding_size_2 = 0
    num_tags = 72
    batch_size = 100
    num_hidden = 100
    train_steps = 20000
    dropoutrate = 0.5
    learning_rate = 0.001
    train_data_path = pathfenci + '/train.txt'
    test_data_path = pathfenci + '/test.txt'
    log_dir = pathfenci
    word2vec_path = charvecpath

    #     tf.app.flags.DEFINE_float("learning_rate"+str(lerate), lerate, "learning rate")
    #     tf.app.flags.DEFINE_string('train_data_path'+str(lerate), pathfenci+'/train.txt',
    #                            'Training data dir')
    #     tf.app.flags.DEFINE_string('test_data_path'+str(lerate), pathfenci+'/test.txt',
    #                            'Test data dir')
    #     tf.app.flags.DEFINE_string('log_dir'+str(lerate), pathfenci, 'The log  dir')
    #     tf.app.flags.DEFINE_string("word2vec_path"+str(lerate), charvecpath,
    #                            "the word2vec data path")

    def do_load_data(path):
        x = []
        y = []
        fp = open(path, "r")
        for line in fp.readlines():
            line = line.rstrip()
            if not line:
                continue
            ss = line.split(" ")
            assert (len(ss) == (max_sentence_len * 2))
            lx = []
            ly = []
            for i in range(max_sentence_len):
                lx.append(int(ss[i]))
                ly.append(int(ss[i + max_sentence_len]))
            x.append(lx)
            y.append(ly)
        fp.close()
        return np.array(x), np.array(y)

    class Model:
        def __init__(self, embeddingSize, distinctTagNum, c2vPath, numHidden):
            self.embeddingSize = embeddingSize
            self.distinctTagNum = distinctTagNum
            self.numHidden = numHidden
            self.c2v = self.load_w2v(c2vPath, embedding_size)
            if embedding_size_2 > 0:
                self.c2v2 = self.load_w2v(word2vec_path_2l, embedding_size_2)
            self.words = tf.Variable(self.c2v, name="words")
            if embedding_size_2 > 0:
                self.words2 = tf.constant(self.c2v2, name="words2")
            with tf.variable_scope('Softmax') as scope:
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
                                      shape=[None, max_sentence_len],
                                      name="input_placeholder")
            pass

        def length(self, data):
            used = tf.sign(tf.abs(data))
            length = tf.reduce_sum(used, reduction_indices=1)
            length = tf.cast(length, tf.int32)
            return length

        def inference(self, X, reuse=None, trainMode=True):
            word_vectors = tf.nn.embedding_lookup(self.words, X)
            length = self.length(X)
            length_64 = tf.cast(length, tf.int64)
            if embedding_size_2 > 0:
                word_vectors2 = tf.nn.embedding_lookup(self.words2, X)
                # concat 沿着某一个维度连接
                word_vectors = tf.concat(2, [word_vectors, word_vectors2])
            # if trainMode:
            #  word_vectors = tf.nn.dropout(word_vectors, 0.5)
            with tf.variable_scope("rnn_fwbw", reuse=reuse) as scope:
                forward_output, _ = tf.nn.dynamic_rnn(
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
                output = tf.nn.dropout(output, dropoutrate)

            matricized_unary_scores = tf.matmul(output, self.W) + self.b
            # matricized_unary_scores = tf.nn.log_softmax(matricized_unary_scores)
            unary_scores = tf.reshape(
                matricized_unary_scores,
                [-1, max_sentence_len, self.distinctTagNum])

            return unary_scores, length

        def loss(self, X, Y):
            P, sequence_length = self.inference(X)
            log_likelihood, self.transition_params = tf.contrib.crf.crf_log_likelihood(
                P, Y, sequence_length)
            loss = tf.reduce_mean(-log_likelihood)
            return loss

        def load_w2v(self, path, expectDim):
            fp = open(path, "r")
            # print("load data from:", path)
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
                if len(ss) != (dim + 1):
                    ws.append(ws[0])
                    continue
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
            P, sequence_length = self.inference(self.inp, reuse=True, trainMode=False)
            return P, sequence_length

        def Matrix(self):
            return self.transMatr

    def read_csv(batch_size, file_name):
        filename_queue = tf.train.string_input_producer([file_name])
        reader = tf.TextLineReader(skip_header_lines=0)
        key, value = reader.read(filename_queue)
        # decode_csv will convert a Tensor from type string (the text line) in
        # a tuple of tensor columns with the specified defaults, which also
        # sets the data type for each column
        decoded = tf.decode_csv(
            value,
            field_delim=' ',
            record_defaults=[[0] for i in range(max_sentence_len * 2)])

        # batch actually reads the file and loads "batch_size" rows in a single tensor
        return tf.train.shuffle_batch(decoded,
                                      batch_size=batch_size,
                                      capacity=batch_size * 50,
                                      min_after_dequeue=batch_size)

    def test_evaluate(sess, unary_score, test_sequence_length, transMatrix, inp,
                      tX, tY):
        totalEqual = 0
        batchSize = batch_size
        totalLen = tX.shape[0]
        numBatch = int((tX.shape[0] - 1) / batchSize) + 1
        correct_labels = 0
        correct_sentence = 0
        total_labels = 0
        total_sentence = 0
        word = 0
        total_correct_word = 0
        for i in range(numBatch):
            endOff = (i + 1) * batchSize
            if endOff > totalLen:
                endOff = totalLen
            y = tY[i * batchSize:endOff]
            feed_dict = {inp: tX[i * batchSize:endOff]}
            unary_score_val, test_sequence_length_val = sess.run(
                [unary_score, test_sequence_length], feed_dict)
            for tf_unary_scores_, y_, sequence_length_ in zip(unary_score_val, y, test_sequence_length_val):
                # print("seg len:%d" % (sequence_length_))
                tf_unary_scores_ = tf_unary_scores_[:sequence_length_]
                y_ = y_[:sequence_length_]
                viterbi_sequence, _ = tf.contrib.crf.viterbi_decode(tf_unary_scores_,
                                                                    transMatrix)
                # Evaluate word-level accuracy.
                correct_labels += np.sum(np.equal(viterbi_sequence, y_))
                total_labels += sequence_length_
                total_sentence += 1
                flag = 1

                for record in y_ == viterbi_sequence:
                    if record == False:
                        flag = 0
                        break
                if flag == 1:
                    correct_sentence += 1

                for i in range(sequence_length_):
                    p = 0
                    q = 0
                    flag1 = 0
                    if (y_[i] == 3):
                        word = word + 1
                        q = i
                        for k in range(p, q + 1):
                            if y_[k] != viterbi_sequence[k]:
                                flag1 = 1;
                        if flag1 == 0:
                            total_correct_word = total_correct_word + 1
                        p = i
                    elif (y_[i] == 0):
                        word = word + 1
                        if y_[i] == viterbi_sequence[i]:
                            total_correct_word = total_correct_word + 1
                        p = i

        lableAccuracy = 100.0 * correct_labels / float(total_labels)
        wordAccuracy = 100.0 * total_correct_word / float(word)
        sentenceAccuracy = 100.0 * correct_sentence / float(total_sentence)
        #       print("lableAccuracy: %.3f%%\n" % lableAccuracy)
        #       print("WordAccuracy: %.3f%%\n" % wordAccuracy)
        #       print("SentenceAccuracy: %.3f%%\n" % sentenceAccuracy)
        fp.write("\n lableAccuracy: [%f] " % (lableAccuracy))
        fp.write("\n WordAccuracy: [%f] " % (wordAccuracy))
        fp.write("\n SentenceAccuracy: [%f]" % (sentenceAccuracy))

    def inputs(path):
        whole = read_csv(batch_size, path)
        features = tf.transpose(tf.stack(whole[0:max_sentence_len]))
        label = tf.transpose(tf.stack(whole[max_sentence_len:]))
        return features, label

    def train(total_loss):
        return tf.train.AdamOptimizer(learning_rate).minimize(total_loss)

    fp = open(pathfenci + '/save.txt', "w")
    curdir = os.path.dirname(os.path.realpath(__file__))
    trainDataPath = train_data_path
    if not trainDataPath.startswith("/"):
        trainDataPath = curdir + "/../../" + trainDataPath
    graphs = tf.Graph()
    with graphs.as_default():
        model = Model(embedding_size, num_tags, word2vec_path,
                      num_hidden)
        #         print("train data path:", trainDataPath)
        X, Y = inputs(trainDataPath)
        tX, tY = do_load_data(test_data_path)
        total_loss = model.loss(X, Y)
        train_op = train(total_loss)
        test_unary_score, test_sequence_length = model.test_unary_score()
        sv = tf.train.Supervisor(graph=graphs, logdir=log_dir)
        with sv.managed_session(master='') as sess:
            # actual training loop
            training_steps = train_steps
            for step in range(training_steps):
                if sv.should_stop():
                    break
                try:
                    _, model.transMatrix = sess.run([train_op, model.transition_params])
                    model.transMatr = model.transMatrix
                    model.transParams = model.transition_params
                    # for debugging and learning purposes, see how the loss gets decremented thru training steps
                    if (step + 1) % 50 == 0:
                        k = sess.run(total_loss)
                        fp.write("\n [%d] loss: [%r]" % (step + 1, k))
                        print("[%d] loss: [%r]" % (step + 1, k))
                        np.save(pathfenci + '/Matrix.npy', model.Matrix())
                    if (step + 1) % 1000 == 0:
                        test_evaluate(sess, test_unary_score, test_sequence_length,
                                      model.transMatrix, model.inp, tX, tY)
                        # print (model.Matrix())
                except KeyboardInterrupt as e:
                    sv.saver.save(sess, pathfenci + '/model', global_step=(step + 1))
                    raise e
            sv.saver.save(sess, pathfenci + '/finnal-model')
    fp.close()
    return True
