import unittest
import time
import pathlib
import random

from experiment import Experiment
from study import Study, get_id_for_dict


class TestExperiment1(Experiment):
    def build(self):
        print("Building Test Experiment 1")
    def run(self):
        print("Running Test Experiment 1")

class TestExperiment_w_name(Experiment):
    def __init__(self, p, a):
        super().__init__(p,a)
        self.name = "None"
    def build(self):
        print("Building Test Experiment: %s"%self.name)
    def run(self):
        print("Running Test Experiment: %s"%self.name)
        time.sleep(random.random()/2)

class TestStudyMethods(unittest.TestCase):

    def test_add_experiment(self):
        study = Study(name="teststudy", resourcePool={"r1":[1,2], "r2":[0,0,7]})

        p1 = {"a":2, "b":5}
        a1 = {"g": 0}
        e11 = TestExperiment1(p1, a1)
        e12 = TestExperiment1(p1, {})

        study.add_experiment(e11)
        self.assertTrue(e11 == list(study.experiments.values())[0])

        print("This should generate a warning of double add.")
        study.add_experiment(e12)
        self.assertTrue(e11 == list(study.experiments.values())[0])
        self.assertTrue(e12 == list(study.experiments.values())[0])
        self.assertTrue(len(study.experiments.values()) == 1)

        p2 = {"a":1, "c":2, "b":5}
        e21 = TestExperiment1(p2, a1)
        study.add_experiment(e21)
        self.assertTrue(len(study.experiments.values()) == 2)

    def test_acquire_and_release_resources(self):
        study = Study(name="teststudy", resourcePool={"r1":[1], "r2":[0,0,7]})
        p1 = {"a":2, "b":5}
        p2 = {"a":1, "c":2, "b":5}
        e1 = TestExperiment1(p1, {})
        e2 = TestExperiment1(p2, {})
        study.add_experiment(e1)
        study.add_experiment(e2)

        self.assertTrue(len(study.resourcePool["r1"]) == 1)
        self.assertTrue(len(study.resourcePool["r2"]) == 3)

        res = study.wait_and_acquire_resources()
        e1._fill_resources(res)
        self.assertTrue(len(study.resourcePool) == 2)
        self.assertTrue(len(study.resourcePool["r1"]) == 0)
        self.assertTrue(len(study.resourcePool["r2"]) == 2)
        study.release_resources(e1)
        self.assertTrue(len(study.resourcePool) == 2)
        self.assertTrue(len(study.resourcePool["r1"]) == 1)
        self.assertTrue(len(study.resourcePool["r2"]) == 3)

    def test_run_all(self):
        study = Study(name="teststudy", resourcePool={"r1":[1,2], "r2":[0,0,7]})
        p1 = {"a":2, "b":5}
        p2 = {"a":1, "c":2, "b":5}
        e1 = TestExperiment_w_name(p1, {})
        e2 = TestExperiment_w_name(p2, {})
        e1.name = "Test01"
        e2.name = "Test02"
        study.add_experiment(e1)
        study.add_experiment(e2)

        self.assertTrue(len(study.resourcePool) == 2)
        self.assertTrue(len(study.resourcePool["r1"]) == 2)
        self.assertTrue(len(study.resourcePool["r2"]) == 3)
        #print(study.resourcePool)
        study.run_all()
        time.sleep(1)
        #print(study.resourcePool)
        self.assertTrue(len(study.resourcePool) == 2)
        self.assertTrue(len(study.resourcePool["r1"]) == 2)
        self.assertTrue(len(study.resourcePool["r2"]) == 3)

    def save_exp(self):
        study = Study(name="teststudy", resourcePool={"r1":[1,2], "r2":[0,0,7]})
        p1 = {"a":2, "b":5}
        e1 = TestExperiment1(p1, {})
        study.add_experiment(e1)
        study.save_exp(e1)

        fn = self.exp_result_dir + get_id_for_dict(exp.parameters)
        path = pathlib.Path(fn)
        self.assertEquals((str(path), path.is_file()), (str(path), True))



if __name__ == '__main__':
    unittest.main()
