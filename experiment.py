from abc import ABC

class Experiment():

    def __init__(self, parameters, attributes):
        """
        parameters : dict, Parameters of the experiment. Will be used to identify
                     an instance of the experiment.
        attributes : dict, Additional attributes of the experiment. Will not be
                     used to identify and instance of the experiment.
        """
        pass

    def build(self):
        """
        Prepare and initialize the experiment.
        """
        pass

    def run(self):
        """
        Run the experiment.
        """
        pass
