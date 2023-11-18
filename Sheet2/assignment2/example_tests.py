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
import assignment2 as solution

class TestAssignment3(unittest.TestCase):


    def test_find_forks(self):
        graph = self._create_example_graph()
        forks = solution.find_forks(graph)
        # Ensure we allow both string and node returns
        try:
            forks = [n.name for n in forks]
        except AttributeError:
            pass 
        self.assertEqual(set(forks), {"E"}, "Incorrect forks found.")

    def test_find_chains(self):
        graph = self._create_example_graph()
        chains = solution.find_chains(graph)
        # Ensure we allow both string and node returns
        try:
            chains = [n.name for n in chains]
        except AttributeError:
            pass 
        self.assertEqual(set(chains), set([]), "The graph does not have chains.")

    def test_find_collider(self):
        graph = self._create_example_graph()
        collider = solution.find_collider(graph)
        # Ensure we allow both string and node returns
        try:
            collider = [n.name for n in collider]
        except AttributeError:
            pass 
        self.assertEqual(set(collider), {"A"}, "Incorrect collider found.")


    def test_find_immoralities(self):
        graph1 = self._create_example_graph()
        graph2 = graph1.copy()
        graph2.remove_edge("E","R")
        graph2.add_edge("R","E")
        print("Immoralities of graph1: ", solution.find_immoralities(graph1))
        print("Immoralities of graph2: ", solution.find_immoralities(graph2))
        # You would need to define your own test here since the return
        # type is up to you!
        

    def test_same_skeleton(self):
        graph1 = self._create_example_graph()
        graph2 = graph1.copy()
        graph2.remove_edge("E","R")
        graph2.add_edge("R","E")
        self.assertTrue(solution.same_skeleton(graph1, graph2), "The graphs have the same skeletons")


    def test_markov_equivalent(self):
        graph1 = self._create_example_graph()
        graph2 = graph1.copy()
        graph2.remove_edge("E","R")
        graph2.add_edge("R","E")
        self.assertTrue(solution.markov_equivalent(graph1, graph2), "Graphs are ME")

    def test_get_paths(self):
        graph = self._create_example_graph()
        paths = solution.get_paths(graph, "A", "R")
        true_paths = [["A","E","R"]]
        for p in true_paths:
            self.assertIn(p, paths)

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

if __name__ == "__main__":
    unittest.main()
        
