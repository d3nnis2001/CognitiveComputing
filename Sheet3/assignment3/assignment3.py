"""
Last modified on Wed Nov 13 2023
@author: hvoss
"""

# Import of the provided graph class. You would
# need to change this line if you plan to use your
# own graph class!
from ccbase.networks import Graph
from ccbase.nodes import Node
from ccbase.networks import BayesianNetwork
from ccbase.nodes import DiscreteVariable
from ccbase.factor import Factor

from typing import Union, Optional, List, Dict, Iterable, Tuple


###
# Note: If you use your own graph implementation, take care
# that the parameters may be either a node's name or a node's
# object. You do however not need to worry about implementing both
# return types. It will be enough as long as the functions return either
# node objects or the node names (or lists thereof).
###


def is_collider(dg, node, path):
    """
        Checks whether or not the given node is a collider with respect to the given
        path.

        Parameters
        ----------
        dg: Graph
            The graph that contains at least all the nodes of the given path 
            and their connections.
        node: Node or String
            The node object (or its name) of a node that should be present in the 
            given path, which is to be checked.
        path: [Node or String,]
            A list of node objects (or node names) that represents
            an undirected path that contains the given node.

        Returns
        ----------
        bool
            True if the given node is a collider with respect to the given path
            within the graph, False otherwise.
    """
    if len(path) < 3:
        return False

    index = path.index(node)
    if index == 0 or index == len(path) - 1:
        return False

    prev_node = path[index - 1]
    next_node = path[index + 1]

    ancestors = dg.get_ancestors(path[index])
    if prev_node in ancestors and next_node in ancestors:
        print("The node is a collider")
        return True
    return False

    

def is_path_open(dg, path, nodes_z):
    """ 
        Checks whether or not the given path is open conditioned on the given nodes.

        Parameters
        ---------
        dg: Graph
            The graph that should contain all the nodes and their connections.
        path: [Node or String,]
            A list of node objects (or node names) that represents
            an undirected path between the first and last node of the path within 
            the graph.
        nodes_z: iterable of Node/Strings
            The set of conditioned nodes, that might influence the paths 
            between node_x and node_y
        
        Returns
        --------
        bool
            False if the path is blocked given given the nodes_z, True otherwise.
        
    """
    pass


def unblocked_path_exists(dg, node_x, node_y, nodes_z):
    """
        Computes if there is at least one unblocked undirected path
        between node_x and node_y when considering the nodes in nodes_z.
        
        Parameters
        ---------
        dg: Graph
            The graph that should contain all the nodes.
        nodes_x: Node/String
            The first of the two nodes whose paths are to be checked.
        nodes_y: Node/String
            The second of the two nodes whose paths are to be checked.
        nodes_z: iterable of Node/Strings
            The set of conditioned nodes, that might influence the paths 
            between node_x and node_y
            
        Returns
        --------
        bool
            False if all undirected paths between node_x and node_y are blocked 
            given the nodes_z, True otherwise.
    """
    visited = set()
    def blocked(currentnode):
        if currentnode == node_y:
            return False

        visited.add(currentnode)

        for child in dg.get_children(currentnode):
            if child not in visited and child not in nodes_z:
                if not blocked(child):
                    return False
                
        for parent_node in dg.get_parents(currentnode):
            if parent_node not in visited and parent_node not in nodes_z:
                if not blocked(parent_node):
                    return False
        return True
    return not blocked(node_x)


def check_independence(dg, nodes_x, nodes_y, nodes_z):
    """
        Computes whether or not nodes in nodes_x are conditionally 
        independend of nodes in nodes_y given nodes in nodes_z.
        
        Parameters
        ---------
        dg: Graph
            The graph that should contain all the nodes.
        nodes_x: iterable of Node or String
            The nodes that should be conditionally independent of the nodes
            in nodes_y
        nodes_y: iterable of Node or String
            The nodes that should be conditionally independent of the nodes
            in nodes_x                
        nodes_z: iterable of Node or String
            The set of nodes that should make nodes_x and nodes_y conditionally
            independent.
            
        Returns
        ----------
        bool
            True if all nodes in nodes_x are conditionally independent of all
            nodes in nodes_y given the nodes in nodes_z, False otherwise.
    """
    def is_d_separated(dg, nodes_x, nodes_y, nodes_z):
        pass

    for node_x in nodes_x:
        for node_y in nodes_y:
            # Check if node_x and node_y are conditionally independent given nodes_z
            if not is_d_separated(dg, node_x, node_y, nodes_z):
                return False
    return True

