from abc import ABC, abstractmethod

class Experiment():

    def __init__(self, parameters: dict, attributes: dict):
        """
        parameters : dict, Parameters of the experiment. Will be used to identify
                     an instance of the experiment.
        attributes : dict, Additional attributes of the experiment. Will not be
                     used to identify and instance of the experiment.
        """
        self.parameters = parameters
        self.attributes = attributes

    @abstractmethod
    def build(self):
        """
        Prepare and initialize the experiment.
        """
        pass

    @abstractmethod
    def run(self):
        """
        Run the experiment.
        """
        pass


    def __eq__(self, other):
        """
        Return true if the parameters and the type are the same.
        """
        if not (isinstance(other, type(self)) and isinstance(self, type(other))):
            return false
        return self.parameters == other.parameters
