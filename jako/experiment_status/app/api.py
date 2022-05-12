from fastapi import FastAPI
from ..tracker import Tracker

app = FastAPI()
tracker = Tracker()


@app.get("/", tags=["Home"])
def get_number_of_nodes() -> int:
    number_of_nodes = tracker.total_nodes()
    return number_of_nodes
