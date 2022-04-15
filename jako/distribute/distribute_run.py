import json
import threading
import os
from .distribute_params import run_scan
from .distribute_utils import return_current_machine_id, ssh_connect
from .distribute_utils import ssh_file_transfer, ssh_run, ssh_get_files
from .distribute_database import update_db


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

    current_machine_id = str(return_current_machine_id(self))

    if current_machine_id == str(0):

        clients = ssh_connect(self)

        for machine_id, client in clients.items():

            new_config = config
            new_config['current_machine_id'] = machine_id

            with open('/tmp/remote_config.json', 'w') as outfile:
                json.dump(new_config, outfile)

            ssh_file_transfer(self, client, machine_id)

        # create the threads
        threads = []

        if run_central_node:

            args = (self, n_splits, run_central_node)
            thread = threading.Thread(target=run_central_machine, args=args)
            thread.start()
            threads.append(thread)

            args = ([self, update_db_n_seconds, current_machine_id, self.stage])
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

        for file in os.listdir('/tmp/'):
            if file.startswith('machine_id'):
                os.remove('/tmp/' + file)

        for machine_id, client in clients.items():
            ssh_get_files(self, client, machine_id)

    from .distribute_finish import distribute_finish
    self = distribute_finish(self)
