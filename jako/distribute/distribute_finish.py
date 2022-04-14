def distribute_finish(self):

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

    return self
