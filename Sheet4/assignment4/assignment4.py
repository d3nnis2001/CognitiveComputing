from typing import Union, Optional, List, Dict, Iterable, Tuple

from ccbase.networks import BayesianNetwork
from ccbase.nodes import DiscreteVariable
from ccbase.factor import Factor
import numpy as np
import random
import itertools




def maximize_out(factor: Factor, variable: str) -> Factor:
    """
        Takes a factor and removes the given variable from that
        factor via maximization, according to the definition in
        Darwiche: Modeling and Reasoning with Bayes:

        $(max_x f)(\mathbf{y}) = max_x f(x, \mathbf{y})$

        Parameters
        ----------
        factor: Factor
            The factor from which to remove the variable.
        variable: String
            The name of the variable to be maxmized out.

        Returns
        --------
        Factor
            A new factor that results from maximizing out the 
            variable from the initial factor.
    """
    newFactor = factor.copy()

    if variable in newFactor.variable_order:
        index = factor.variable_order.index(variable)
        newFactor.potentials = np.max(newFactor.potentials, axis=index)
        newFactor.variable_order.remove(variable)

    return newFactor


def max_product_elim_var(factors: Iterable[Factor], variable: str) -> Tuple[Iterable[Factor], Factor]:
    """
        Eliminates the given variable from the given factors via maximization.

        Parameters
        ----------
        factors: iterable of Factor
            Any iterable of factors from which the variable is to be removed
        variable: String
            The variable to be eliminated.

        Returns
        --------
        iterable of Factor
            The remaining factors that do no longer include the eliminated variable.
        Factor
            The factor combining all Factors containing the variable. This is helpful
            for traceback function.
    """ 
    raise NotImplementedError("TODO Exercise 1.2")

def traceback(factors: Dict[str, Factor], order: List[str]) -> Dict[str,str]:
    """
        Computes the optimal instantiation of all variables based on
        the given factors and elimination order.

        Parameters
        ----------
        factors: dict of ccbase.factor.Factor
            A dictionary containing variable-name:Factor pairs, where each 
            Factor is the Factor from which the variable was to be removed via
            maximization.
        order: list of String
            The order in which the variables have been eliminated.

        Returns
        -------
        dict
            A dictionary containing variable:outcome pairs representing the
            MPE.
    """
    instantiation = {}

    for i in order[::-1]:
        factor = factors[i]

        potentials = []
        for value in factor.outcomes[i]:
            instantiation[i] = value
            potentials.append(factor.potential(instantiation.copy()))

        index = np.argmax(potentials)
        instantiation[i] = factor.outcomes[i][index]

    return instantiation


def calculate_MAP(bn: BayesianNetwork, 
                evidence: Optional[Union[str, DiscreteVariable]] =None) -> Tuple[float, Dict[str,str]]:
    """
        Function calculating the most probable explanation (MPE) as well as its
        probability given potential evidence.

        Parameters
        -----------
        bn: ccbase.networks.BayesianNetwork
            The BayesianNetwork for which the MAP is to be computed.
        evidence: {Node/Nodename: Outcome}, optional
            The evidence which needs to be considered when computing the MAP.

        Returns
        --------
        float
            The probability of the MPE
        dict
            A dictionary representing the MPE as Variable:Outcome pairs for all
            variables in the network.
    """
    raise NotImplementedError("TODO Exercise 1.4")


def sample(distribution: Dict[str, float]) -> str:
    """
        Sample an outcome from a given probability distribution using the
        univariate sampling (also called roulette wheel selection) mentioned
        in the lecture.

        Parameters
        ----------
        distribution: dict
            A dictionary containing the possible outcomes as keys and their
            respective probabilities as values.

        Returns
        -------
            String
            The sampled outcome
    """
    cum = np.cumsum(list(distribution.values()))
    rand = random.random()
    index = np.searchsorted(cum, rand)
    output = list(distribution.keys())[index]
    return output


def get_ancestral_ordering(bayesnet):
    """
        Generate an ancestral ordering for nodes of the given network.

        Parameters
        ----------
        bayesnet: BayesianNetwork
            The network whose nodes are to be ordered.

        Returns
        -------
        [String/Nodes]
            A list containing the nodes (or their names) of the network in
            ancestral ordering (i.e. all parents of a node appear before that
            node in the list)
    """
    raise NotImplementedError("TODO Exercise 3.1")


def do_forward_sampling(bayesnet, var_name, num_samples=1000):
    """
        Calculate marginals using Forward Sampling without worrying about
        dealing with evidence.

        Parameters
        -----------
        bayesnet: BayesianNetwork
            The network to be sampled.
        var_name: String
            The name of the variable whose marginal is to be approximated.
        num_samples: Int (optional)
            The number of samples to be generated to estimate the marginal. Default
            1000.

        Returns
        --------
            dict
            A dictionary containing the outcome of the variable var_name
            as keys and those outcomes marginal probabilities as values.
    """
    raise NotImplementedError("TODO Exercise 3.2")


