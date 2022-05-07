import webbrowser
from ..distribute.distribute_database import get_db_host


def open_browser(self):
    hasura_url = 'http://{}:8080/console'
    db_host = get_db_host(self)
    hasura_url = hasura_url.format(db_host)
    webbrowser.open_new(hasura_url)
