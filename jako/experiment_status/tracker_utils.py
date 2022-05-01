import os
import shutil


def create_docker_compose_install_script(self):
    filename = 'jako_docker_compose.sh'
    sh_path = os.path.dirname(__file__) + '/' + filename
    shutil.copy(sh_path, '/tmp/')


def create_graphql_install_script(self):
    filename = 'jako_docker_graphql.sh'
    sh_path = os.path.dirname(__file__) + '/' + filename
    shutil.copy(sh_path, '/tmp/')


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

    tracker_files = ['jako_docker_compose.sh', 'jako_docker_graphql.sh']

    for file in os.listdir("/tmp/"):
        if file in tracker_files:
            sftp.put("/tmp/" + file, self.dest_dir + file)

    sftp.close()


def setup_graphql(self, client, machine_id):

    execute_strings = ['sh /tmp/jako_docker_compose.sh',
                       'sh /tmp/jako_docker_graphql.sh']

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
