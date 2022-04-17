from talos import Scan


class RemoteScan(Scan):
    def __init__(self,
                 x,
                 y,
                 params,
                 model,
                 experiment_name,
                 **kwargs):
        '''Distributed version of talos.Scan() for the remote machines.

        Parameters
        ----------
        params | `dict` | Hyperparameters for distribution.
        config | str or dict | The default is '/tmp/remote_config.json'.

        Returns
        -------
        None.

        '''

        import time
        import json

        self.x = x
        self.y = y
        self.params = params
        self.model = model
        self.experiment_name = experiment_name
        self.x_val = kwargs['x_val']
        self.y_val = kwargs['y_val']
        self.val_split = kwargs['val_split']

        # randomness
        self.random_method = kwargs['random_method']
        self.seed = kwargs['seed']

        # limiters
        self.performance_target = kwargs['performance_target']
        self.fraction_limit = kwargs['fraction_limit']
        self.round_limit = kwargs['round_limit']
        self.time_limit = kwargs['time_limit']
        self.boolean_limit = kwargs['boolean_limit']

        # optimization
        self.reduction_method = kwargs['reduction_method']
        self.reduction_interval = kwargs['reduction_interval']
        self.reduction_window = kwargs['reduction_window']
        self.reduction_threshold = kwargs['reduction_threshold']
        self.reduction_metric = kwargs['reduction_metric']
        self.minimize_loss = kwargs['minimize_loss']

        # display
        self.disable_progress_bar = kwargs['disable_progress_bar']
        self.print_params = kwargs['print_params']

        # performance
        self.clear_session = kwargs['clear_session']
        self.save_weights = kwargs['save_weights']

        # distributed configurations
        self.config = kwargs['config']

        self.save_timestamp = time.strftime('%D%H%M%S').replace('/', '')

        if isinstance(self.config, str):
            with open(self.config, 'r') as f:
                self.config_data = json.load(f)

        else:
            TypeError('Pass the correct `config` path')

        if 'finished_scan_run' in self.config_data.keys():
            del self.config_data['finished_scan_run']

        config = self.config_data

        with open("/tmp/arguments_remote.json", "r") as f:
            arguments_dict = json.load(f)

        self.stage = arguments_dict["stage"]

        if 'run_central_node' in config.keys():
            run_central_node = config['run_central_node']
        else:
            run_central_node = False

        from .distribute_params import run_scan
        from .distribute_database import update_db
        from .distribute_utils import return_current_machine_id

        import threading

        n_splits = len(config['machines'])
        if run_central_node:
            n_splits += 1

        update_db_n_seconds = 5
        if 'DB_UPDATE_INTERVAL' in config['database'].keys():
            update_db_n_seconds = int(config['database']['DB_UPDATE_INTERVAL'])

        current_machine_id = str(return_current_machine_id(self))

        # create the threadpool
        threads = []

        args = ([self, update_db_n_seconds, current_machine_id, self.stage])
        thread = threading.Thread(target=update_db, args=args)
        thread.start()
        threads.append(thread)

        args = (self, n_splits, run_central_node, current_machine_id)
        thread = threading.Thread(target=run_scan, args=args)

        thread.start()
        threads.append(thread)

        # excecute the threadpool
        for t in threads:
            t.join()
