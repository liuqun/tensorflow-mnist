import os
import model
import tensorflow as tf

from tensorflow.examples.tutorials.mnist import input_data
data = input_data.read_data_sets("/tmp/data/", one_hot=True)

# model
with tf.variable_scope("convolutional"):
    x = tf.placeholder(tf.float32, [None, 784])
    keep_prob = tf.placeholder(tf.float32)
    logits, variables = model.convolutional(x, keep_prob)
    y = tf.nn.softmax(logits)

# train
y_ = tf.placeholder(tf.float32, [None, 10])
cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=logits)
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

saver = tf.train.Saver(variables)
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(20000):
        batch = data.train.next_batch(50)
        if i % 100 == 0:
            train_accuracy = accuracy.eval(feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0})
            print("step %d, training accuracy %g" % (i, train_accuracy))
        sess.run(train_step, feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

    print(sess.run(accuracy, feed_dict={x: data.test.images, y_: data.test.labels, keep_prob: 1.0}))

    path = saver.save(
        sess, os.path.join(os.path.dirname(__file__), 'data', 'convolutional.ckpt'),
        write_meta_graph=False, write_state=False)
    print("Saved:", path)
