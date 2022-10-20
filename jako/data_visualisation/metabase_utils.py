import requests


def get_token(self, db_host, config):

    url = 'http://{}:3000/api/session'.format(db_host)

    mb_username = config['metabase']['username']
    mb_password = config['metabase']['password']
    headers = {'content-type': 'application/json',
               'username': mb_username,
               'password': mb_password
               }
    res = requests.post(url, json=headers)

    try:
        token = res.json()['id']
    except KeyError:
        token = None

    return token


def run_query(self, token, db_host, endpoint, req_type='get'):

    url = 'http://{}/{}'.format(db_host, endpoint)

    headers = {'Content-Type': 'application/json', 'X-Metabase-Session': token}
    if req_type == 'get':
        res = requests.get(url, headers=headers)
    elif req_type == 'post':
        res = requests.post(url, headers=headers)

    return res.json()


def create_database(self, token, db_host):
    headers = {'Content-Type': 'application/json', 'X-Metabase-Session': token}
    url = 'http://{}:3000/api/database/'.format(db_host)

    db = {
        "engine": "postgres",
        "name": 'jako_metabase_postgres',
        "details":
            {
                "host": db_host,
                "port": "5432",
                "db": "postgres",
                "user": "postgres",
                "password": "postgres"
            }
    }

    res = requests.get(url, headers=headers).json()
    db_list = [data['name'] for data in res['data']]

    db_flag = False
    if 'jako_metabase_postgres' in db_list:
        db_flag = True

    if not db_flag:
        # if database does not exist, create database using databaset header
        res = requests.post(url, headers=headers, json=db)

    return res
