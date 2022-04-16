# DistributedScan

The experiment is configured and started through the `DistributedScan()` command. All of the options effecting the experiment, other than the hyperparameters themselves, are configured through the Scan arguments. The most common use-case is where ~10 arguments are invoked.

## Minimal Example

```python
jako.DistributedScan(x='x', y='y', params=p, model=input_model,config='config.json')

```

## DistributedScan Arguments

`x`, `y`, `params`, `model` and `config` are the only required arguments to start the experiment, all other are optional.</aside>

Argument | Input | Description
--------- | ------- | -----------
`x` | array or list of arrays | prediction features
`y` | array or list of arrays | prediction outcome variable
`params` | dict or ParamSpace object | the parameter dictionary or the ParamSpace object after splitting
`model` | function | the Keras model as a function
`experiment_name` | str | Used for creating the experiment logging folder
`x_val` | array or list of arrays | validation data for x
`y_val` | array or list of arrays | validation data for y
`val_split` | float | validation data split ratio
`random_method` | str | the random method to be used
`seed` | float | Seed for random states
`performance_target` | list | A result at which point to end experiment
`fraction_limit` | float | The fraction of permutations to be processed
`round_limit` | int | Maximum number of permutations in the experiment
`time_limit` | datetime | Time limit for experiment in format `%Y-%m-%d %H:%M`
`boolean_limit` | function | Limit permutations based on a lambda function
`reduction_method` | str | Type of reduction optimizer to be used used
`reduction_interval` | int | Number of permutations after which reduction is applied
`reduction_window` | int | the lookback window for reduction process
`reduction_threshold` | float | The threshold at which reduction is applied
`reduction_metric` | str | The metric to be used for reduction
`minimize_loss` | bool | `reduction_metric` is a loss
`disable_progress_bar` | bool | Disable live updating progress bar
`print_params` | bool | Print each permutation hyperparameters
`clear_session` | bool | Clear backend session between permutations
`save_weights` | bool | Keep model weights (increases memory pressure for large models)
`config` | str or dict | Configuration containing information about machines to distribute and database to upload the data.


## DistributedScan Object Properties

Once the `DistributedScan()` procedures are completed, an object with several useful properties is returned.The namespace is strictly kept clean, so all the properties consist of meaningful contents.

In the case conducted the following experiment, we can access the properties in `distributed_scan_object` which is a python class object.

```python
distributed_scan_object = jako.DistributedScan(x, y, model=iris_model, params=p, fraction_limit=0.1, config='config.json')
```
<hr>

**`best_model`** picks the best model based on a given metric and returns the index number for the model.

```python
distributed_scan_object.best_model(metric='f1score', asc=False)
```
NOTE: `metric` has to be one of the metrics used in the experiment, and `asc` has to be True for the case where the metric is something to be minimized.

<hr>

**`data`** returns a pandas DataFrame with the results for the experiment together with the hyperparameter permutation details.

```python
distributed_scan_object.data
```

<hr>

**`details`** returns a pandas Series with various meta-information about the experiment.

```python
distributed_scan_object.details
```

<hr>

**`evaluate_models`** creates a new column in `distributed_scan_object.data` with result from kfold cross-evaluation.

```python
distributed_scan_object.evaluate_models(x_val=x_val,
                            y_val=y_val,
                            n_models=10,
                            metric='f1score',
                            folds=5,
                            shuffle=True,
                            average='binary',
                            asc=False)
```

Argument | Description
-------- | -----------
`distributed_scan_object` | The class object returned by DistributedScan() upon completion of the experiment.
`x_val` | Input data (features) in the same format as used in DistributedScan(), but should not be the same data (or it will not be much of validation).
`y_val` | Input data (labels) in the same format as used in DistributedScan(), but should not be the same data (or it will not be much of validation).
`n_models` | The number of models to be evaluated. If set to 10, then 10 models with the highest metric value are evaluated. See below.
`metric` | The metric to be used for picking the models to be evaluated.
`folds` | The number of folds to be used in the evaluation.
`shuffle` | If the data is to be shuffled or not. Set always to False for timeseries but keep in mind that you might get periodical/seasonal bias.
`average` |One of the supported averaging methods: 'binary', 'micro', or 'macro'
`asc` |Set to True if the metric is to be minimized.
`saved` | bool | if a model saved on local machine should be used
`custom_objects` | dict | if the model has a custom object, pass it here

<hr>

**`learning_entropy`** returns a pandas DataFrame with entropy measure for each permutation in terms of how much there is variation between results of each epoch in the permutation.

```python
distributed_scan_object.learning_entropy
```

<hr>

**`params`** returns a dictionary with the original input parameter ranges for the experiment.

```python
distributed_scan_object.params
```

<hr>

**`round_times`** returns a pandas DataFrame with the time when each permutation started, ended, and how many seconds it took.

```python
distributed_scan_object.round_times
```

<hr>

<hr>

**`round_history`** returns epoch-by-epoch data for each model in a dictionary.

```python
distributed_scan_object.round_history
```

<hr>

**`saved_models`** returns the JSON (dictionary) for each model.

```python
distributed_scan_object.saved_models
```

<hr>

**`saved_weights`** returns the weights for each model.

```python
distributed_scan_object.saved_weights
```

<hr>

**`x`** returns the input data (features).

```python
distributed_scan_object.x
```

<hr>

**`y`** returns the input data (labels).

```python
distributed_scan_object.y
```

## Input Model

The input model is any Keras or tf.keras model. It's the model that Jako will use as the basis for the hyperparameter experiment.

#### A minimal example

```python
def input_model(x_train, y_train, x_val, y_val, params):

    model.add(Dense(12, input_dim=8, activation=params['activation']))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', params['optimizer'])
    out = model.fit(x=x_train,
                    y=y_train,
                    validation_data=[x_val, y_val])

    return out, model
```
See specific details about defining the model [here](Examples_Typical?id=defining-the-model).

#### Models with multiple inputs or outputs (list of arrays)

For both cases, `DistributedScan(... x_val, y_val ...)` must be explicitly set i.e. you split the data yourself before passing it into Jako. Using the above minimal example as a reference.

For **multi-input** change `model.fit()` as highlighted below:

```python
out = model.fit(x=[x_train_a, x_train_b],
                y=y_train,
                validation_data=[[x_val_a, x_val_b], y_val])
```

For **multi-output** the same structure is expected but instead of changing the `x` argument values, now change `y`:

```python
    out = model.fit(x=x_train,
                    y=[y_train_a, y_train_b],
                    validation_data=[x_val, [y_val_a, y_val_b]])
```
For the case where its both **multi-input** and **multi-output** now both `x` and `y` argument values follow the same structure:

```python
    out = model.fit(x=[x_train_a, x_train_b],
                    y=[y_train_a, y_train_b],
                    validation_data=[[x_val_a, x_val_b], [y_val_a, y_val_b]])
```


## Parameter Dictionary

The first step in an experiment is to decide the hyperparameters you want to use in the optimization process.

#### A minimal example

```python
p = {
    'first_neuron': [12, 24, 48],
    'activation': ['relu', 'elu'],
    'batch_size': [10, 20, 30]
}
```

#### Supported Input Formats

Parameters may be inputted either in a list or tuple.

As a set of discreet values in a list:

```python
p = {'first_neuron': [12, 24, 48]}
```
As a range of values `(min, max, steps)`:

```python
p = {'first_neuron': (12, 48, 2)}
```

For the case where a static value is preferred, but it's still useful to include it in in the parameters dictionary, use list:

```python
p = {'first_neuron': [48]}
```

