# Experiment Status API

While the experiment is running, the user can access the round results from each run through the experiment status api. The postgres database to which the results are updated, can be accessed via a GraphQL API provided by the hasura console.

## Minimal Example

```
from jako import run_tracker
run_tracker()
```

This will run the api on `http://0.0.0.0:8080`. Each API can be accessed via the corresponding url shown below, once the api has started running.

### Number of Nodes

Arguments: None
Description : Number of machines in which the DistributedScan experiment runs.
Returns: int
endpoint: `http://0.0.0.0:8080/number_of_nodes`

### Number of Permutations

Arguments: None
Description : Number of permutations completed so far in the distributed run.
Returns: int
endpoint: `http://0.0.0.0:8080/number_of_permutations`

### Time Per Permutation

Arguments: None
Description : Time taken between the current and previous permutation.
Returns: int
endpoint: `http://0.0.0.0:8080/time_per_permutation`

### Total Time

Arguments: None
Description : Total time taken for the current experiment to run.
Returns: int
endpoint: `http://0.0.0.0:8080/total_time`

### Max By Metric

Arguments: metric
Description : Given a metric, output the maximum value for the metric. Eg: Max of val_accuracy for a given experiment.
Returns: float
endpoint: `http://0.0.0.0:8080/max_by_metric/?metric=metric_name`

Replace the value `metric_name` in the above endpoint with metric of your choice.

### Min By Metric

Arguments: metric
Description : Given a metric, output the minimum value for the metric. Eg: Min of val_accuracy for a given experiment.
Returns: float
endpoint: `http://0.0.0.0:8080/min_by_metric/?metric=metric_name`

Replace the value `metric_name` in the above endpoint with metric of your choice.

### Max By Parameter

Arguments: parameter, param_value, metric
Description : Given a parameter, and its value, output the max value for the metric.
Eg: Max of val_accuracy for  when parameter first neuron has param value 256.
Returns: float
endpoint: `http://0.0.0.0:8080/max_by_parameter/?parameter=parameter_name&param_value=param_value&metric=metric_name`

Replace the values `parameter_name`, `param_value`, `metric_name` in the above endpoint with respective parameter name, parameter value and metric of your choice.

### Min By Parameter

Arguments: parameter, param_value, metric
Description : Given a parameter, and its value, output the min value for the metric.
Eg: Min of val_accuracy for  when parameter first neuron has param value 256.
Returns: float
endpoint: `http://0.0.0.0:8080/min_by_parameter/?parameter=parameter_name&param_value=param_value&metric=metric_name`

Replace the values `parameter_name`, `param_value`, `metric_name` in the above endpoint with respective parameter name, parameter value and metric of your choice.





