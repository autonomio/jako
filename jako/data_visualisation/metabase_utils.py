import requests
from ..distribute.distribute_utils import read_config
from ..distribute.distribute_database import get_db_host


def get_token(self):
    db_host = get_db_host(self)
    url = 'http://{}:3000/api/session'.format(db_host)

    config = read_config(self)
    mb_username = config['metabase']['username']
    mb_password = config['metabase']['password']
    headers = {'content-type': 'application/json',
               'username': mb_username,
               'password': mb_password
                   }
    res = requests.post(url, json=headers)
    token = res.json()['id']
    return token
    
    