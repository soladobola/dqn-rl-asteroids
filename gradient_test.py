import tensorflow as tf


def f(w1, w2):
    return 2*w1 + 3*w2*w1


w1, w2 = tf.Variable(0.0), tf.Variable(0.0)
with tf.GradientTape() as tape:
    z = f(w1, w2)

gradients = tape.gradient(z, [w1, w2])

print(gradients[1])