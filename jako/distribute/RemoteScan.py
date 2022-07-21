from talos import Scan


class RemoteScan(Scan):
    def __init__(self,
                 x,
                 y,
                 params,
                 model,
                 experiment_name,
                 x_val,
                 y_val,
                 **kwargs):
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

        self.x = x
        self.y = y
        self.params = params
        self.model = model
        self.experiment_name = experiment_name
        self.x_val = x_val
        self.y_val = y_val
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
        status_details = {}

        with open("/tmp/{}/jako_arguments_remote.json".format(
                self.experiment_name), "r") as f:
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

        status_details['total_nodes'] = n_splits

        update_db_n_seconds = 5
        if 'DB_UPDATE_INTERVAL' in config['database'].keys():
            update_db_n_seconds = int(config['database']['DB_UPDATE_INTERVAL'])

        current_machine_id = str(return_current_machine_id(self))

        status_details['experiment_stage'] = int(self.stage)
        status_details['machine_id'] = int(current_machine_id)
        # create the threadpool
        threads = []

        args = ([self, update_db_n_seconds, current_machine_id, self.stage,
                 status_details])
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
