from .docker_pull import docker_pull
from .docker_utils import write_shell_script, docker_ssh_run


def docker_run(self, client, machine_id, db_machine=False):
    '''Run docker commands in remote machines'''
    write_shell_script(self)
    docker_ssh_run(self, client, machine_id)

    database_imagename = 'abhijithneilabraham/jako_database_docker'
    jako_imagename = 'abhijithneilabraham/jako_docker_image'

    if db_machine:
        docker_pull(self, database_imagename)

    docker_pull(self, jako_imagename)
