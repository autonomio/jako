import uvicorn

from fastapi import FastAPI
from .tracker import Tracker

app = FastAPI()


@app.get("/number_of_nodes")
def get_number_of_nodes() -> int:
    tracker = Tracker()
    number_of_nodes = tracker.total_nodes()
    return number_of_nodes


@app.get("/number_of_permutations")
def get_number_of_permutations() -> int:
    tracker = Tracker()
    number_of_permutations = tracker.number_of_permutations()
    return number_of_permutations


@app.get("/time_per_permutation")
def get_time_per_permutation() -> int:
    tracker = Tracker()
    time_per_permutation = tracker.time_per_permutation()
    return time_per_permutation


@app.get("/total_time")
def get_total_time() -> int:
    tracker = Tracker()
    total_time = tracker.total_time()
    return total_time


@app.get("/max_by_metric/")
def get_max_by_metric(metric: str) -> float:
    tracker = Tracker()
    max_by_metric = tracker.max_by_metric(metric)
    return max_by_metric


@app.get("/min_by_metric/")
def get_min_by_metric(metric: str) -> float:
    tracker = Tracker()
    min_by_metric = tracker.min_by_metric(metric)
    return min_by_metric


@app.get("/max_by_parameter/")
def get_max_by_parameter(parameter: str,
                         param_value: str, metric: str) -> float:
    tracker = Tracker()
    max_by_parameter = tracker.max_by_parameter(parameter, param_value, metric)
    return max_by_parameter


@app.get("/min_by_parameter/")
def get_min_by_parameter(parameter: str,
                         param_value: str, metric: str) -> float:
    tracker = Tracker()
    min_by_parameter = tracker.min_by_parameter(parameter, param_value, metric)
    return min_by_parameter


@app.get("/params_by_max_metric/")
def get_params_by_max_metric(metric: str) -> dict:
    tracker = Tracker()
    params_by_max_metric = tracker.params_by_max_metric(metric)
    return params_by_max_metric


@app.get("/params_by_min_metric/")
def get_params_by_min_metric(metric: str) -> dict:
    tracker = Tracker()
    params_by_min_metric = tracker.params_by_min_metric(metric)
    return params_by_min_metric


@app.get("/params_by_max_params/")
def get_params_by_max_params(metric: str, ref_param: str, ref_val: str) -> dict:
    tracker = Tracker()
    params_by_max_params = tracker.params_by_max_params(metric,
                                                        ref_param, ref_val)
    return params_by_max_params


@app.get("/params_by_min_params/")
def get_params_by_min_params(metric: str, ref_param: str, ref_val: str) -> dict:
    tracker = Tracker()
    params_by_min_params = tracker.params_by_min_params(metric,
                                                        ref_param, ref_val)
    return params_by_min_params


def run_tracker():
    uvicorn.run(app, host='0.0.0.0', port=8080)
    tracker = Tracker()
    uri = tracker.hasura_url
    out_str = '''
    Hasura console running at {}
    '''.format(uri)
    tracker.open_browser()
    return out_str
