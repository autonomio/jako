from ..distribute.distribute_database import get_db_host
import webbrowser


class MetabaseRun:
    def __init__(self, experiment_name):
        self.experiment_name = experiment_name
        db_host = get_db_host(self)
        self.db_host = db_host

    def run_browser(self):
        db_host = self.db_host
        url = 'http://{}:3000/browse/'
        url = url.format(db_host)
        print('metabase running on {}'.format(url))
        webbrowser.open_new(url)
