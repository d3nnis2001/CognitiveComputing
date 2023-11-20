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

    raise NotImplementedError("TODO Exercise 1.1")


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
    raise NotImplementedError("TODO Exercise 1.2")


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
    raise NotImplementedError("TODO Exercise 1.3")


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
    raise NotImplementedError("TODO Exercise 1.4")


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
    raise NotImplementedError("TODO Exercise 2.1")


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
    raise NotImplementedError("TODO Exercise 2.2")


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
    raise NotImplementedError("TODO Exercise 2.3")


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
    raise NotImplementedError("TODO Exercise 2.4")
    

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
    
    raise NotImplementedError("TODO Exercise 3.1")


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
    raise NotImplementedError("TODO Exercise 4.1")


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
