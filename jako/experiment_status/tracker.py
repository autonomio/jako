import webbrowser
from ..distribute.distribute_database import get_db_host
from .tracker_utils import run_query
import json
import datetime


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
            self.stage = self.latest_stage()

    def open_browser(self):
        hasura_url = self.hasura_url
        webbrowser.open_new(hasura_url)

    def latest_stage(self):
        from .tracker_queries import query_latest_experiment_stage

        experiment_name = self.experiment_name
        uri = self.uri
        statusCode = self.statusCode

        query = query_latest_experiment_stage(experiment_name)
        res = run_query(uri, query, statusCode)
        agg = res['data'][experiment_name + '_aggregate']['aggregate']['max']
        res = agg['experiment_stage']

        return res

    def total_nodes(self):
        from .tracker_queries import query_total_nodes

        experiment_name = self.experiment_name
        uri = self.uri
        statusCode = self.statusCode

        query = query_total_nodes(experiment_name)

        res = run_query(uri, query, statusCode)
        res = res['data'][experiment_name][0]['total_nodes']

        return res

    def number_of_permutations(self):
        from .tracker_queries import query_number_of_permutations

        experiment_name = self.experiment_name
        stage = self.stage
        uri = self.uri
        statusCode = self.statusCode

        query = query_number_of_permutations(experiment_name, stage)

        res = run_query(uri, query, statusCode)
        res = len(res['data'][experiment_name])

        return res

    def max_by_metric(self, metric):
        from .tracker_queries import query_max_by_metric

        experiment_name = self.experiment_name
        stage = self.stage
        uri = self.uri
        statusCode = self.statusCode

        query = query_max_by_metric(experiment_name, metric, stage)

        res = run_query(uri, query, statusCode)
        agg = res['data'][experiment_name + '_aggregate']['aggregate']['max']
        res = agg[metric]
        return res

    def min_by_metric(self, metric):
        from .tracker_queries import query_min_by_metric

        experiment_name = self.experiment_name
        stage = self.stage
        uri = self.uri
        statusCode = self.statusCode

        query = query_min_by_metric(experiment_name, metric, stage)

        res = run_query(uri, query, statusCode)
        agg = res['data'][experiment_name + '_aggregate']['aggregate']['min']
        res = agg[metric]
        return res

    def max_by_parameter(self, parameter):
        from .tracker_queries import query_max_by_parameter

        experiment_name = self.experiment_name
        stage = self.stage
        uri = self.uri
        statusCode = self.statusCode

        query = query_max_by_parameter(experiment_name, parameter, stage)

        res = run_query(uri, query, statusCode)
        agg = res['data'][experiment_name + '_aggregate']['aggregate']['max']
        res = agg[parameter]
        return res

    def min_by_parameter(self, parameter):
        from .tracker_queries import query_min_by_parameter

        experiment_name = self.experiment_name
        stage = self.stage
        uri = self.uri
        statusCode = self.statusCode

        query = query_min_by_parameter(experiment_name, parameter, stage)

        res = run_query(uri, query, statusCode)
        agg = res['data'][experiment_name + '_aggregate']['aggregate']['min']
        res = agg[parameter]
        return res

    def time_per_permutation(self):
        from .tracker_queries import query_time_per_permutation

        experiment_name = self.experiment_name
        uri = self.uri
        statusCode = self.statusCode

        query = query_time_per_permutation(experiment_name)

        res = run_query(uri, query, statusCode)
        time1 = res['data'][experiment_name][0]['timestamp']
        time1 = int(time1)
        time2 = res['data'][experiment_name][1]['timestamp']
        time2 = int(time2)

        time_elapsed = int(time1 - time2)

        return time_elapsed

    def total_time(self):
        from .tracker_queries import query_total_time

        experiment_name = self.experiment_name
        stage = self.stage
        uri = self.uri
        statusCode = self.statusCode

        query = query_total_time(experiment_name, stage)

        res = run_query(uri, query, statusCode)
        start_ts_agg = res['data'][experiment_name + '_aggregate']['aggregate']
        start_ts = start_ts_agg['min']['timestamp']
        end_ts = res['data'][experiment_name][0]['timestamp']

        time_elapsed = end_ts - start_ts

        return time_elapsed
