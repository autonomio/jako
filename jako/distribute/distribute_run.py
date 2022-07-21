import json
import threading
import os
from .distribute_params import run_scan
from .distribute_utils import return_current_machine_id, ssh_connect
from .distribute_utils import ssh_file_transfer, ssh_run, ssh_get_files
from .distribute_database import update_db

from ..docker.docker_run import docker_setup
from ..docker.docker_utils import setup_db_with_graphql


def run_central_machine(self, n_splits, run_central_node):
    '''Runs `talos.Scan()` in the central machine.

    Parameters
    ----------
    params  | `dict` | hyperparameter options

    Returns
    -------
    None.

    '''

    machine_id = 0

    run_scan(self, n_splits, run_central_node, machine_id)


def distribute_run(self):
    '''

    Parameters
    ----------
    run_central_machine | `bool` |The default is False.
    db_machine_id | `int` | The default is 0. Indicates the centralised store
                              where the data gets merged.

    Returns
    -------
    None.

    '''

    config = self.config_data
    status_details = {}

    if 'run_central_node' in config.keys():
        run_central_node = config['run_central_node']
    else:
        run_central_node = False

    update_db_n_seconds = 5
    if 'DB_UPDATE_INTERVAL' in config['database'].keys():
        update_db_n_seconds = int(config['database']['DB_UPDATE_INTERVAL'])

    n_splits = len(config['machines'])

    if run_central_node:
        n_splits += 1

    status_details['total_nodes'] = n_splits

    current_machine_id = str(return_current_machine_id(self))

    if 'database' in config.keys():
        db_machine_id = config['database']['DB_HOST_MACHINE_ID']

    if current_machine_id == str(0):

        clients = ssh_connect(self)

        run_docker = False
        if 'run_docker' in self.config_data.keys():
            run_docker = self.config_data['run_docker']

        for machine_id, client in clients.items():

            new_config = config
            new_config['current_machine_id'] = machine_id

            with open('/tmp/{}/jako_remote_config.json'.format(
                    self.experiment_name), 'w') as outfile:
                json.dump(new_config, outfile)

            ssh_file_transfer(self, client, machine_id)

            if run_docker:

                db_machine = False
                if int(db_machine_id) == int(machine_id):
                    db_machine = True

                docker_setup(self, client, machine_id, db_machine)
                setup_db_with_graphql(self, client, machine_id)

        from .distribute_database import get_db_object
        from .distribute_utils import get_experiment_stage

        db = get_db_object(self)
        self.stage = get_experiment_stage(self, db)

        if not self.stage:
            self.stage = 0

        with open('/tmp/{}/jako_arguments_remote.json'.format(
                self.experiment_name), 'r') as outfile:
            arguments_dict = json.load(outfile)

        arguments_dict["stage"] = self.stage
        status_details['experiment_stage'] = int(self.stage)
        status_details['machine_id'] = int(current_machine_id)

        with open('/tmp/{}/jako_arguments_remote.json'.format(
                self.experiment_name), 'w') as outfile:
            json.dump(arguments_dict, outfile, indent=2)

        extra_files = ['jako_arguments_remote.json']
        for machine_id, client in clients.items():
            ssh_file_transfer(self, client, machine_id,
                              extra_files)

        if run_docker:
            # create the threads
            from ..docker.docker_run import docker_run
            threads = []

            if run_central_node:

                args = (self, n_splits, run_central_node)
                thread = threading.Thread(target=run_central_machine,
                                          args=args)
                thread.start()
                threads.append(thread)

                args = ([self, update_db_n_seconds, current_machine_id,
                         self.stage, status_details])
                thread = threading.Thread(target=update_db, args=args)
                thread.start()
                threads.append(thread)

            for machine_id, client in clients.items():

                args = (self, client, machine_id)
                thread = threading.Thread(target=docker_run, args=args)
                thread.start()
                threads.append(thread)

            for t in threads:
                t.join()

            for file in os.listdir('/tmp/{}'.format(
                    self.experiment_name)):
                if file.startswith('machine_id'):
                    os.remove('/tmp/{}/'.format(self.experiment_name) + file)

            for machine_id, client in clients.items():
                ssh_get_files(self, client, machine_id)
        else:
            # create the threads
            threads = []

            if run_central_node:

                args = (self, n_splits, run_central_node)
                thread = threading.Thread(target=run_central_machine,
                                          args=args)
                thread.start()
                threads.append(thread)

                args = ([self, update_db_n_seconds, current_machine_id,
                         self.stage, status_details])
                thread = threading.Thread(target=update_db, args=args)
                thread.start()
                threads.append(thread)

            for machine_id, client in clients.items():

                args = (self, client, machine_id)
                thread = threading.Thread(target=ssh_run, args=args)
                thread.start()
                threads.append(thread)

            for t in threads:
                t.join()

            for file in os.listdir('/tmp/{}'.format(
                    self.experiment_name)):
                if file.startswith('machine_id'):
                    os.remove('/tmp/{}/'.format(self.experiment_name) + file)

            for machine_id, client in clients.items():
                ssh_get_files(self, client, machine_id)

    from .distribute_finish import distribute_finish
    self = distribute_finish(self)
