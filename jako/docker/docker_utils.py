import os


def docker_install_commands(self):
    '''commands to install docker in a machine'''

    commands = ['curl -fsSL https://get.docker.com -o get-docker.sh',
                'sh get-docker.sh']

    return commands


def write_shell_script(self):
    '''write docker commands to shell script'''
    commands = docker_install_commands(self)
    with open('/tmp/jako_docker.sh', 'w') as f:
        for command in commands:
            f.write(command + '\n')


def write_dockerfile(self):
    commands = ['FROM abhijithneilabraham/jako_docker_image',
                'RUN mkdir -p /tmp/',
                'COPY jako_scanfile_remote.py /tmp/jako_scanfile_remote.py',
                'COPY jako_x_data_remote.npy /tmp/jako_x_data_remote.npy',
                'COPY jako_y_data_remote.npy /tmp/jako_y_data_remote.npy',
                '''COPY jako_arguments_remote.json
                /tmp/jako_arguments_remote.json'''.replace('\n', ''),
                'COPY jako_remote_config.json /tmp/jako_remote_config.json',
                'CMD python3 /tmp/jako_scanfile_remote.py',
                'RUN chmod -R 777 /tmp/'
                ]

    with open('/tmp/Dockerfile', 'w') as f:
        for command in commands:
            f.write(command + '\n')


def docker_ssh_file_transfer(self, client, db_machine=False):
    '''Transfer the docker scripts to the remote machines'''

    write_dockerfile(self)

    sftp = client.open_sftp()

    try:
        sftp.chdir(self.dest_dir)  # Test if dest dir exists

    except IOError:
        sftp.mkdir(self.dest_dir)  # Create dest dir
        sftp.chdir(self.dest_dir)

    docker_files = ['jako_docker.sh', 'Dockerfile', 'docker-compose.yml']

    if db_machine:

        from ..distribute.distribute_database import get_db_object
        import yaml

        currpath = os.path.abspath(__file__)
        compose_path = currpath + '/docker-compose.yml'
        with open(compose_path, 'r') as f:
            data = yaml.safe_load(f)

        db_object = get_db_object(self)
        db_url = db_object.DB_URL
        db_url = db_url.replace('postgresql', 'postgres')
        env = data['services']['graphql-engine']['environment']
        env['HASURA_GRAPHQL_METADATA_DATABASE_URL'] = db_url
        env['PG_DATABASE_URL'] = db_url

        with open('tmp/docker-compose.yml', 'w') as f:
            yaml.dump(data, f)

    for file in os.listdir("/tmp/"):
        if file in docker_files:
            sftp.put("/tmp/" + file, self.dest_dir + file)

    sftp.close()


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
    execute_str = 'sudo docker'
    execute_strings = []
    stdin, stdout, stderr = client.exec_command(execute_str)
    dockerflag = True
    if stdout:
        if 'command not found' in stdout:
            dockerflag = False
    if stderr:
        if 'command not found' in stdout:
            dockerflag = False

    if not dockerflag:
        install = ['chmod +x /tmp/jako_docker.sh', '/tmp/jako_docker.sh']
        execute_strings += install

    pull = ['sudo docker pull abhijithneilabraham/jako_docker_image']
    execute_strings += pull

    if db_machine:

        cmd = 'sudo docker compose -f /tmp/docker-compose.yml up -d'
        execute_strings += [cmd]

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


def docker_scan_run(self, client, machine_id):
    machine_id = str(machine_id)
    print('started experiment in machine id {}'.format(machine_id))
    build = ['sudo docker build -t jako_docker_remote -f /tmp/Dockerfile /tmp/']
    execute_strings = [
        'sudo docker run  --name jako_docker_remote jako_docker_remote',
        'sudo docker container cp -a jako_docker_remote:/tmp/ /',
        'sudo docker rm jako_docker_remote']
    execute_strings = build + execute_strings
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

    print('Completed experiment in machine id {}'.format(machine_id))
