from .docker_utils import write_shell_script, docker_image_setup
from .docker_utils import docker_ssh_file_transfer


def docker_setup(self, client, machine_id, db_machine=False):
    '''Run docker commands in remote machines'''
    write_shell_script(self)
    docker_ssh_file_transfer(self, client, db_machine)
    docker_image_setup(self, client, machine_id, db_machine)
