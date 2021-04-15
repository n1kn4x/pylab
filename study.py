from threading import Thread, Lock
import time
import pickle
import logging

from experiment import Experiment

class Study():

    def __init__(self, name: str, resourcePool: dict, continuable: bool=True):
        """
        resourcePool: dict of key:list, where the key denotes the resource type and
                      and the list contains the resources. e.g. {"gpu":[0,1,2]}
        continuable : bool, The study tries to recover a previous state (true)
                      or start over (false).
        """
        self.name = name
        self.resourcePool = resourcePool
        self.resourcePool_Lock = Lock()
        self.continuable = continuable
        self.experiments = {} # dict mapping uuid : experiment

        self.exp_result_dir = "~/studies/%s/" % self.name
        create_folders(self.exp_result_dir)

    def add_experiment(experiment):
        """
        Add experiment to the queue.
        """
        if (experiment in self.experiments):
            logging.warning("Experiment is already included in study. Skipping it.")
        self.experiments.append(experiment)

    def wait_and_acquire_resources(self):
        """
        Wait until a full set of resources for one experiment are available
        and acquires them. Returns the resources as a dict.
        """
        res, are_res_filled = False, {}
        while not are_res_filled:
            # Check if resource is available and required
            self.resourcePool_Lock.acquire()
            for key in resourcePool:
                if (len(resourcePool[key]) > 0 and not key in res):
                    res[key] = resourcePool[key].pop()
            # Check if all resources are filled
            if (set(resourcePool.keys()) == set(res.keys())):
                are_res_filled = True
            # Give running threads a chance to return resources
            self.resourcePool_Lock.release()
            time.sleep(100)
        return res

    def release_resources(self, exp: Experiment):
        """
        Returns the used resources of the experiment to the resource pool.
        """
        self.resourcePool_Lock.acquire()
        for key in exp.resources:
            self.resourcePool[key].append(exp.resources[key])
        exp.resources = {}
        self.resourcePool_Lock.release()

    def run_all(self):
        """
        Try to recover previous state and run all/remaining experiments.
        """
        for exp in self.experiments:
            # Check if experiment file already exists
            expid = get_id_for_dict(exp.parameters)
            if exists_file(self.exp_result_dir + expid):
                print("Experiment with id %s exists. Skipping.")
            self.run_experiment(exp)

    def run_experiment(self, exp: Experiment):
        """
        Runs an experiment in a new thread. After its done, the experiment is
        saved and the resources are returned to the resource pool.
        """
        res = self.wait_and_acquire_resources()
        exp._fill_resources(res)
        # Resources for the experiment are filled. ready to start
        t = Thread(target=run_with_cleanup, args=(self, exp))

    def run_with_cleanup(self, exp: Experiment):
        """
        Runs the experiment, saves the result and releases the used resources.
        """
        exp.run()
        self.save_exp(exp)
        self.release_resources(exp)

    def save_exp(self, exp: Experiment):
        """
        Saves an experiment. Most probably gonna change.
        """
        fn = self.exp_result_dir + get_id_for_dict(exp.parameters)
        with open(fn, 'wb+') as outfile:
            pickle.dump(exp, outfile)

    def stop(self):
        """
        Gracefully save states and stop experiments for later continuation.
        """
        pass

    def save(self):
        pass


import hashlib
from pathlib import Path #pip install pathib2

def get_id_for_dict(d: dict):
    unique_str = ''.join(["'%s':'%s';"%(key, val) for (key, val) in sorted(d.items())])
    return hashlib.sha1(unique_str).hexdigest()

def exists_file(fn: str):
    if Path(fn).is_file():
        return true
    else:
        return false

def create_folders(fp: str):
    Path(fp).mkdir(parents=True, exist_ok=True)
