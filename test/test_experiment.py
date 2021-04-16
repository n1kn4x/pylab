import unittest

from experiment import Experiment

class TestExperiment1(Experiment):
    def build(self):
        print("Building Test Experiment 1")
    def run(self):
        print("Running Test Experiment 1")

class TestExperiment2(Experiment):
    def build(self):
        print("Building Test Experiment 2")
    def run(self):
        print("Running Test Experiment 2")


class TestExperimentMethods(unittest.TestCase):

    def test_equals(self):
        p1 = {"a":2, "b":5}
        a1 = {"g": 0}
        e11 = TestExperiment1(p1, a1)
        e12 = TestExperiment1(p1, {})
        self.assertTrue(e11 == e12)
        self.assertTrue(e12 == e11)

        p2 = {"a":1, "c":2, "b":5}
        p3 = {"a":1, "b":5}
        e21 = TestExperiment1(p2, a1)
        e22 = TestExperiment1(p3, a1)
        self.assertFalse(e21 == e11)
        self.assertFalse(e21 == e12)
        self.assertFalse(e22 == e12)
        self.assertFalse(e22 == e11)
        self.assertFalse(e21 == e22)

if __name__ == '__main__':
    unittest.main()
