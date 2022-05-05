import json
import os

currpath = os.path.dirname(__file__)
json_path = currpath + 'queries.json'

with open(json_path, 'r') as f:
    queries = json.load(f)


def total_nodes(self):
    return queries['total_nodes']