# Function to get all children of node as a list

def make_ancestral_graph(graph: Graph, nodes: Iterable[Union[Node, str]]) -> Graph:
    """
        Computes the ancestral graph of the given graph for the given set of nodes.

        Parameters
        ----------
        graph: ccbase.networks.Graph
            The (directed) graph from which to compute the ancestral graph.
        nodes: Iterable of ccbase.nodes.Node or String
            The set of nodes for which to compute the ancestral graph.

        Returns
        -------
        ccbase.networks.Graph
            The resulting ancestral graph.
    """

    ancestralGraph = graph.copy()
    nodesToRemove = []

    for node in ancestralGraph.nodes:
        #check if node and his children are not in nodes
        if not node in nodes and not any(ancestralGraph.is_ancestor(node, node2) for node2 in nodes):
            nodesToRemove.append(node)

    for node in nodesToRemove:
        ancestralGraph.remove_node(node)

    return ancestralGraph

def make_moral_graph(graph: Graph) -> Graph:
    """
        Computes the moral graph of the given graph, i.e., an
        undirected copy of the given graph with all immoralities removed.

        Parameters
        ----------
        graph: ccbase.networks.Graph
            The (directed) graph from which to compute the moral graph.

        Returns
        -------
        ccbase.networks.Graph
            The resulting moral graph which is undirected.
    """

    # Function from Ex2
    def find_immoralities(graph: Graph, immoralities):
        for node in graph.nodes.values():
            parents = list(graph.get_parents(node))
            while parents:
                current_parent = parents.pop()
                for parent in parents:
                    if current_parent not in parent.children and current_parent not in parent.parents:
                        immoralities.append((current_parent, parent))

    moralGraph = graph.copy()
    immoralities = []
    find_immoralities(graph, immoralities)

    for immorality in immoralities:
        moralGraph.add_edge(immorality[0], immorality[1])

    moralGraph = moralGraph.to_undirected()
    return moralGraph

def separation(graph: Graph, nodes_z: Iterable[Union[Node, str]]) -> Graph:
    """
        Separates the given nodes from the graph.

        Parameters
        ----------
        graph: ccbase.networks.Graph
            The (directed) graph from which to separate the given nodes.
        nodes_z: Iterable of ccbase.nodes.Node or String
            The set of nodes to separate.

        Returns
        -------
        ccbase.networks.Graph
            The resulting graph with all links from the nodes in node_z
            removed.
    """
    separatedGraph = graph.copy()

    for node in nodes_z:
        separatedGraph.remove_node(node)

    return separatedGraph


def check_independence_general(graph: Graph, nodes_x: Iterable[Union[Node, str]],
                               nodes_y: Iterable[Union[Node, str]], nodes_z: Iterable[Union[Node, str]]) -> bool:
    """
        Computes whether or not nodes in nodes_x are conditionally 
        independend of nodes in nodes_y given nodes in nodes_z
        using the general graphical test.
        
        Parameters
        ---------
        dg: ccbase.networks.Graph
            The directed or undirected graph that should contain all the nodes.
        nodes_x: iterable of ccbase.nodes.Node or String
            The nodes that should be conditionally independent of the nodes
            in nodes_y
        nodes_y: iterable of ccbase.nodes.Node or String
            The nodes that should be conditionally independent of the nodes
            in nodes_x                
        nodes_z: iterable of ccbase.nodes.Node or String
            The set of nodes that should make nodes_x and nodes_y conditionally
            independent.
            
        Returns
        ----------
        bool
            True if all nodes in nodes_x are conditionally independent of all
            nodes in nodes_y given the nodes in nodes_z, False otherwise.
    """

    undirectedGraph = graph.to_undirected()
    nodes = set(nodes_x) | set(nodes_y) | set(nodes_z)

    ancestralGraph = make_ancestral_graph(undirectedGraph, nodes)
    moralGraph = make_moral_graph(ancestralGraph)
    separatedGraph = separation(moralGraph, nodes_z)

    for nodeX in nodes_x:
        for nodeY in nodes_y:
            if separatedGraph.is_ancestor(nodeX, nodeY):
                return False

            for node in separatedGraph.nodes:
                if separatedGraph.is_ancestor(node, nodeX) and separatedGraph.is_ancestor(node, nodeY):
                    return False

    return True
    

