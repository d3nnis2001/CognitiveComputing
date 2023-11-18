"""
Last modified on Tue Nov 3 2023
@author: hvoss
"""

# Import of the provided graph class. You would
# need to change this line if you plan to use your
# own graph class!

# If you change this, make sure you also import you Graph
# with that name, e.g. if you want to use the assignment1.py file
# directly your import could look like:
# from assignment1.py import DGraph as Graph
# Also make sure to submit your assignment1.py (or whatever you end up)
# calling it, alongside this file so that the imports work!
from ccbase.networks import Graph
from ccbase.nodes import Node
###
# You should not really require numpy for this assignment, but you are free
# to use it if you want.
import numpy as np
# Imports for type hints
from typing import Union, List, Iterable

###
# Note: If you use your own graph implementation, take care
# that the parameters may be either a node's name or a node's
# object. You do however not need to worry about implementing both
# return types. It will be enough as long as the functions return either
# node objects or the node names (or lists thereof). Similarly, when implementing
# the functions below, it is sufficient if your solutions work with either names
# or node objects.


## Exercise 3: Finding basic (causal) structures

def find_forks(dg: Graph) -> List[Union[Node, str]]:
    """
        Finds all forks within the given directed graph.
        
        Parameters
        ----------
        dg: ccbase.networks.Graph
            The (directed) graph whose forks are to be found.
            You can assume that the graph will be directed.
            
        Returns
        ----------
        list of ccbase.nodes.Node or Strings
            A list containing all Nodes (either object or their name/id) that
            represent forks in the network.
    """
    """# alternative:
    forks = []
    for node in dg.nodes:
        if len(dg.get_children(node)) > 1:
            forks.append(node)
    
    return forks
    """
    return [node for node in dg.nodes if len(dg.get_children(node)) > 1]

def find_chains(dg: Graph) -> List[Union[Node, str]]:
    """
        Finds all chains within the given directed graph.
        
        Parameters
        ----------
        dg: ccbase.networks.Graph
            The (directed) graph whose chains are to be found.
            You can assume that the graph will be directed.
            
        Returns
        ----------
        list of ccbase.nodes.Node or Strings
            A list containing all Nodes (either object or their name/id) that
            represent chains in the network.
    """
    """# alternative:
    chains = []
    for node in dg.nodes:
        parents = dg.get_parents(node)
        children = dg.get_children(node)
        
        if parents and children:
            chains.append(node)
            
    return chains
    """
    return [node for node in dg.nodes
            if dg.get_parents(node) and dg.get_children(node)]

def find_collider(dg: Graph) -> List[Union[Node, str]]:
    """
        Finds all colliders within the given graph.
        
        Parameters
        ----------
        dg: ccbase.networks.Graph
            The (directed) graph whose colliders are to be found.
            You can assume that the graph will be directed.
            
        Returns
        ----------
        list of ccbase.nodes.Node or Strings
            A list containing all Nodes (either object or their name/id) that
            represent collider in the network.
    """
    """# alternative:
    collider = []
    
    for node in dg.nodes:
        if len(dg.get_parents(node)) > 1:
            collider.append(node)
    
    return collider
    """
    return [node for node in dg.nodes if len(dg.get_parents(node)) > 1]


### Exercise 4: Markov Equality

def find_immoralities(graph: Graph) -> List:
    """
        A function to return all immoralities (i.e. two nodes with the same 
        child but no direct connection) of the given directed graph.

        Parameter
        ---------
        graph: ccbase.networks.Graph or equivalent
            The directed graph to check for immoralities

        Returns
        -------
        list
            A list of all immoralities contained in the graph. How you
            represent a single immorality is up to you.
    """
    immoralities = []
    for node in graph.nodes:
        parents = graph.get_parents(node)
        while parents:
            current_parent = parents.pop()
            for parent in parents:
                if current_parent not in parent.children and  current_parent not in parent.parents:
                    immoralities.append((current_parent, parent))

    return immoralities


