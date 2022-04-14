def distribute_finish(self):
    import pandas as pd
    import os
    import json
    import numpy as np

    attrs_final = ['data', 'x', 'y', 'learning_entropy', 'round_times',
                   'params', 'saved_models', 'saved_weights', 'round_history',
                   'details']

    keys = list(self.__dict__.keys())
    for key in keys:
        if key not in attrs_final:
            delattr(self, key)

    from talos.scan.scan_addon import func_best_model, func_evaluate
    self.best_model = func_best_model.__get__(self)
    self.evaluate_models = func_evaluate.__get__(self)

    all_filenames = ['/tmp/' + file for file in os.listdir('/tmp/')]

    scan_data_list = []
    scan_details_list = []
    scan_learning_entropy_list = []
    scan_round_times_list = []
    scan_saved_models_dict = {}
    scan_round_history_dict = {}
    scan_saved_weights_dict = {}

    for file in all_filenames:
        if file.endswith('scan_data.csv'):
            df = pd.read_csv(file)
            scan_data_list.append(df)

        if file.endswith('scan_details.csv'):
            df = pd.read_csv(file)
            scan_details_list.append(df)

        if file.endswith('scan_learning_entropy.csv'):
            df = pd.read_csv(file)
            scan_learning_entropy_list.append(df)

        if file.endswith('scan_round_times.csv'):
            df = pd.read_csv(file)
            scan_round_times_list.append(df)

        if file.endswith('scan_saved_models.json'):
            with open(file, 'r') as f:
                scan_saved_model = json.load(f)
                scan_saved_models_dict.update(scan_saved_model)

        if file.endswith('scan_round_history.npy'):
            scan_round_history = np.load(file, allow_pickle=True)
            keyname = os.path.basename(file).replace(".npy", '')
            scan_round_history_dict[keyname] = scan_round_history

        if file.endswith('scan_saved_weights.npy'):
            scan_saved_weights = np.load(file, allow_pickle=True)
            keyname = os.path.basename(file).replace(".npy", '')
            scan_saved_weights_dict[keyname] = scan_saved_weights

    self.data = pd.concat(scan_data_list)
    self.details = pd.concat(scan_details_list)
    self.learning_entropy = pd.concat(scan_learning_entropy_list)
    self.round_times = pd.concat(scan_round_times_list)
    self.saved_models = scan_saved_models_dict
    self.round_history = scan_round_history_dict
    self.saved_weights = scan_saved_weights_dict

    return self
