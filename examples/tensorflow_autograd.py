import tensorflow as tf

x = tf.Variable(3.0)
with tf.GradientTape() as tape:
    y = x * x
gradient = tape.gradient(y, x)
print(gradient.numpy())  # dy/dx = 6.0
