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
