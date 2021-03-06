#https://www.tensorflow.org/get_started/get_started


def func_primary():
    import tensorflow as tf
    node1 = tf.constant(3.0, tf.float32)
    node2 = tf.constant(4.0)  # also tf.float32 implicitly

    node3 = tf.add(node1, node2)

    print('\nnode 1 => ', node1)
    print('node 2 => ', node2)

    sess = tf.Session()

    print('executando os nós >')
    print(sess.run([node1, node2]))

    print('node3: ', node3)
    print("sess.run(node3): ", sess.run(node3))

    a = tf.placeholder(tf.float32)
    b = tf.placeholder(tf.float32)
    adder_node = a + b  # + provides a shortcut for tf.add(a, b)

    print(sess.run(adder_node, {a: 3, b: 4.5}))
    print(sess.run(adder_node, {a: [1, 3], b: [2, 4]}))

    add_and_triple = adder_node * 3.
    print(sess.run(add_and_triple, {a: 3, b: 4.5}))

    W = tf.Variable([.3], tf.float32)
    b = tf.Variable([-.3], tf.float32)
    x = tf.placeholder(tf.float32)

    print('w = ', W)
    print('b = ', b)
    print('x = ', x)

    linear_model = W * x + b

    init = tf.global_variables_initializer()
    sess.run(init)

    print(sess.run(linear_model, {x: [1, 2, 3, 4]}))

    print('\n função de perda  ', '--' * 30, ' : ')

    y = tf.placeholder(tf.float32)
    squared_deltas = tf.square(linear_model - y)
    loss = tf.reduce_sum(squared_deltas)
    print('perda => ', sess.run(loss, {x: [1, 2, 3, 4], y: [0, -1, -2, -3]}))

    # mudandos os valores de W e b
    # fixW = tf.assign(W, [-1.])
    # fixb = tf.assign(b, [1.])
    # sess.run([fixW, fixb])
    # print('perda => ', sess.run(loss, {x:[1,2,3,4], y:[0,-1,-2,-3]}))

    optimizer = tf.train.GradientDescentOptimizer(0.01)
    train = optimizer.minimize(loss)

    sess.run(init)  # reset values to incorrect defaults.
    for i in range(1000):
        sess.run(train, {x: [1, 2, 3, 4], y: [0, -1, -2, -3]})

    print(sess.run([W, b]))


def func_second():
    import numpy as np
    import tensorflow as tf

    # Model parameters
    W = tf.Variable([.3], tf.float32)
    b = tf.Variable([-.3], tf.float32)

    # Model input and output
    x = tf.placeholder(tf.float32)
    linear_model = W * x + b
    y = tf.placeholder(tf.float32)

    # loss
    loss = tf.reduce_sum(tf.square(linear_model - y))  # sum of the squares

    # optimizer
    optimizer = tf.train.GradientDescentOptimizer(0.01)
    train = optimizer.minimize(loss)

    # training data
    x_train = [1, 2, 3, 4]
    y_train = [0, -1, -2, -3]

    # training loop
    init = tf.global_variables_initializer()
    sess = tf.Session()
    sess.run(init)  # reset values to wrong

    for i in range(1000):
        sess.run(train, {x: x_train, y: y_train})

    # evaluate training accuracy
    curr_W, curr_b, curr_loss = sess.run([W, b, loss], {x: x_train, y: y_train})
    print("W: %s b: %s loss: %s" % (curr_W, curr_b, curr_loss))


def func_terceira():
    import tensorflow as tf
    # NumPy is often used to load, manipulate and preprocess data.
    import numpy as np

    # Declare list of features. We only have one real-valued feature. There are many
    # other types of columns that are more complicated and useful.
    features = [tf.contrib.layers.real_valued_column("x", dimension=1)]

    # An estimator is the front end to invoke training (fitting) and evaluation
    # (inference). There are many predefined types like linear regression,
    # logistic regression, linear classification, logistic classification, and
    # many neural network classifiers and regressors. The following code
    # provides an estimator that does linear regression.
    estimator = tf.contrib.learn.LinearRegressor(feature_columns=features)

    # TensorFlow provides many helper methods to read and set up data sets.
    # Here we use `numpy_input_fn`. We have to tell the function how many batches
    # of data (num_epochs) we want and how big each batch should be.
    x = np.array([1., 2., 3., 4.])
    y = np.array([0., -1., -2., -3.])
    input_fn = tf.contrib.learn.io.numpy_input_fn({"x": x}, y, batch_size=4,
                                                  num_epochs=1000)

    # We can invoke 1000 training steps by invoking the `fit` method and passing the
    # training data set.
    estimator.fit(input_fn=input_fn, steps=1000)

    # Here we evaluate how well our model did. In a real example, we would want
    # to use a separate validation and testing data set to avoid overfitting.
    print(estimator.evaluate(input_fn=input_fn))


    # Declare list of features, we only have one real-valued feature




def model(features, labels, mode):
    import tensorflow as tf

    # Build a linear model and predict values
    W = tf.get_variable("W", [1], dtype=tf.float64)
    b = tf.get_variable("b", [1], dtype=tf.float64)
    y = W * features['x'] + b

    # Loss sub-graph
    loss = tf.reduce_sum(tf.square(y - labels))

    # Training sub-graph
    global_step = tf.train.get_global_step()
    optimizer = tf.train.GradientDescentOptimizer(0.01)
    train = tf.group(optimizer.minimize(loss), tf.assign_add(global_step, 1))

    # ModelFnOps connects subgraphs we built to the
    # appropriate functionality.
    return tf.contrib.learn.ModelFnOps(mode=mode, predictions=y, loss=loss, train_op=train)


def func_quatra():
    import numpy as np
    import tensorflow as tf

    estimator = tf.contrib.learn.Estimator(model_fn=model)

    # define our data set
    x = np.array([1., 2., 3., 4.])
    y = np.array([0., -1., -2., -3.])
    input_fn = tf.contrib.learn.io.numpy_input_fn({"x": x}, y, 4, num_epochs=1000)

    # train -
    estimator.fit(input_fn=input_fn, steps=1000)

    # evaluate our model
    print(estimator.evaluate(input_fn=input_fn, steps=10))


if __name__ == '__main__':
    func_quatra()