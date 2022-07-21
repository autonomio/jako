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
        '''
    Distributed version of talos.Scan() for the local machine.
    USE: jako.DistributedScan(x=x,
                                y=y,
                                params=params_dict,
                                model=model,
                                config=config)
    # CORE ARGUMENTS
    ----------------
    x : ndarray
        1d or 2d array, or a list of arrays with features for the prediction
        task.
    y : ndarray
        1d or 2d array, or a list of arrays with labels for the prediction
        task.
    params : dict
        Lists all permutations of hyperparameters, a subset of which will be
        selected at random for training and evaluation.
    model : keras model
        Any Keras model with relevant declrations like params['first_neuron']
    experiment_name : str
        Experiment name will be used to produce a folder (unless already) it's
        there from previous iterations of the experiment. Logs of the
        experiment are saved in the folder with timestamp of start
        time as filenames.
    x_val : ndarray
        User specified cross-validation data. (Default is None).
    y_val : ndarray
        User specified cross-validation labels. (Default is None).
    val_split : float, optional
        The proportion of the input `x` which is set aside as the
        validation data. (Default is 0.3).
    multi_input : bool, optional
        If it is a multi_input model, then set to True.
    # RANDOMNESS ARGUMENTS
    ----------------------
    random_method : str
        Determinines the way in which the grid_downsample is applied. The
        default setting is 'uniform_mersenne'.
    seed : int
        Sets numpy random seed.
    # LIMITER ARGUMENTS
    -------------------
    performance_target : None or list [metric, threshold, loss or not]
        Allows setting a threshold for a given metric, at which point the
        experiment will be concluded as successful.
        E.g. performance_target=['f1score', 0.8, False]
    fraction_limit : int
        The fraction of `params` that will be tested (Default is None).
        Previously grid_downsample.
    round_limit : int
        Limits the number of rounds (permutations) in the experiment.
    time_limit : None or str
        Allows setting a time when experiment will be completed. Use the format
        "%Y-%m-%d %H:%M" here.
    boolean_limit : None or lambda function
        Allows setting a limit to accepted permutations as a lambda function.
        E.g. example lambda p: p['first_neuron'] * p['hidden_layers'] < 220
    # OPTIMIZER ARGUMENTS
    ---------------------
    reduction_method : None or string
        If None, random search will be used as the optimization strategy.
        Otherwise use the name of the specific strategy, e.g. 'correlation'.
    reduction_interval : None or int
        The number of reduction method rounds that will be performed. (Default
        is None).
    reduction_window : None or int
        The number of rounds of the reduction method before observing the
        results. (Default is None).
    reduction_threshold: None or float
        The minimum value for reduction to be applied. For example, when
        the 'correlation' reducer finds correlation below the threshold,
        nothing is reduced.
    reduction_metric : None or str
        Metric used to tune the reductions. minimize_loss has to be set to True
        if this is a loss.
    minimize_loss : bool
        Must be set to True if a reduction_metric is a loss.
    # OUTPUT ARGUMENTS
    ------------------
    disable_progress_bar : bool
        Disable TQDM live progress bar.
    print_params : bool
        Print params for each round on screen (useful when using TrainingLog
        callback for visualization)
    # CONFIG ARGUMENTS
    -----------------
    config : str or dict | Path or dict containing details of
                            Distributed Machines and database.

    # OTHER ARGUMENTS
    -----------------
    clear_session : bool
        If the backend session is cleared between every permutation.
    save_weights : bool
        If set to False, then model weights will not be saved and best_model
        and some other features will not work. Will reduce memory pressure
        on very large models and high number of rounds/permutations.
    save_models : bool
        If True, models will be saved on the local disk in theexperiment
        folder. When `save_models` is set to True, you should consider setting
        `save_weights` to False.


        '''

        import time
        import json
        import os
        import inspect
        import numpy as np

        # remove all pre-existing input files
        self.experiment_name = experiment_name

        # handles location for params,data and model
        if not os.path.exists('/tmp/{}'.format(
                self.experiment_name)):
            os.mkdir('/tmp/{}/'.format(self.experiment_name))

        for file in os.listdir('/tmp/{}'.format(
                self.experiment_name)):
            if file.startswith('jako'):
                os.remove('/tmp/{}/'.format(self.experiment_name) + file)

        self.x = x
        self.y = y
        self.params = params
        self.model = model
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

        for file in os.listdir('/tmp/{}'.format(
                self.experiment_name)):
            if file.startswith('jako'):
                os.remove('/tmp/{}'.format(self.experiment_name) + file)

        arguments_dict = self.__dict__
        remove_parameters = ['x', 'y', 'model', 'x_val', 'y_val']
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

        self.dest_dir = '/tmp/{}/'.format(self.experiment_name)

        # save data in numpy format
        np.save('/tmp/{}/jako_x_data_remote.npy'.format(
                self.experiment_name), x)
        np.save('/tmp/{}/jako_y_data_remote.npy'.format(
                self.experiment_name), y)

        try:
            x_val.shape
            y_val.shape
            np.save('/tmp/{}/jako_x_val_data_remote.npy'.format(
                    self.experiment_name), x_val)
            np.save('/tmp/{}/jako_y_val_data_remote.npy'.format(
                    self.experiment_name), y_val)
        except AttributeError:
            pass
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
