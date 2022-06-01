from talos import Scan


class DistributedScan(Scan):

    def __init__(self,
                 x,
                 y,
                 params,
                 model,
                 experiment_name,
                 x_val=None,
                 y_val=None,
                 val_split=0.3,
                 random_method='uniform_mersenne',
                 seed=None,
                 performance_target=None,
                 fraction_limit=None,
                 round_limit=None,
                 time_limit=None,
                 boolean_limit=None,
                 reduction_method=None,
                 reduction_interval=50,
                 reduction_window=20,
                 reduction_threshold=0.2,
                 reduction_metric='val_acc',
                 minimize_loss=False,
                 disable_progress_bar=False,
                 print_params=False,
                 clear_session=True,
                 save_weights=True,
                 config='config.json'):
        '''Distributed version of talos.Scan() for the local machine.

        Parameters
        ----------
        params | `dict` | Hyperparameters for distribution.
        config | str or dict | The default is 'config.json'.

        Returns
        -------
        None.

        '''

        import time
        import json
        import os
        import inspect
        import numpy as np

        self.x = x
        self.y = y
        self.params = params
        self.model = model
        self.experiment_name = experiment_name
        self.x_val = x_val
        self.y_val = y_val
        self.val_split = val_split

        # randomness
        self.random_method = random_method
        self.seed = seed

        # limiters
        self.performance_target = performance_target
        self.fraction_limit = fraction_limit
        self.round_limit = round_limit
        self.time_limit = time_limit
        self.boolean_limit = boolean_limit

        # optimization
        self.reduction_method = reduction_method
        self.reduction_interval = reduction_interval
        self.reduction_window = reduction_window
        self.reduction_threshold = reduction_threshold
        self.reduction_metric = reduction_metric
        self.minimize_loss = minimize_loss

        # display
        self.disable_progress_bar = disable_progress_bar
        self.print_params = print_params

        # performance
        self.clear_session = clear_session
        self.save_weights = save_weights

        # distributed configurations
        self.config = config

        arguments_dict = self.__dict__
        remove_parameters = ['x', 'y', 'model']
        arguments_dict = {k: v for k, v in arguments_dict.items()
                          if k not in remove_parameters}

        self.file_path = '/tmp/{}/scanfile_remote.py'.format(
            self.experiment_name)

        self.save_timestamp = time.strftime('%D%H%M%S').replace('/', '')

        # Handle the case when `config` is a filename
        if isinstance(config, str):
            with open(config, 'r') as f:
                self.config_data = json.load(f)

        # Handle the case when `config` is dict
        if isinstance(config, dict):
            self.config_data = config
            with open('config.json', 'w') as outfile:
                json.dump(self.config_data, outfile, indent=2)

        else:
            TypeError('`config` must be dict or filename string.')

        # write database name as same as experiment name
        self.config_data['database']['DB_TABLE_NAME'] = experiment_name
        run_docker = False

        if 'run_docker' in self.config_data.keys():
            run_docker = self.config_data['run_docker']

        if run_docker:
            self.config_data['database']['DATABASE_NAME'] = 'postgres'

        if isinstance(config, str):
            config_path = config

        else:
            config_path = 'config.json'

        with open(config_path, 'w') as f:
            json.dump(self.config_data, f, indent=2)

        if 'finished_scan_run' in self.config_data.keys():
            del self.config_data['finished_scan_run']

        # handles location for params,data and model
        inputs_path = '/tmp/{}'.format(self.experiment_name)
        if not os.path.exists(inputs_path):
            os.mkdir(inputs_path)

        self.dest_dir = '/tmp/'

        # save data in numpy format
        np.save('/tmp/{}/jako_x_data_remote.npy'.format(self.experiment_name),
                x)
        np.save('/tmp/{}/jako_y_data_remote.npy'.format(self.experiment_name),
                x)

        # get model function as a string
        model_func = inspect.getsource(model).lstrip()

        self.model_func = model_func
        self.model_name = model.__name__

        with open('/tmp/{}/jako_arguments_remote.json'.format(
                self.experiment_name), 'w') as outfile:

            json.dump(arguments_dict, outfile, indent=2)

        with open('/tmp/{}/jako_remote_config.json'.format(
                self.experiment_name), 'w') as outfile:
            json.dump(self.config_data, outfile, indent=2)

        from .distribute_run import distribute_run
        distribute_run(self)
