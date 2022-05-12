from fastapi import FastAPI
from ..tracker import Tracker

app = FastAPI()
tracker = Tracker()


@app.get("/number_of_nodes")
def get_number_of_nodes() -> int:
    number_of_nodes = tracker.total_nodes()
    return number_of_nodes


@app.get("/number_of_permutations")
def get_number_of_permutations() -> int:
    number_of_permutations = tracker.number_of_permutations()
    return number_of_permutations


@app.get("/time_per_permutation")
def get_time_per_permutation() -> int:
    time_per_permutation = tracker.time_per_permutation()
    return time_per_permutation


@app.get("/total_time")
def get_total_time() -> int:
    total_time = tracker.total_time()
    return total_time