def same_skeleton(graph1: Graph, graph2: Graph) -> bool:
    """
        A function to check whether or not the two given directed graphs have the
        same skeleton

        Parameters
        ----------
        graph1: ccbase.networks.Graph or equivalent
            The first directed graph to test.
        graph2: ccbase.networks.Graph or equivalent
            The second directed graph to test against the first.

        Returns
        -------
        bool
            True if the two graphs have the same skeletons, False otherwise.
    """
    undirected_graph1 = graph1.to_undirected()
    undirected_graph2 = graph2.to_undirected()
    if set(undirected_graph1.nodes) != set(undirected_graph2.nodes):
        return False
    for node in undirected_graph1.nodes:
        if node not in undirected_graph2.nodes:
            return False
        else:
            parents1 = undirected_graph1.get_parents(node)
            parents2 = undirected_graph2.get_parents(node)
            if not parents1 == parents2:
                return False
            children1 = undirected_graph1.get_children(node)
            children2 = undirected_graph2.get_children(node)
            if not children1 == children2:
                return False
    return True

def markov_equivalent(graph1: Graph, graph2: Graph) -> bool:
    """
        A function to check whether or not the two given directed graphs are Markov
        equivalent.

        Parameters
        ----------
        graph1: ccbase.networks.Graph or equivalent
            The first directed graph to test.
        graph2: ccbase.networks.Graph or equivalent
            The second directed graph to test against the first.

        Returns
        -------
        bool
            True if the two graphs are Markov equivalent, False otherwise.
    """
    return same_skeleton(graph1, graph2) and (find_immoralities(graph1) == find_immoralities(graph2))

## Exercise 5: Paths

def get_paths(graph: Graph, node_x: Union[Node, str], 
                    node_y: Union[Node, str]) -> List[List[Union[Node, str]]]:
    """
        Computes all undirected paths between node_x and node_y within
        the (directed or undirected) graph.

        Parameters
        ----------
        graph: ccbase.networks.Graph
            The graph in which to compute the paths. This may be directed or
            undirected.
        node_x: ccbase.nodes.Node or String
            The node object or name for the first of the two nodes.
        node_y: ccbase.nodes.Node or String
            The node object or name for the second of the two nodes.

        Returns
        --------
        list of lists of ccbase.nodes.Node or Strings
            A list of lists of node objects (or node names) that each represent
            an undirected path from node_x to node_y. These paths should contain
            the starting and end nodes as well.
    """
    graph = graph.to_undirected()
    current_path = [node_x]
    found_paths = []
    for child in graph.get_children(node_x):
        if child == node_y:
            found_paths.append(current_path + [node_y]) 
        else:
            found_paths = get_paths_rec(graph, child, node_y, found_paths, current_path)
    return found_paths


def get_paths_rec(graph: Graph, node_x: Union[Node, str], 
                    node_y: Union[Node, str], found_paths: List[List[Union[Node, str]]], current_path: List[Union[Node, str]]) -> List[List[Union[Node, str]]]:
    current_path.append(node_x)
    for child in graph.get_children(node_x):
        if child == node_y:
            found_paths.append(current_path + [node_y]) 
        elif child not in current_path:
            found_paths = get_paths_rec(graph, child, node_y, found_paths, current_path)
    return found_paths

    



def create_example_graphs():
    """
        A method to create a trivial example graph from the 
        lecture. Feel free to create your own methods that generate
        graphs on which you want to test your implementations!

        Returns
        --------
        ccbase.networks.Graph
            A directed graph containing the four nodes A,B,E and R.
    """
    dg = Graph()
    dg.add_node("A")
    dg.add_node("B")
    dg.add_node("E")
    dg.add_node("R")
    dg.add_edge("B","A")
    dg.add_edge("E","A")
    dg.add_edge("E","R")

    dg2 = dg.copy()
    dg2.remove_edge("E","R")
    dg2.add_edge("R","E")
    return dg, dg2


if __name__ == "__main__":
    # Example calls
    g1, g2 = create_example_graphs()
    forks = find_forks(g1)
    print("The graph contains the following forks: {}".format(forks))
    assert set(forks) == set(["E"])
    chains = find_chains(g1)
    print("The graph contains the following chains: {}".format(chains))
    assert set(chains) == set([])
    colliders = find_collider(g1)
    print("The graph contains the following colliders: {}".format(colliders))
    assert set(colliders) == set(["A"])
    
    #Markov Equality Since you determine how to represent immoralities
    # I cannot provide any asserts here.
    print("Immoralities for graph 1: ", find_immoralities(g1))
    print("Do g1 and g2 have the same skeleton? ", same_skeleton(g1, g2))
    print("Are g1 and g2 Markov Equivalent? ", markov_equivalent(g1, g2))

    # Graphical independence tests
    # Hint: You may want to test these methods with a more complex graph!
    paths = get_paths(g1, "B", "R")
    print("Undirected paths from B to R in the graph: {}".format(paths))