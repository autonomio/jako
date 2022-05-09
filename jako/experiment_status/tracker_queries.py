import json
import os

currpath = os.path.dirname(__file__)
json_path = currpath + 'queries.json'

with open(json_path, 'r') as f:
    queries = json.load(f)


def query_total_nodes(experiment_name):
    query = queries['total_nodes']
    query = query % {'experiment_name': experiment_name}
    return query


def query_number_of_permutations(experiment_name):
    query = queries['number_of_permutations']
    query = query % {'experiment_name': experiment_name}
    return query


def query_max_by_metric(experiment_name, metric):
    query = queries['max_by_metric']
    query = query % {'experiment_name': experiment_name,
                     'metric': metric}
    return query
