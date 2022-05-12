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


def run_tracker():
    uvicorn.run(app, host='0.0.0.0', port=8080)
