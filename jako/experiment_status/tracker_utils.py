import os
import shutil
import yaml
from ..distribute.distribute_database import get_db_object
from ..distribute.distribute_utils import read_config


def create_docker_compose_install_script(self):
    filename = 'jako_docker_compose.sh'
    sh_path = os.path.dirname(__file__) + '/' + filename
    shutil.copy(sh_path, '/tmp/')


def create_graphql_install_script(self):
    filename = 'docker-compose.yml'

    yml_path = os.path.dirname(__file__) + '/' + filename
    with open(yml_path, 'r') as f:
        data = yaml.safe_load(f)

    db_object = get_db_object(self)
    config = read_config(self)
    pg_pwd = config['database']['DB_PASSWORD']
    data['services']['postgres']['environment']['POSTGRES_PASSWORD'] = pg_pwd
    env = data['services']['graphql-engine']['environment']
    db_url = db_object.DB_URL
    env['HASURA_GRAPHQL_METADATA_DATABASE_URL'] = db_url
    env['PG_DATABASE_URL'] = db_url

    with open(yml_path, 'w') as f:
        yaml.dump(data, f)

    shutil.copy(yml_path, '/tmp/')


def tracker_ssh_file_transfer(self, client):
    '''Transfer the docker scripts to the remote machines'''

    create_docker_compose_install_script(self)
    create_graphql_install_script(self)

    import os

    sftp = client.open_sftp()

    try:
        sftp.chdir(self.dest_dir)  # Test if dest dir exists

    except IOError:
        sftp.mkdir(self.dest_dir)  # Create dest dir
        sftp.chdir(self.dest_dir)

    tracker_files = ['jako_docker_compose.sh', 'docker-compose.yml']

    for file in os.listdir("/tmp/"):
        if file in tracker_files:
            sftp.put("/tmp/" + file, self.dest_dir + file)

    sftp.close()


def setup_graphql(self, client, machine_id):

    execute_strings = ['sh /tmp/jako_docker_compose.sh'
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
