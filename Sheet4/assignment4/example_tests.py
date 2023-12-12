"""
Some test cases in a similar way to the ones used for grading your submissions.
The actual grading will test many corner cases not considered here.
Feel free to add more complex test cases here.
More information about the used testing framework can be found in the LernraumPlus as
well as the tutorial sessions.
This makes use of the unittest framework.
In general, testing approximate sampling is a lot more tricky than other assignments
as there is randomness in the approximate methods, these tests thus may
report failures due to slight inaccuracies. I will need to manually
revise each submission manually regardless of test outcome but you can still
check if your solution works in general. 

author: Jan Pöppel
last modified. 23.11.2021
"""

import unittest
import random
import assignment4 as solution

import numpy as np

from ccbase.nodes import DiscreteVariable



class TestAssignment5(unittest.TestCase):

    def get_trivial_net(self):
        net = solution.BayesianNetwork()
        a = solution.DiscreteVariable("A", ["True", "False"])
        b = solution.DiscreteVariable("B", ["True", "False"])
        c = solution.DiscreteVariable("C", ["True", "False"])
        d = solution.DiscreteVariable("D", ["True", "False"])
        net.add_node(a)
        net.add_node(b)
        net.add_node(c)
        net.add_node(d)
        net.add_edge(b, a)
        net.add_edge(c, b)
        net.add_edge(b, d)
        a.set_probability_table(np.array([[0.2, 0.3], [0.8, 0.7]]))
        b.set_probability_table(np.array([[0.6, 0.8], [0.4, 0.2]]))
        c.set_probability_table(np.array([0.4, 0.6]))
        d.set_probability_table(np.array([[0.4, 0.2], [0.6, 0.8]]))
        return net
        
        
    
    def test_maximize_out(self):
        f = solution.Factor(["A","B"], {"A":["True","False"], "B": ["True","False"]}, np.array([[0.2,0.3],[0.8,0.7]]))
        res = solution.maximize_out(f, "B")
        np.testing.assert_almost_equal(res.potentials, np.array([0.3, 0.8]))

    def test_max_product_elim_var(self):
        f1 = solution.Factor(["A","B"], {"A":["True","False"], "B": ["True","False"]}, np.array([[0.2,0.3],[0.8,0.7]]))
        f2 = solution.Factor(["B"], {"B": ["True","False"]}, np.array([0.4,0.6]))
        res_list, res_f = solution.max_product_elim_var([f1,f2], "B")
        self.assertEqual(len(res_list), 1)
        np.testing.assert_almost_equal(res_list[0].potentials, np.array([0.18, 0.42]))
        np.testing.assert_almost_equal(res_f.potentials, np.array([[0.08, 0.18], [0.32, 0.42]]))

    def test_traceback(self):
        max_a_factor = solution.Factor(["A"], {"A": ["True","False"]}, np.array([0.18,0.42]))
        max_b_factor = solution.Factor(["A","B"], {"A":["True","False"], "B": ["True","False"]}, np.array([[0.08, 0.18], [0.32, 0.42]]))
        res = solution.traceback({"A": max_a_factor, "B": max_b_factor}, ["B", "A"])
        self.assertEqual(res, {"A": "False", "B":"False"})

    def test_calculate_MAP(self):
        net = self.get_trivial_net()
        res_prob, res_map = solution.calculate_MAP(net)
        self.assertEqual(res_prob, 0.2304)
        self.assertEqual(res_map, {'A': 'False', 'B': 'True', 'C': 'False', 'D': 'False'})
        

    def test_sample(self):
        exampleNode = DiscreteVariable("color", 
                               ["red","green", "blue"], 
                               np.array([0.15,0.55,0.3]))
	
        self.assertTrue(solution.sample(exampleNode.get_distribution()) in ["red","green","blue"], "Sample frequency not matching actual distribution")

    def test_get_ancestral_ordering(self):
        self.assertTrue(solution.get_ancestral_ordering(solution.get_wetgrass_network()) == ['winter', 'sprinkler', 'rain', 'wet_grass', 'dry_fields'])


    def test_do_forward_sampling(self):
        fs = solution.do_forward_sampling(solution.get_wetgrass_network(), "wet_grass", 10000 )
        self.assertAlmostEqual(fs["True"],0.7,1)
        self.assertAlmostEqual(fs["False"], 0.3, 1)

    def test_get_markov_distr_simple(self):
        net = self.get_trivial_net()
        a = net.nodes["A"]
        evidence = {"A":"True", "B":"False", "C":"True", "D":"False"}
        true_distr = {"True": 0.3, "False": 0.7}
        distr = solution.get_markov_distr(a, evidence)
        norm = sum(distr.values())
        distr = {k:v/norm for k,v in distr.items()}
        for key in distr:
            self.assertAlmostEqual(distr[key], true_distr.get(key,0), 5, "The local distr for A={} needs to be this".format(key))

    def test_do_gibbs_sampling(self):
        gs = solution.do_gibbs_sampling(solution.get_wetgrass_network(), "wet_grass", {"slippery_road": "True"}, 10000, 100, 1)
        self.assertAlmostEqual(gs["True"], 0.7, 1)
        self.assertAlmostEqual(gs["False"], 0.3, 1)

if __name__ == "__main__":
    unittest.main()
