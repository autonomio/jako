import requests


def setup_graphql(self, client, machine_id):
    ''' Set up Hasura graphql for database'''

    execute_strings = ['sh /tmp/jako_docker_compose.sh',
                       'sudo docker compose -f /tmp/docker-compose.yml up -d'
                       ]

    for execute_str in execute_strings:
        stdin, stdout, stderr = client.exec_command(execute_str)
        if stderr:
            for line in stderr:
                try:
                    # Process each error line in the remote output
                    print(line)
                except Exception as e:
                    print(e)

        for line in stdout:
            try:
                # Process each line in the remote output
                print(line)
            except Exception as e:
                print(e)


def run_query(uri, query, statusCode):
    ''' Send a post request containing the query'''

    request = requests.post(uri, json={'query': query})
    if request.status_code == statusCode:
        return request.json()
    else:
        raise Exception(f'''Unexpected status code returned:
                        {request.status_code}''')


def track_table(uri, experiment_name, statusCode):
    ''' Track table in the beginning of the experiment
    if it is not already tracked'''

    query = {
      "type": "pg_track_table",
      "args": {
        "source": "default",
        "schema": "public",
        "name": "{}".format(experiment_name)
      }
     }

    request = requests.post(uri, json=query)
    if request.status_code in (statusCode, 400):
        return request.json()
    else:
        raise Exception(f'''Unexpected status code returned:
                        {request.status_code}''')
