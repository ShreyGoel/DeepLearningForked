# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 00:14:00 2018

@author: Shrey
"""

import tflearn
import tensorflow as tf



X = tf.placeholder(shape=(None, 784), dtype=tf.float32)
net = tf.reshape(X, [-1, 28, 28, 1])

# Using TFLearn convolution layer.
net = tflearn.conv_2d(net, 32, 3, activation='relu')

# Using Tensorflow's max pooling op.
net = tf.nn.max_pool(net, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')