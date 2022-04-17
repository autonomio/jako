import json
import paramiko
import os
import pandas as pd
import datetime


def create_temp_file(self):
    filestr = '''
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
             )
    '''.format(self.model_func, self.model_name)

    with open("/tmp/scanfile_remote.py", "w") as f:
        f.write(filestr)


def return_current_machine_id(self,):
    ''' Return machine id after checking the ip from config'''

    current_machine_id = 0
    if 'current_machine_id' in self.config_data.keys():
        current_machine_id = int(self.config_data['current_machine_id'])

    return current_machine_id


def return_central_machine_id(self):
    ''' Return central machine id as mentioned in config'''
    central_id = 0
    config_data = self.config_data
    if 'database' in config_data.keys():
        central_id = int(config_data['database']['DB_HOST_MACHINE_ID'])
    return central_id


def read_config(self):
    '''Read config from file'''

    config_path = "/tmp/remote_config.json"

    with open(config_path, 'r') as f:
        config_data = json.load(f)

    return config_data


def write_config(self, new_config):
    ''' Write config to file'''

    config_path = "/tmp/remote_config.json"

    with open(config_path, 'w') as outfile:
        json.dump(new_config, outfile, indent=2)


def ssh_connect(self):
    '''
    Returns
    -------
    clients | `list` | List of client objects of machines after connection.

    '''

    configs = self.config_data['machines']
    clients = {}

    for config in configs:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        host = config['JAKO_IP_ADDRESS']
        port = config['JAKO_PORT']
        username = config['JAKO_USER']

        if 'JAKO_PASSWORD' in config.keys():
            password = config['JAKO_PASSWORD']
            client.connect(host, port, username, password)

        elif 'JAKO_KEY_FILENAME' in config.keys():
            client.connect(host, port, username,
                           key_filename=config['JAKO_KEY_FILENAME'])

        clients[config['machine_id']] = client

    return clients


def ssh_file_transfer(self, client, machine_id):
    '''Transfer the current talos script to the remote machines'''

    create_temp_file(self)

    sftp = client.open_sftp()

    try:
        sftp.chdir(self.dest_dir)  # Test if dest dir exists

    except IOError:
        sftp.mkdir(self.dest_dir)  # Create dest dir
        sftp.chdir(self.dest_dir)

    data_files = ['y_data_remote.npy', 'x_data_remote.npy']
    scan_script_files = ['scanfile_remote.py']
    additional_scan_files = ['remote_config.json', 'arguments_remote.json']
    scan_filenames = data_files + scan_script_files + additional_scan_files
    for file in os.listdir("/tmp/"):
        if file in scan_filenames:
            sftp.put("/tmp/" + file, file)

    sftp.close()


def ssh_run(self, client, machine_id):
    '''Run the transmitted script remotely without args and show its output.

    Parameters
    ----------
    client | `Object` | paramiko ssh client object
    params | `dict`| hyperparameter options
    machine_id | `int`| Machine id for each of the distribution machines

    Returns
    -------
    None.

    '''
    execute_str = 'python3 /tmp/scanfile_remote.py'
    stdin, stdout, stderr = client.exec_command(execute_str)

    if stderr:
        for line in stderr:
            try:
                # Process each error line in the remote output
                print(line)
            except Exception as e:
                print(e)

    for line in stdout:
        try:
            # Process each line in the remote output
            print(line)
        except Exception as e:
            print(e)


def ssh_get_files(self, client, machine_id):
    '''Get files via ssh from a machine'''
    sftp = client.open_sftp()

    scan_object_filenames = ('scan_details.csv', 'scan_learning_entropy.csv',
                             'scan_round_history.npy', 'scan_round_times.csv',
                             'scan_saved_models.json', 'scan_saved_weights.npy',
                             'scan_data.csv')

    sftp.chdir(self.dest_dir)

    for file in sftp.listdir(self.dest_dir):
        if file.endswith(scan_object_filenames):
            sftp.get(self.dest_dir + file, '/tmp/' + file)

    sftp.close()


