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


def write_docker_pull_script(self, db_machine=False):
    import inspect
    from .docker_pull import docker_pull

    script = inspect.getsource(docker_pull)
    image_name = 'abhijithneilabraham/jako_docker_image'
    function_call = '\n' + 'docker_pull("{}")'.format(image_name)
    script = script + function_call
    write_path = '/tmp/jako_docker_image_pull.py'

    with open(write_path, 'w') as f:
        f.write(script)

    if db_machine:
        script = inspect.getsource(docker_pull)
        image_name = 'abhijithneilabraham/jako_database_docker'
        function_call = '\n' + 'docker_pull("{}")'.format(image_name)
        write_path = '/tmp/jako_docker_database_pull.py'

        with open(write_path, 'w') as f:
            f.write(script)


def write_dockerfile(self):
    commands = ['FROM abhijithneilabraham/jako_docker_image',
                'RUN mkdir -p /tmp/',
                'COPY scanfile_remote.py /tmp/scanfile_remote.py',
                'COPY x_data_remote.npy /tmp/x_data_remote.npy',
                'COPY y_data_remote.npy /tmp/y_data_remote.npy',
                'COPY arguments_remote.json /tmp/arguments_remote.json',
                'COPY remote_config.json /tmp/remote_config.json',
                'CMD python3 /tmp/scanfile_remote.py'
                ]

    with open('/tmp/Dockerfile', 'w') as f:
        for command in commands:
            f.write(command + '\n')


def docker_ssh_file_transfer(self, client, db_machine=False):
    '''Transfer the docker scripts to the remote machines'''

    import os

    write_docker_pull_script(self, db_machine)
    write_dockerfile(self)

    sftp = client.open_sftp()

    try:
        sftp.chdir(self.dest_dir)  # Test if dest dir exists

    except IOError:
        sftp.mkdir(self.dest_dir)  # Create dest dir
        sftp.chdir(self.dest_dir)

    docker_files = ['jako_docker.sh', 'jako_docker_image_pull.py',
                    'jako_docker_database_pull.py',
                    'Dockerfile']

    for file in os.listdir("/tmp/"):
        if file in docker_files:
            sftp.put("/tmp/" + file, file)

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
    execute_strings = ['chmod +x /tmp/jako_docker.sh', '/tmp/jako_docker.sh',
                       'python3 /tmp/jako_docker_image_pull.py']

    if db_machine:
        execute_strings += ['python3 /tmp/jako_docker_database_pull.py']

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
        'sudo docker rm jako_docker_remote'
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
