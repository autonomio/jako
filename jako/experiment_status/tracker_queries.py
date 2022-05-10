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


def query_max_by_parameter(experiment_name, parameter, stage):
    query = queries['max_by_parameter']
    query = query % {'experiment_name': experiment_name,
                     'parameter': parameter,
                     'stage': stage}
    return query


def query_min_by_parameter(experiment_name, parameter, stage):
    query = queries['min_by_parameter']
    query = query % {'experiment_name': experiment_name,
                     'parameter': parameter,
                     'stage': stage}
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