def fetch_latest_file(self):
    '''Fetch the latest csv for an experiment'''

    experiment_name = self.experiment_name
    save_timestamp = self.save_timestamp

    if not os.path.exists(experiment_name):
        return []

    filelist = []
    for file in os.listdir(experiment_name):
        if file.endswith('.csv'):
            if int(file.replace('.csv', '')) >= int(save_timestamp):
                latest_file = os.path.join(experiment_name, file)
                filelist.append(latest_file)

    if filelist:
        latest_filepath = max(filelist, key=os.path.getmtime)

        try:
            results_data = pd.read_csv(latest_filepath)
            return results_data
        except Exception as e:
            e = str(e)
            allowed_exception = 'No columns to parse from file'

            if allowed_exception in e:
                return []
            else:
                raise Exception(e)
    else:
        return []


def add_timestamp(self, results_data):
    '''Adds timestamp to the DataFrame'''

    ct = datetime.datetime.now()
    hour = ct.hour
    minute = ct.minute
    day = ct.day
    month = ct.month
    year = ct.year

    if minute < 10:
        minute = '0' + str(minute)

    if hour < 10:
        hour = '0' + str(hour)

    timestamp = "{}:{}/{}-{}-{}".format(hour, minute, day, month, year)
    results_data["timestamp"] = [timestamp] * len(results_data)

    return results_data


def get_experiment_stage(self, db):
    '''Get the current number of times of experiment run'''

    try:
        ids = db.return_existing_experiment_ids()
        stage = int(list(ids)[-1].split("-")[0]) + 1

    except Exception as e:
        allowed_exception = '(psycopg2.errors.UndefinedTable)'
        e = str(e)
        if allowed_exception in e:
            pass
        else:
            raise Exception(e)

        stage = 0

    return stage


def add_experiment_id(self, results_data, machine_id, start_row,
                      end_row, db, stage):
    '''Generate experiment id from model id and row number'''

    try:
        ids = db.return_existing_experiment_ids()
        if "experiment_id" in results_data.columns:
            results_data = results_data[~results_data['experiment_id'].isin(ids
                                                                            )]

    except Exception as e:
        allowed_exception = '(psycopg2.errors.UndefinedTable)'
        e = str(e)
        if allowed_exception in e:
            pass
        else:
            raise Exception(e)

    results_data = results_data.iloc[start_row:end_row]
    experiment_ids = []
    for i in range(start_row, end_row):
        experiment_id = str(stage) + "-" + str(machine_id) + "-" + str(i)
        experiment_ids.append(experiment_id)
    results_data["experiment_id"] = experiment_ids

    return results_data


def write_scan_namespace(self, scan_object, machine_id):
    '''

    Parameters
    ----------
    scan_object | talos.Scan object | Scan object after Scan run

    Returns
    -------
    None.

    '''
    import pandas as pd
    import json
    import numpy as np
    import os

    write_path = os.path.join('/tmp/', 'machine_id_' + str(machine_id) + '_')
    scan_details = scan_object.details
    scan_data = scan_object.data
    scan_learning_entropy = scan_object.learning_entropy
    scan_round_history = scan_object.round_history
    scan_round_times = scan_object.round_times
    scan_saved_models = scan_object.saved_models
    scan_saved_weights = scan_object.saved_weights

    details_df = pd.DataFrame({'scan_details': scan_details})
    details_df.to_csv(write_path + 'scan_details.csv')

    scan_data.to_csv(write_path + 'scan_data.csv')
    scan_learning_entropy.to_csv(write_path + 'scan_learning_entropy.csv')
    scan_round_times.to_csv(write_path + 'scan_round_times.csv')

    np.save(write_path + 'scan_round_history.npy', scan_round_history)

    with open(write_path + 'scan_saved_models.json', 'w') as f:
        scan_saved_models = {'saved_models_machine_id_' + str(machine_id):
                             scan_saved_models}
        json.dump(scan_saved_models, f, indent=2)

    np.save(write_path + 'scan_saved_weights.npy', scan_saved_weights)
