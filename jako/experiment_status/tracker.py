import webbrowser
from ..distribute.distribute_database import get_db_host
from .tracker_utils import run_query
import json


class Tracker:
    def __init__(self):
        with open('/tmp/jako_arguments_remote.json', 'r') as f:
            arguments_dict = json.load(f)
            self.experiment_name = arguments_dict['experiment_name']
            self.db_host = get_db_host()
            hasura_url = 'http://{}:8080/console'
            self.hasura_url = hasura_url.format(self.db_host)
            self.uri = 'http://{}:8080/v1/graphql'.format(self.db_host)
            self.statusCode = 200

    def open_browser(self):
        hasura_url = self.hasura_url
        webbrowser.open_new(hasura_url)

    def total_nodes(self):
        from .tracker_queries import total_nodes

        experiment_name = self.experiment_name
        uri = self.uri
        statusCode = self.statusCode

        query = total_nodes()
        query = query % {'experiment_name': experiment_name}

        res = run_query(uri, query, statusCode)
        res = res['data'][experiment_name][0]['total_nodes']

        return res

    def number_of_permutations(self):
        from .tracker_queries import number_of_permutations

        experiment_name = self.experiment_name
        uri = self.uri
        statusCode = self.statusCode

        query = number_of_permutations()
        query = query % {'experiment_name': experiment_name}

        res = run_query(uri, query, statusCode)
        res = len(res['data'][experiment_name])

        return res
