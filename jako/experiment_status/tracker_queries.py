import json
import os

currpath = os.path.dirname(__file__)
json_path = currpath + 'queries.json'

with open(json_path, 'r') as f:
    queries = json.load(f)


def total_nodes():
    return queries['total_nodes']


def number_of_permutations():
    return queries['number_of_permutations']
