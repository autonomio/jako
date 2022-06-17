from .metabase_utils import get_token, create_database
from ..distribute.distribute_utils import read_config
from ..distribute.distribute_database import get_db_host
import webbrowser


class MetabaseRun:
    def __init__(self, experiment_name):
        self.experiment_name = experiment_name

        db_host = get_db_host(self)
        self.db_host = db_host

        config = read_config(self)
        token = get_token(self, db_host, config)
        self.token = token

        create_database(self, token, db_host)

    def run_browser(self):
        db_host = self.db_host
        url = 'http://{}:3000/browse/1-jako-metabase-postgres'
        url = url.format(db_host)
        webbrowser.open_new(url)
