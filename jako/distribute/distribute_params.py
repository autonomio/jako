from talos import Scan
from .distribute_utils import read_config, write_config, write_scan_namespace


def create_param_space(self, n_splits):
    '''Creates the parameter space for each machine

    Parameters
    ----------
    n_splits | int | The default is 2.

    Returns
    -------
    param_grid | `list` of `dict` | Split parameter spaces for each machine.

    '''

    from talos.parameters.DistributeParamSpace import DistributeParamSpace

    params = self.params
    param_keys = self.params.keys()

    random_method = self.random_method
    fraction_limit = self.fraction_limit
    round_limit = self.round_limit
    time_limit = self.time_limit
    boolean_limit = self.boolean_limit

    param_grid = DistributeParamSpace(params=params,
                                      param_keys=param_keys,
                                      random_method=random_method,
                                      fraction_limit=fraction_limit,
                                      round_limit=round_limit,
                                      time_limit=time_limit,
                                      boolean_limit=boolean_limit,
                                      machines=n_splits)

    return param_grid


def run_scan(self, machines, run_central_node, machine_id):
    '''Run `talos.Scan()` on each machine.

    Parameters
    ----------
    machines | int |
    run_central_node | bool |

    Returns
    -------
    None.

    '''

    # runs Scan in a machine after param split
    machine_id = int(machine_id)
    current_machine_id = machine_id

    if not run_central_node:
        if machine_id != 0:
            machine_id = machine_id - 1

    split_params = create_param_space(self, n_splits=machines)
    split_params = split_params.param_spaces[machine_id]

    print('Started experiment in machine id : {}'.format(current_machine_id))

    scan_object = Scan(x=self.x,
                       y=self.y,
                       params=split_params,
                       model=self.model,
                       experiment_name=self.experiment_name,
                       x_val=self.x_val,
                       y_val=self.y_val,
                       val_split=self.val_split,
                       random_method=self.random_method,
                       seed=self.seed,
                       performance_target=self.performance_target,
                       fraction_limit=self.fraction_limit,
                       round_limit=self.round_limit,
                       time_limit=self.time_limit,
                       boolean_limit=self.boolean_limit,
                       reduction_method=self.reduction_method,
                       reduction_interval=self.reduction_interval,
                       reduction_window=self.reduction_window,
                       reduction_threshold=self.reduction_threshold,
                       reduction_metric=self.reduction_metric,
                       minimize_loss=self.minimize_loss,
                       disable_progress_bar=self.disable_progress_bar,
                       print_params=self.print_params,
                       clear_session=self.clear_session,
                       save_weights=self.save_weights)

    print('Completed experiment in machine id : {}'.format(current_machine_id))

    new_config = read_config(self)
    new_config['finished_scan_run'] = True

    if int(current_machine_id) == 0:
        new_config['current_machine_id'] = 0

    write_config(self, new_config)
    write_scan_namespace(self, scan_object, current_machine_id)
