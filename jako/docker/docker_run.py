from .docker_pull import docker_pull


def docker_run(self, db_machine=False):
    '''Run docker commands in remote machines'''

    database_imagename = 'abhijithneilabraham/jako_database_docker'
    jako_imagename = 'abhijithneilabraham/jako_docker_image'

    if db_machine:
        docker_pull(self, database_imagename)

    docker_pull(self, jako_imagename)
