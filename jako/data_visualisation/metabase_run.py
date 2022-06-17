from .metabase_utils import get_token
from ..distribute.distribute_utils import read_config
from ..distribute.distribute_database import get_db_host


class MetabaseRun:
    def __init__(self, experiment_name):
        self.experiment_name = experiment_name
        db_host = get_db_host(self)
        self.db_host = db_host
        config = read_config(self)
        self.token = get_token(self, db_host, config)
