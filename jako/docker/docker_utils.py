def docker_install_commands(self):
    '''commands to install docker in a machine'''

    commands = ['curl -fsSL https://get.docker.com -o get-docker.sh',
                'sh get-docker.sh']

    return commands


def write_shell_script(self):
    '''write docker commands to shell script'''
    commands = docker_install_commands(self)
    with open('/tmp/jako_docker.sh') as f:
        f.writelines(commands)


def docker_ssh_run(self, client, machine_id):
    '''Run the transmitted script remotely without args and show its output.

    Parameters
    ----------
    client | `Object` | paramiko ssh client object
    machine_id | `int`| Machine id for each of the distribution machines

    Returns
    -------
    None.

    '''
    execute_str = '/tmp/jako_docker.sh'
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
