from experiment import Experiment

class Study():

    def __init__(self, continuable=True):
        """
        continuable : bool, The study tries to recover a previous state (true)
                      or start over (false).
        """
        pass

    def add_experiment(Experiment experiment):
        """
        Add experiment to the queue.
        """
        pass

    def run(self):
        """
        Try to recover previous state and run all/remaining experiments.
        """
        pass

    def stop(self):
        """
        Gracefully save states and stop experiments for later continuation.
        """
        pass
