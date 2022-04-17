def script_script():

    out = '''
from jako import RemoteScan
import numpy as np
import json
import pickle
x=np.load('/tmp/x_data_remote.npy')
y=np.load('/tmp/y_data_remote.npy')

{}
with open('/tmp/arguments_remote.json','r') as f:
    arguments_dict=json.load(f)

t=RemoteScan(x=x,
             y=y,
             params=arguments_dict['params'],
             model={},
             experiment_name=arguments_dict['experiment_name'],
             x_val=arguments_dict['x_val'],
             y_val=arguments_dict['y_val'],
             val_split=arguments_dict['val_split'],
             random_method=arguments_dict['random_method'],
             seed=arguments_dict['seed'],
             performance_target=arguments_dict['performance_target'],
             fraction_limit=arguments_dict['fraction_limit'],
             round_limit=arguments_dict['round_limit'],
             time_limit=arguments_dict['time_limit'],
             boolean_limit=arguments_dict['boolean_limit'],
             reduction_method=arguments_dict['reduction_method'],
             reduction_interval=arguments_dict['reduction_interval'],
             reduction_window=arguments_dict['reduction_window'],
             reduction_threshold=arguments_dict['reduction_threshold'],
             reduction_metric=arguments_dict['reduction_metric'],
             minimize_loss=arguments_dict['minimize_loss'],
             disable_progress_bar=arguments_dict['disable_progress_bar'],
             print_params=arguments_dict['print_params'],
             clear_session=arguments_dict['clear_session'],
             save_weights=arguments_dict['save_weights'],
             config='/tmp/remote_config.json'
             )'''

    return out
