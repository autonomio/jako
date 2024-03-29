import webbrowser
from ..distribute.distribute_database import get_db_host
from .tracker_utils import run_query, track_table
import json


class Tracker:
    def __init__(self, experiment_name):
        with open('/tmp/jako_arguments_remote.json', 'r') as f:
            arguments_dict = json.load(f)
            self.experiment_name = experiment_name
            params = list(arguments_dict['params'].keys())
            self.params = ' '.join(params)
            self.stage = arguments_dict['stage']
            self.db_host = get_db_host()
            hasura_url = 'http://{}:8080/console'
            self.hasura_url = hasura_url.format(self.db_host)
            self.uri = 'http://{}:8080/v1/graphql'.format(self.db_host)
            self.statusCode = 200
            metadata_uri = self.uri.replace('graphql', 'metadata')
            track_table(metadata_uri, self.experiment_name, self.statusCode)

    def open_browser(self):
        hasura_url = self.hasura_url
        webbrowser.open_new(hasura_url)

    def total_nodes(self):
        from .tracker_queries import query_total_nodes

        experiment_name = self.experiment_name
        uri = self.uri
        statusCode = self.statusCode
        stage = self.stage

        query = query_total_nodes(experiment_name, stage)

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

    def max_by_parameter(self, parameter, param_value, metric):
        from .tracker_queries import query_max_by_parameter

        experiment_name = self.experiment_name
        stage = self.stage
        uri = self.uri
        statusCode = self.statusCode

        query = query_max_by_parameter(experiment_name,
                                       parameter, param_value, metric, stage)

        res = run_query(uri, query, statusCode)
        agg = res['data'][experiment_name + '_aggregate']['aggregate']['max']
        res = agg[metric]
        return res

    def min_by_parameter(self, parameter, param_value, metric):
        from .tracker_queries import query_min_by_parameter

        experiment_name = self.experiment_name
        stage = self.stage
        uri = self.uri
        statusCode = self.statusCode

        query = query_min_by_parameter(experiment_name,
                                       parameter, param_value, metric, stage)

        res = run_query(uri, query, statusCode)
        agg = res['data'][experiment_name + '_aggregate']['aggregate']['min']
        res = agg[metric]
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

    def params_by_max_metric(self, metric):
        from .tracker_queries import query_params_by_max_metric

        experiment_name = self.experiment_name
        stage = self.stage
        uri = self.uri
        statusCode = self.statusCode
        max_metric = self.max_by_metric(metric)
        parameter = self.params

        query = query_params_by_max_metric(experiment_name,
                                           parameter, metric,
                                           max_metric, stage)

        res = run_query(uri, query, statusCode)
        res = res['data'][experiment_name][0]
        return res

    def params_by_min_metric(self, metric):
        from .tracker_queries import query_params_by_min_metric

        experiment_name = self.experiment_name
        stage = self.stage
        uri = self.uri
        statusCode = self.statusCode
        min_metric = self.min_by_metric(metric)
        parameter = self.params

        query = query_params_by_min_metric(experiment_name,
                                           parameter, metric,
                                           min_metric, stage)

        res = run_query(uri, query, statusCode)
        res = res['data'][experiment_name][0]
        return res

    def params_by_max_params(self, metric, ref_param, ref_val):
        from .tracker_queries import query_params_by_max_params

        experiment_name = self.experiment_name
        stage = self.stage
        uri = self.uri
        statusCode = self.statusCode
        parameter = self.params

        query = query_params_by_max_params(experiment_name, metric,
                                           parameter, ref_param,
                                           ref_val, stage)

        res = run_query(uri, query, statusCode)
        res = res['data'][experiment_name]
        return {'params_by_max_params': res}

    def params_by_min_params(self, metric, ref_param, ref_val):
        from .tracker_queries import query_params_by_min_params

        experiment_name = self.experiment_name
        stage = self.stage
        uri = self.uri
        statusCode = self.statusCode
        parameter = self.params

        query = query_params_by_min_params(experiment_name, metric,
                                           parameter, ref_param,
                                           ref_val, stage)

        res = run_query(uri, query, statusCode)
        res = res['data'][experiment_name]
        return {'params_by_min_params': res}
