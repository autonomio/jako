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
                'CMD python3 /tmp/jako_scanfile_remote.py'
                ]

    with open('/tmp/Dockerfile', 'w') as f:
        for command in commands:
            f.write(command + '\n')


def docker_ssh_file_transfer(self, client, db_machine=False):
    '''Transfer the docker scripts to the remote machines'''

    import os

    write_dockerfile(self)

    sftp = client.open_sftp()

    try:
        sftp.chdir(self.dest_dir)  # Test if dest dir exists

    except IOError:
        sftp.mkdir(self.dest_dir)  # Create dest dir
        sftp.chdir(self.dest_dir)

    docker_files = ['jako_docker.sh', 'Dockerfile']

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
    execute_strings = ['chmod +x /tmp/jako_docker.sh', '/tmp/jako_docker.sh']

    if db_machine:
        from ..distribute.distribute_utils import read_config
        config = read_config(self)
        if "database" in config.keys():
            db_username = config['database']['DB_USERNAME']
            db_password = config['database']['DB_PASSWORD']
            db_port = config['database']['DB_PORT']
        else:
            db_username = 'postgres'
            db_password = 'postgres'
            db_port = '5432'
        db_container_name = 'jako_db'
        stop_cmd = 'docker stop {}'.format(db_container_name)
        rm_cmd = 'docker rm {}'.format(db_container_name)
        cmd = 'sudo docker run --name {} -e POSTGRES_PASSWORD={} -d -p {}:{} {}'
        cmd = cmd.format(db_container_name,
                         db_password, db_port, db_port, db_username)
        execute_strings += [stop_cmd, rm_cmd, cmd]

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

    execute_strings = [
        'sudo docker pull abhijithneilabraham/jako_docker_image'
        'sudo docker build -t jako_docker_remote -f /tmp/Dockerfile /tmp/',
        'sudo docker run -it  --name jako_docker_remote jako_docker_remote',
        'sudo docker container cp jako_docker_remote:/tmp/ /',
        'sudo docker rm jako_docker_remote']

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