def create_initial_sample(bayesnet: BayesianNetwork, evidence: Dict[str, str]) -> Dict[str,str]:
    """
        Create an initial sample useable for Gibbs sampling for the given network that
        takes the given evidence into account.

        Parameters
        ----------
        bayesnet: ccbase.networks.BayesianNetwork
            The network in which to sample.
        evidence: Dict[str,str]
            Node-name:outcome pairs specifying the observed evidence.

        Returns
        -------
        Dict[str,str]
            A dictionary containing node-name:outcome pairs for all nodes in the
            network required for Gibbs sampling.
    """
    raise NotImplementedError("TODO Exercise 4.1")

def get_markov_distr(node, evidence):
    """
        Computes the local probability distribution for the random variable represented
        by the given node, given the provided evidence. 

        Parameters
        ----------
        node: ccbase.nodes.DiscreteVariable
            The DiscreteVariable from a BayesianNetwork for which the distribution
            is to be computed. 
        evidence: dict
            A dictionary containing node names as keys and their observed outcomes
            as values. You may assume that this dictionary contains key-value
            pairs for all nodes in the Bayesian network from which "node" came. 
        
        Returns
        -------
        Dict[str, float]
            A dictionary representation of a probability distribution with the outcomes
            of node as keys and their probabilities as values.  
    """

    raise NotImplementedError("TODO Exercise 4.2")

def do_gibbs_sampling(bayesnet, var_name, evidence, num_samples=1000, burn_in_period_length=100, thinning=1):
    """
        Calculate marginals using Gibbs Sampling.
        Hint: When computing the local probability of a variable according to 
        its MarkovBlanket, it might be useful (but not required!) to use the 
        factor class. 
        
        Parameters
        ---------
        bayesnet: BayesianNetwork
            The network from which the samples should be created.
        var_name: String
            The variable to calculate marginals for
        evidence: dict
            A dictionary containing node_name: outcome pairs to specify the
            evidence.
        num_samples: Int (optional)
            Number of samples to generate after the burn_in_period. 
            Default 1000.
        burn_in_period_length: Int (optional) 
            Number of samples that are discarded at the beginning. Default 100
        thinning: Int (optional)
            Only take every nth sample for the calculation of the marginal. 
            Default 1
         
        Return
        -------
            dict
            A dictionary containing the outcome of the variable var_name
            as keys and those outcomes marginal probabilities as values
            obtained by gibbs sampling.
    """
    raise NotImplementedError("TODO Exercise 4.3")



######
#
# Example networks
#
######

def get_wetgrass_network():
    net = BayesianNetwork()

    #Create the discrete variables that should be contained in the network
    node_winter = DiscreteVariable("winter", ["True", "False"])
    node_sprinkler = DiscreteVariable("sprinkler", ["True", "False"])
    node_rain = DiscreteVariable("rain", ["True", "False"])
    node_grass = DiscreteVariable("wet_grass", ["True", "False"])
    node_fields = DiscreteVariable("dry_fields", ["True", "False"])

    #Add the nodes to the network
    net.add_node(node_winter)
    net.add_node(node_sprinkler)
    net.add_node(node_rain)
    net.add_node(node_grass)
    net.add_node(node_fields)

    #Setup the relationships between the variables
    net.add_edge(node_winter, node_sprinkler)
    net.add_edge(node_winter, node_rain)
    net.add_edge(node_sprinkler, node_grass)
    net.add_edge(node_rain, node_grass)
    net.add_edge(node_rain, node_fields)
    
    
    # This corresponds to P(winter=True) = 0.6 and P(winter=False) = 0.4
    node_winter.set_probability_table(np.array([0.6, 0.4]))
    
    # As sprinkler has 1 parent (winter) this corresponds to:
    # P(sprinkler=True|winter=True) = 0.2
    # P(sprinkler=True|winter=False) = 0.75
    # P(sprinkler=False|winter=True) = 0.8
    # P(sprinkler=False|winter=False) = 0.25
    node_sprinkler.set_probability_table(np.array([[0.2, 0.75], 
                                                   [0.8, 0.25]]))
    
    
    # Analogue to the sprinkler node
    node_rain.set_probability_table(np.array([[0.8, 0.1], 
                                              [0.2, 0.9]]))
    
    # Analogue to the sprinkler node, just with rain as parent
    node_fields.set_probability_table(np.array([[0.01, 0.8], 
                                              [0.99, 0.2]]))
    
    # Grass has 2 parents, sprinkler and rain (in that order as specified above!)
    # Accordingly this corresponds to:
    # P(grass=True|sprinkler=True, rain=True)= 0.99
    # P(grass=True|sprinkler=True, rain=False)= 0.7
    # P(grass=True|sprinkler=False, rain=True)= 0.9
    # P(grass=True|sprinkler=False, rain=False)= 0.1
    # P(grass=False|sprinkler=True, rain=True)= 0.01
    # P(grass=False|sprinkler=True, rain=False)= 0.3
    # P(grass=False|sprinkler=False, rain=True)= 0.1
    # P(grass=False|sprinkler=False, rain=False)= 0.9
    node_grass.set_probability_table(np.array([
                                            [ #Block for wet_grass=True 
                                                [0.99, 0.7], #sprinkler=True
                                                [0.9, 0.1 ] #sprinkler = False
                                            ], 
                                            [ # Block for wet_grass=False
                                                [0.01, 0.3], #sprinkler=True
                                                [0.1, 0.9] #sprinkler=False
                                            ]]))
    
    return net



