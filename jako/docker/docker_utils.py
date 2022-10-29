import os
import shutil
from ..distribute.distribute_database import get_db_host
from ..distribute.distribute_utils import get_stdout


def docker_install_commands(self):
    '''commands to install docker in a machine'''

    commands = ['curl -fsSL https://get.docker.com -o get-docker.sh',
                'sh get-docker.sh']

    return commands


def write_shell_script(self):
    '''write docker commands to shell script'''
    commands = docker_install_commands(self)

    with open('/tmp/{}/jako_docker.sh'.format(
            self.experiment_name), 'w') as f:
        for command in commands:
            f.write(command + '\n')


def write_dockerfile(self):
    commands = ['FROM abhijithneilabraham/jako_docker_image',
                'RUN mkdir -p /tmp/',
                'COPY jako_scanfile_remote.py /tmp/jako_scanfile_remote.py',
                'COPY jako_x_data_remote.npy /tmp/jako_x_data_remote.npy',
                'COPY jako_y_data_remote.npy /tmp/jako_y_data_remote.npy',
                ]

    if self.x_val and self.y_val:
        commands += [
                '''COPY jako_x_val_data_remote.npy
                /tmp/jako_x_val_data_remote.npy'''.replace('\n', ''),
                '''COPY jako_y_val_data_remote.npy
                /tmp/jako_y_val_data_remote.npy'''.replace('\n', '')
                ]

    commands += [
                '''COPY jako_arguments_remote.json
                /tmp/jako_arguments_remote.json'''.replace('\n', ''),
                'COPY jako_remote_config.json /tmp/jako_remote_config.json',
                'CMD python3 /tmp/jako_scanfile_remote.py',
                'RUN chmod -R 777 /tmp/'
                ]

    with open('/tmp/{}/Dockerfile'.format(
            self.experiment_name), 'w') as f:
        for command in commands:
            f.write(command + '\n')


def modify_docker_compose(self):
    import yaml
    currpath = os.path.dirname(__file__)
    compose_path = currpath + '/docker-compose.yml'

    with open(compose_path) as f:
        compose_config = yaml.safe_load(f)

    compose_config_metabase = compose_config['services']['metabase-app']
    compose_config_env = compose_config_metabase['environment']

    db_host = get_db_host(self)
    db_uri = 'postgresql://postgres:postgres@{}:5432/postgres'
    db_uri = db_uri.format(db_host)
    compose_config_env['MB_DB_CONNECTION_URI'] = db_host

    with open(compose_path, "w") as f:
        yaml.dump(compose_config, f)

    return compose_config


def docker_ssh_file_transfer(self, client, db_machine=False):
    '''Transfer the docker scripts to the remote machines'''

    write_dockerfile(self)

    sftp = client.open_sftp()

    try:
        sftp.chdir(self.dest_dir)  # Test if dest dir exists

    except IOError:
        sftp.mkdir(self.dest_dir)  # Create dest dir
        sftp.chdir(self.dest_dir)

    docker_files = ['jako_docker.sh', 'Dockerfile']
    docker_compose_files = ['docker-compose.yml', 'jako_docker_compose.sh']

    if db_machine:

        currpath = os.path.dirname(__file__)
        compose_install_script_path = currpath + '/jako_docker_compose.sh'
        compose_path = currpath + '/docker-compose.yml'

        shutil.copy(compose_install_script_path, '/tmp/')
        shutil.copy(compose_path, '/tmp/')

    for file in os.listdir("/tmp/{}".format(self.experiment_name)):
        if file in docker_files:
            sftp.put("/tmp/{}/".format(
                self.experiment_name) + file, self.dest_dir + file)
    try:
        sftp.chdir('/tmp/')  # Test if dest dir exists

    except IOError:
        sftp.mkdir('/tmp/')  # Create dest dir
        sftp.chdir('/tmp/')

    for file in os.listdir("/tmp/"):
        if file in docker_compose_files:
            sftp.put("/tmp/" + file, file)

    sftp.close()


def setup_db_with_graphql(self, client, machine_id):
    ''' Hasura GraphQL setup along with the current database'''

    if self.machine_spec == 'amazon_linux':
        execute_strings = [
            'sudo docker-compose -f /tmp/docker-compose.yml up -d']
    else:
        execute_strings = ['sh /tmp/jako_docker_compose.sh']
        execute_strings.append(
            'sudo docker compose -f /tmp/docker-compose.yml up -d')

    for execute_str in execute_strings:
        stdin, stdout, stderr = client.exec_command(execute_str)
        get_stdout(self, stdout, stderr)


def amazon_linux_docker_cmds(self):
    '''commands to install docker in amazon linux'''
    cmds = ['sudo yum update -y',
            'sudo amazon-linux-extras install docker',
            'sudo service docker start',
            ]
    return cmds


