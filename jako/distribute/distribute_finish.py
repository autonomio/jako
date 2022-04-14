def distribute_finish(self):

    attrs_final = ['data', 'x', 'y', 'learning_entropy', 'round_times',
                   'params', 'saved_models', 'saved_weights', 'round_history']

    keys = list(self.__dict__.keys())
    for key in keys:
        if key not in attrs_final:
            delattr(self, key)

    return self
