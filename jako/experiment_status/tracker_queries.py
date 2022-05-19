import os
import ast

currpath = os.path.dirname(__file__)
json_path = currpath + '/queries.json'

with open(json_path, 'r') as f:
    json_str = f.read()

queries = ast.literal_eval(json_str)

q = {}
for keys, vals in queries.items():
    v = vals.replace("\n", '')
    q[keys] = v

queries = q


def query_latest_experiment_stage(experiment_name):
    query = queries['latest_experiment_stage']
    query = query % {'experiment_name': experiment_name}
    return query


def query_total_nodes(experiment_name, stage):
    query = queries['total_nodes']
    query = query % {'experiment_name': experiment_name}
    return query


def query_number_of_permutations(experiment_name, stage):
    query = queries['number_of_permutations']
    query = query % {'experiment_name': experiment_name,
                     'stage': stage}
    return query


def query_max_by_metric(experiment_name, metric, stage):
    query = queries['max_by_metric']
    query = query % {'experiment_name': experiment_name,
                     'metric': metric,
                     'stage': stage}
    return query


def query_min_by_metric(experiment_name, metric, stage):
    query = queries['min_by_metric']
    query = query % {'experiment_name': experiment_name,
                     'metric': metric,
                     'stage': stage}
    return query


def query_max_by_parameter(experiment_name,
                           parameter, param_value, metric, stage):
    query = queries['max_by_parameter']
    param_value = str(param_value)
    query = query % {'experiment_name': experiment_name,
                     'parameter': parameter,
                     'param_value': param_value,
                     'metric': metric,
                     'stage': stage,
                     }
    return query


def query_min_by_parameter(experiment_name,
                           parameter, param_value, metric, stage):
    query = queries['min_by_parameter']
    param_value = str(param_value)
    query = query % {'experiment_name': experiment_name,
                     'parameter': parameter,
                     'param_value': param_value,
                     'metric': metric,
                     'stage': stage
                     }
    return query


def query_time_per_permutation(experiment_name):
    query = queries['time_per_permutation']
    query = query % {'experiment_name': experiment_name}

    return query


def query_total_time(experiment_name, stage):
    query = queries['total_time']
    query = query % {'experiment_name': experiment_name,
                     'stage': stage}

    return query


def query_params_by_max_metric(experiment_name,
                               parameter, metric, max_metric, stage):
    query = queries['params_by_max_metric']
    query = query % {'experiment_name': experiment_name,
                     'parameter': parameter,
                     'metric': metric,
                     'max_metric': max_metric,
                     'stage': stage}

    return query


def query_params_by_min_metric(experiment_name,
                               parameter, metric, min_metric, stage):
    query = queries['params_by_min_metric']
    query = query % {'experiment_name': experiment_name,
                     'parameter': parameter,
                     'metric': metric,
                     'min_metric': min_metric,
                     'stage': stage}

    return query


def query_params_by_max_params(experiment_name, metric,
                               parameter, ref_param, ref_val, stage):
    query = queries['params_by_max_param']
    query = query % {'experiment_name': experiment_name,
                     'metric': metric,
                     'parameter': parameter,
                     'ref_param': ref_param,
                     'ref_val': ref_val,
                     'stage': stage}

    return query


def query_params_by_min_params(experiment_name, metric,
                               parameter, ref_param, ref_val, stage):
    query = queries['params_by_min_param']
    query = query % {'experiment_name': experiment_name,
                     'parameter': parameter,
                     'metric': metric,
                     'ref_param': ref_param,
                     'ref_val': ref_val,
                     'stage': stage}

    return query
