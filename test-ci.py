def test_distribute():
    '''Test distributing a Talos experiment'''

    from numpy import loadtxt
    from jako import DistributedScan

    url = 'https://raw.githubusercontent.com/'
    url += 'jbrownlee/Datasets/master/pima-indians-diabetes.data.csv'

    dataset = loadtxt(url, delimiter=',')

    x = dataset[:, 0:8]
    y = dataset[:, 8]

    def diabetes(x_train, y_train, x_val, y_val, params):

        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Dense

        model = Sequential()
        model.add(Dense(params['first_neuron'],
                        input_dim=8,
                        activation=params['activation']))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])

        out = model.fit(x=x,
                        y=y,
                        validation_data=[x_val, y_val],
                        epochs=4,
                        batch_size=params['batch_size'],
                        verbose=0)

        return out, model

    p = {'first_neuron': [12, 24, 48],
         'activation': ['relu', 'elu'],
         'batch_size': [10, 20, 40]}

    DistributedScan(x=x,
                    y=y,
                    params=p,
                    model=diabetes,
                    experiment_name='diabetes_test',
                    config='config.json')


test_distribute()
