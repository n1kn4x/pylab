import unittest

from experiment import Experiment

class TestExperiment1(Experiment):
    def build():
        print("Building Test Experiment 1")
    def run():
        print("Running Test Experiment 1")

class TestExperiment2(Experiment):
    def build():
        print("Building Test Experiment 2")
    def run():
        print("Running Test Experiment 2")


class TestExperimentMethods(unittest.TestCase):

    def test_equals(self):
        p1 = {"a":2, "b":5}
        a1 = {"g": 0}
        e11 = TestExperiment1(p1, a1)
        e12 = TestExperiment1(p1, {})
        self.assertTrue(e11 == e12)
        self.assertTrue(e12 == e11)

if __name__ == '__main__':
    unittest.main()
