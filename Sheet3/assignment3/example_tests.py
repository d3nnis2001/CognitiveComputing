"""
Some test cases in a similar way to the ones used for grading your submissions.
The actual grading will test many corner cases not considered here.
Feel free to add more complex test cases here.
More information about the used testing framework can be found in the LernraumPlus as
well as the tutorial sessions.
This makes use of the unittest framework

author: Hendric Voß
last modified. 13.11.2022
"""

import unittest
import numpy as np
import assignment3 as solution

class TestAssignment3(unittest.TestCase):

    def test_is_collider(self):
        graph = self._create_example_graph()
        path = ["B","A","E"]
        self.assertTrue(solution.is_collider(graph, "A", path), "A is a collider on this path.")

    def test_is_path_open(self):
        graph = self._create_example_graph()
        path = ["B","A","E"]
        self.assertTrue(solution.is_path_open(graph, path, ["A"]), "Path BAE is open if A is given.")

    def test_unblocked_path_exists_collider_given(self):
        graph = self._create_example_graph()
        self.assertFalse(solution.unblocked_path_exists(graph, "B", "E", []), "The only path is blocked by the collider.")
        self.assertTrue(solution.unblocked_path_exists(graph, "B", "E", ["A"]), "The evidence of the collider opens the path.")
        
    def test_check_indepedence_dsep(self):
        graph = self._create_example_graph()
        self.assertTrue(solution.check_independence(graph, ["B"], ["E"], ["R"]), "B and E are conditionally indepedent given E")
        self.assertFalse(solution.check_independence(graph, ["B"], ["E"], ["A"]), "B and E are conditionally dependent given A")

    def test_ancestral_graph(self):
        graph = self._create_lecture_graph()
        query_nodes = ["A","I","F","L"]
        ancestral_graph =solution.make_ancestral_graph(graph, query_nodes)
        self.assertFalse("G" in ancestral_graph.nodes, "G is not part of the ancestral graph")

    def test_moral_graph(self):
        graph = self._create_lecture_graph()
        moral_graph = solution.make_moral_graph(graph)
        self.assertFalse(moral_graph.is_directed, "The moral graph should no longer be directed.")
        self.assertEqual(set(graph.nodes.keys()), set(moral_graph.nodes.keys()), "A moral graph should not lose any nodes")

    def test_separation(self):
        graph = self._create_lecture_graph()
        res = solution.separation(graph, ["F", "L"])
        self.assertFalse("F" in res.nodes["H"].children, "There should no longer be an edge between F and H")
        self.assertFalse("F" in res.nodes["D"].children, "There should no longer be an edge between F and D")
        self.assertFalse("L" in res.nodes["H"].children, "There should no longer be an edge between L and H")

    def test_check_independence_general(self):
        graph = self._create_lecture_graph()
        self.assertFalse(solution.check_independence_general(graph, ["A"], ["I"], ["L","F"]), "A and I are conditionnaly dependent given L and F")
        
    def test_elimination_order_minFill(self):
        net = self._create_lecture_graph()
        # order = solution.get_elimination_order_minfill(net)
        order = solution.get_elimination_ordering(net.copy())
        true_order = ['A', 'B', 'G', 'L', 'C', 'D', 'I', 'M', 'E', 'F', 'H']
        self.assertEqual(order, true_order, "MinFillHeuristic produces this order")    
        
    
    def get_trivial_net(self):
        net = solution.BayesianNetwork()
        a = solution.DiscreteVariable("A", ["True", "False"])
        b = solution.DiscreteVariable("B", ["True", "False"])
        net.add_node(a)
        net.add_node(b)
        net.add_edge(b,a)
        a.set_probability_table(np.array([[0.2,0.3],[0.8,0.7]]))
        b.set_probability_table(np.array([0.4,0.6]))
        return net


    def test_initialize_factors(self):
        net = self.get_trivial_net()
        factors = solution.initialize_factors(net, None)
        self.assertEqual(len(factors), len(net.nodes))

    def test_sum_product_elim_var(self):
        f1 = solution.Factor(["A","B"], {"A":["True","False"], "B": ["True","False"]}, np.array([[0.2,0.3],[0.8,0.7]]))
        f2 = solution.Factor(["B"], {"B": ["True","False"]}, np.array([0.4,0.6]))
        res = solution.sum_product_elim_var([f1,f2], "B")
        self.assertEqual(len(res), 1)
        # Using almost equal to avoid rounding/precision errors
        np.testing.assert_almost_equal(res[0].potentials, np.array([0.26, 0.74]))

    def _create_example_graph(self):
        dg = solution.Graph()
        dg.add_node("A")
        dg.add_node("B")
        dg.add_node("E")
        dg.add_node("R")
        dg.add_edge("B","A")
        dg.add_edge("E","A")
        dg.add_edge("E","R")
        return dg

    def _create_lecture_graph(self):
        graph = solution.Graph()

        graph.add_node("A")
        graph.add_node("B")
        graph.add_node("C")
        graph.add_node("D")
        graph.add_node("E")
        graph.add_node("F")
        graph.add_node("G")
        graph.add_node("H")
        graph.add_node("I")
        graph.add_node("L")
        graph.add_node("M")

        graph.add_edge("A", "C")
        graph.add_edge("C", "E")
        graph.add_edge("E", "G")
        graph.add_edge("E", "H")
        graph.add_edge("B", "D")
        graph.add_edge("D", "F")
        graph.add_edge("F", "H")
        graph.add_edge("F", "I")
        graph.add_edge("H", "L")
        graph.add_edge("I", "M")
        graph.add_edge("M", "H")

        return graph

if __name__ == "__main__":
    unittest.main()
        
