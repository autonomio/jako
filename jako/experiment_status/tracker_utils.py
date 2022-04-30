import os
import shutil


def docker_compose_install_script(self):
    filename = 'jako_docker_compose.sh'
    sh_path = os.path.dirname(__file__) + filename
    shutil.copy(sh_path, '/tmp/')


def install_docker_compose(self, client, machine_id):

    docker_compose_install_script(self)

    execute_strings = ['sh /tmp/jako_docker_compose.sh']

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