def get_elimination_ordering(bn: BayesianNetwork) -> List[str]:
    """
        Computes an elimination order of all the variables in the network
        according to the MinFillOrder heuristic.

        Parameters
        ---------
        bn: BayesianNetwork
            The BayesianNetwork for which the elimination order is to be
            computed.
        
        Returns
        -------
        [str]
            A list containing the names of all the nodes in the network
            bn, in an order following a suitable heuristic.
            
        Remark:
            Exercise 1 Task 2 does not require you to write code, instead
            you should describe another heuristic and explain how it works
            and what the differences are with respect to the MinFillOrder.
    """
    elimination_ordering = []
    undirected = bn.to_undirected()
    
    # Continue until all nodes are eliminated
    while undirected.nodes:
        fills = []
        
        # Calculate the fill-in sets for each node
        for node in undirected.nodes:
            fill_of_node = []
            neighbors = undirected.get_children(node)

            # Check for missing edges between neighbors
            for cur_neighbor in neighbors:
                for neighbor_to_check in neighbors:
                    if neighbor_to_check != cur_neighbor and neighbor_to_check not in undirected.get_children(cur_neighbor):
                        fill_of_node.append((cur_neighbor, neighbor_to_check))
                
            fills.append((node, fill_of_node))
        
        #print(fills)
        #print(min(fills, key=lambda x: len(x[1])))
        
        # Choose the variable for elimination based on the minimum fill-in set size
        elimination_node, new_edges = min(fills, key=lambda x: len(x[1]))
        
        # Add edges between neighbors with no edges and delete the chosen elimination node
        for edge in new_edges:
            undirected.add_edge(*edge)
        undirected.remove_node(elimination_node)
        elimination_ordering.append(elimination_node)

    return elimination_ordering
        


def initialize_factors(bn: BayesianNetwork, evidence: Optional[Dict[str, str]] = None) -> Iterable[Factor]:
    """
        Creates and returns a factor for every node in the Bayesian network initialized according
        to the node's CPTs while taking the given evidence into account.

        Parameters
        ---------
        bn: BayesianNetwork
            The BayesianNetwork for which the elimination order is to be 
            computed.
        evidence: Dict[str, str], optional
            A dictionary containing the evidence variables as keys and their
            observed outcomes as values. 

        Returns
        -------
            Iterable[Factor]
            An iterable (e.g. a list or a set) containing a factor for every 
            node in the BayesianNetwork, properly initialized.
    """
    pass


def sum_product_elim_var(factors: Iterable[Factor], variable: str) -> Iterable[Factor]:
    """
        Eliminates the given variable from the given factors via marginalization.

        Parameters
        ----------
        factors: iterable of ccbase.factor.Factor
            Any iterable of factors from which the variable is to be removed
        variable: String
            The variable to be eliminated.

        Returns
        --------
        iterable of ccbase.factor.Factor
            The remaining factors that do no longer include the eliminated variable.
    """


    raise NotImplementedError("TODO Exercise 4.2")


def calculate_probabilities(bn: BayesianNetwork,
                        variables: Union[str, DiscreteVariable], 
                        evidence: Optional[Dict[str,str]] = None) -> Factor:
    """
        Calculates P(variables|evidence) for all outcome combinations of
        variables  (i.e. you should return a table similar to a cpt, 
        only representing a joint distribution in this case.)
        
        Example: Calling calculate_marginals(["rain", "winter"], 
                                                {"sprinkler":"True"})
        should return a Factor representing P(rain,winter|sprinkler=True). 
        
        Parameters
        ----------
        bn: BayesianNetwork
            The BayesianNetwork for which the elimination order is to be 
            computed.
        variables: [str, Node]
            List containing the nodes, or their names of the variables of 
            interest.
            (Hint: Your code can/should assume, that a name is passed and
            simply retrieve the node manually, so that you do not have
            to differentiate these two cases.)
        evidence: Dict[str, str], optional
            A dictionary containing the evidence variables as keys and their
            observed outcomes as values. If evidence is not given, the prior
            marginals should be computed.
            
        Returns
        -------
        ccbase.factor.Factor
            A Factor over the specified variables, specifying the joint (posterior) probability
            of these variables.
    """

    raise NotImplementedError("TODO Exercise 4.3")


if __name__ == "__main__":
    print("please run example_tests.py to check your functions")
    graph = Graph()

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

    print("test for elimination ordering on graph from example_test")
    print(get_elimination_ordering(graph))

