import webbrowser
from ..distribute.distribute_database import get_db_host
from .tracker_utils import run_query
import json

with open('/tmp/jako_arguments_remote.json', 'r') as f:
    arguments_dict = json.load(f)

experiment_name = arguments_dict['experiment_name']


def open_browser(self):
    hasura_url = 'http://{}:8080/console'
    db_host = get_db_host(self)
    hasura_url = hasura_url.format(db_host)
    webbrowser.open_new(hasura_url)


def total_nodes(self):
    from .tracker_queries import total_nodes

    db_host = get_db_host(self)
    uri = 'http://{}:8080/v1/graphql'.format(db_host)
    statusCode = 200
    query = total_nodes()
    query = query % {'experiment_name': experiment_name}

    res = run_query(uri, query, statusCode)
    res = res['data'][experiment_name][0]['total_nodes']

    return res