def docker_install(self, client, machine_id):
    execute_str = 'sudo docker'
    '''execute commands to install docker across any platform'''

    stdin, stdout, stderr = client.exec_command(execute_str)
    dockerflag = True
    out = get_stdout(self, stdout, stderr)

    if out == "docker_error":
        dockerflag = False

    if not dockerflag:
        install = ['chmod +x /tmp/{}/jako_docker.sh'.format(
            self.experiment_name),
            'sh /tmp/{}/jako_docker.sh'.format(
                self.experiment_name)]

        for execute_str in install:
            stdin, stdout, stderr = client.exec_command(execute_str)
            out = get_stdout(self, stdout, stderr)

            if out == 'amazon_machine_spec_error':
                self.machine_spec = 'amazon_linux'

        if self.machine_spec == 'amazon_linux':
            cmds = [
                'sudo yum update -y',
                'sudo yum install amazon-linux-extras',
                'sudo amazon-linux-extras install docker',
                'sudo service docker start',
                'sudo groupadd docker',
                'sudo usermod -aG docker $USER']

            for cmd in cmds:
                _, stdout, stderr = client.exec_command(cmd)
                get_stdout(self, stdout, stderr)


def check_architecture(self, client):
    cmd = 'uname -m'
    _, stdout, stderr = client.exec_command(cmd)
    print('-'*100)
    print(stdout, stderr)
    if 'x86_64' in stdout or 'x86_64' in stderr:
        arch = 'amd'
    else:
        arch = 'arm'
    return arch


def docker_image_setup(self, client, machine_id, db_machine=False):
    '''Run the transmitted script remotely without args and show its output.

    Parameters
    ----------
    client | `Object` | paramiko ssh client object
    machine_id | `int`| Machine id for each of the distribution machines

    Returns
    -------
    None.

    '''
    execute_strings = []

    docker_install(self, client, machine_id)

    arch = check_architecture(self, client)

    if arch == 'amd':
        pull = 'sudo docker pull abhijithneilabraham/jako_docker_image'
    elif arch == 'arm':
        pull = 'sudo docker pull abhijithneilabraham/jako_docker_image_arm64'

    execute_strings.append(pull)

    if db_machine:

        if self.machine_spec == 'amazon_linux':
            compose_install_cmd = 'sudo curl -L '
            compose_install_cmd += 'https://github.com/docker/compose/'
            compose_install_cmd += 'releases/download/1.22.0/'
            compose_install_cmd += 'docker-compose-$(uname -s)-$(uname -m)'
            compose_install_cmd += ' -o /usr/local/bin/docker-compose'

            permission_cmd = 'sudo chmod +x /usr/local/bin/docker-compose'
            symlink_cmd = 'sudo ln -s /usr/local/bin/docker-compose'
            symlink_cmd += ' /usr/bin/docker-compose'

            compose_cmd = 'sudo docker-compose -f'
            compose_cmd += ' /tmp/docker-compose.yml up -d'

            execute_strings += [compose_install_cmd,
                                permission_cmd,
                                symlink_cmd,
                                compose_cmd]
        else:
            compose_install_cmd = 'sh /tmp/jako_docker_compose.sh'
            compose_cmd = 'sudo docker compose -f '
            compose_cmd += '/tmp/docker-compose.yml up -d'
            execute_strings += [compose_install_cmd, compose_cmd]

    for execute_str in execute_strings:
        stdin, stdout, stderr = client.exec_command(execute_str)
        get_stdout(self, stdout, stderr)


def docker_scan_run(self, client, machine_id):
    ''' Run DistributedScan using docker'''
    machine_id = str(machine_id)
    experiment_name = self.experiment_name
    print('started experiment in machine id {}'.format(machine_id))
    rm_container = ['sudo docker stop jako_docker_remote',
                    'sudo docker rm jako_docker_remote']
    build = ['sudo docker build -t jako_docker_remote -f /tmp/' +
             experiment_name + '/Dockerfile /tmp/' + experiment_name + '/']
    execute_strings = [
        'sudo docker run  --name jako_docker_remote jako_docker_remote',
        'sudo docker container cp -a jako_docker_remote:/tmp/ /tmp/' +
        experiment_name + '/',
        'sudo docker stop jako_docker_remote',
        'sudo docker rm jako_docker_remote']

    cmd_strings = rm_container + build + execute_strings
    execute_strings = []

    for string in cmd_strings:
        string = string.replace('jako_docker_remote', experiment_name)
        execute_strings.append(string)

    for execute_str in execute_strings:
        stdin, stdout, stderr = client.exec_command(execute_str)
        get_stdout(self, stdout, stderr)
    print('Completed experiment in machine id {}'.format(machine_id))