def get_simple_net():
    """
        Helper function to generate a simple BayesianNetwork with binary
        variables.
    """
    net = BayesianNetwork()

    #Create the discrete variables that should be contained in the network
    node_winter = DiscreteVariable("winter", ["True", "False"])
    node_sprinkler = DiscreteVariable("sprinkler", ["True", "False"])
    node_rain = DiscreteVariable("rain", ["True", "False"])
    node_grass = DiscreteVariable("wet_grass", ["True", "False"])
    node_road = DiscreteVariable("slippery_road", ["True", "False"])

    #Add the nodes to the network
    net.add_node(node_winter)
    net.add_node(node_sprinkler)
    net.add_node(node_rain)
    net.add_node(node_grass)
    net.add_node(node_road)

    #Setup the relationships between the variables
    net.add_edge(node_winter, node_sprinkler)
    net.add_edge(node_winter, node_rain)
    net.add_edge(node_sprinkler, node_grass)
    net.add_edge(node_rain, node_grass)
    net.add_edge(node_rain, node_road)
    
    #Setup the (conditional) probability tables.
    #Make sure that you set these tables AFTER you specify the edges, as adding
    #an edge would require changes to the cpts!
    #Also note, that currently you need ot be careful to specify the table in
    #the correct format, as mentioned in tutorial session 3!
    
    # This corresponds to P(winter=True) = 0.6 and P(winter=False) = 0.4
    node_winter.set_probability_table(np.array([0.6, 0.4]))
    
    # As sprinkler has 1 parent (winter) this corresponds to:
    # P(sprinkler=True|winter=True) = 0.2
    # P(sprinkler=True|winter=False) = 0.75
    # P(sprinkler=False|winter=True) = 0.8
    # P(sprinkler=False|winter=False) = 0.25
    
    node_sprinkler.set_probability_table(np.array([[0.2, 0.75], 
                                                   [0.8, 0.25]]))
    
    # Analogue to the sprinkler node
    node_rain.set_probability_table(np.array([[0.8, 0.1], 
                                              [0.2, 0.9]]))
    
    # Analogue to the sprinkler node, just with rain as parent
    node_road.set_probability_table(np.array([[0.7, 0.0], 
                                              [0.3, 1.0]]))
    
    # Grass has 2 parents, sprinkler and rain (in that order as specified above!)
    # Accordingly this corresponds to:
    # P(grass=True|sprinkler=True, rain=True)= 0.95
    # P(grass=True|sprinkler=True, rain=False)= 0.1
    # P(grass=True|sprinkler=False, rain=True)= 0.8
    # P(grass=True|sprinkler=False, rain=False)= 0.0
    # P(grass=False|sprinkler=True, rain=True)= 0.05
    # P(grass=False|sprinkler=True, rain=False)= 0.9
    # P(grass=False|sprinkler=False, rain=True)= 0.2
    # P(grass=False|sprinkler=False, rain=False)= 1.0
    node_grass.set_probability_table(np.array([
                                            [ #Block for grass=True 
                                                [0.95, 0.1], #sprinkler=True
                                                [0.8, 0.0 ] #sprinkler = False
                                            ], 
                                            [ # Block for grass=False
                                                [0.05, 0.9], #sprinkler=True
                                                [0.2, 1.0] #sprinkler=False
                                            ]]))
    
    
    
    
    return net

def get_non_binary_net():
    """
        Helper function to generate a simple BayesianNetwork with
        non-binary variables.
    """
    net = BayesianNetwork()
    
    node_john = DiscreteVariable("john", ["Calling", "Not_calling"])
    node_burglary = DiscreteVariable("burglary", ["Intruder", "Safe"])
    node_alarm = DiscreteVariable("alarm", ["Ringing", "Silent", "Broken"])
    
    net.add_node(node_john)
    net.add_node(node_burglary)
    net.add_node(node_alarm)
    
    net.add_edge(node_alarm, node_john)
    net.add_edge(node_burglary, node_john)
    
    node_burglary.set_probability_table(np.array([0.4,0.6]))
    node_alarm.set_probability_table(np.array([0.2,0.3,0.5]))
    node_john.set_probability_table(np.array([
                                                [
                                                    [0.8, 0.6], #alarm=ringing
                                                    [0.7, 0.1], #alarm=silent
                                                    [0.5, 0.2] #alarm=broken
                                                ],
                                                [
                                                    [0.2, 0.4],
                                                    [0.3, 0.9],
                                                    [0.5, 0.8]
                                                ]]))
    
    return net

if __name__ == "__main__":
    print("please run example_tests.py to check your functions")
