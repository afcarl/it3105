from blind_test import ann
import demo

"""
import unittest
import pickle

class TestAnn(unittest.TestCase):
    def test_ann(self):
        demo_set_filename = 'demo_python2'
        demo_set = pickle.load(open(demo_set_filename, "rb"))

        feature_sets = demo_set[0]
        expected = map(int, demo_set[1])
        n = ann()
        actual = n.blind_test(feature_sets)

        num_correct = 0
        for i in range(len(expected)):
            if actual[i] == expected[i]:
                num_correct += 1

        print('Accuracy:', float(num_correct) / len(expected))


if __name__ == '__main__':
    unittest.main()
"""

demo.minor_demo(ann)
