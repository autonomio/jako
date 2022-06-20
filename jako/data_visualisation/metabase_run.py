from .metabase_utils import get_token, create_database
from ..distribute.distribute_utils import read_config
from ..distribute.distribute_database import get_db_host
import webbrowser
import time


class MetabaseRun:
    def __init__(self, experiment_name):
        self.experiment_name = experiment_name

        db_host = get_db_host(self)
        self.db_host = db_host

        config = read_config(self)
        try:
            token = get_token(self, db_host, config)
        except KeyError:
            print(''''Opening browser console....
                  Enter username and password for metabase session.
                  The username and password should be same as given in config.
                  And run the jako program again''')
            time.sleep(2)
            self.run_browser()
            exit()
        self.token = token

        create_database(self, token, db_host)

    def run_browser(self):
        db_host = self.db_host
        url = 'http://{}:3000/browse/'
        url = url.format(db_host)
        webbrowser.open_new(url)
