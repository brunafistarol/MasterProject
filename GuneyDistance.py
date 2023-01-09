import numpy as np
import networkx as nx
import random
import seaborn as sns

class GuneyDistance(object):
    
    def __init__(self, graph):
        """
        graph : networkx graph
        """
        self.graph = graph
        
    # taken from https://github.com/emreg00/toolbox/blob/3d707221092937ed45f13409f8cee38b8dc0316e/wrappers.py#L536
    def calculate_proximity(self, 
                            nodes_from,
                            nodes_to,
                            nodes_from_random=None,
                            nodes_to_random=None,
                            bins=None,
                            n_random=1000,
                            min_bin_size=100,
                            seed=452456,
                            lengths=None):
        """
        Calculate proximity from nodes_from to nodes_to
        If degree binning or random nodes are not given, they are generated
        lengths: precalculated shortest path length dictionary
        """
        #distance = "closest"
        #lengths = network_utilities.get_shortest_path_lengths(network, "../data/toy.sif.pcl")
        #d = network_utilities.get_separation(network, lengths, nodes_from, nodes_to, distance, parameters = {})
        nodes_network = set(self.graph.nodes())
        nodes_from = set(nodes_from) & nodes_network 
        nodes_to = set(nodes_to) & nodes_network
        if len(nodes_from) == 0 or len(nodes_to) == 0:
            return None, None, (None, None) # At least one of the node group not in network
        d = self.calculate_closest_distance(nodes_from, nodes_to, lengths)
        if bins is None and (nodes_from_random is None or nodes_to_random is None):
            bins = self.get_degree_binning(min_bin_size, lengths) # if lengths is given, it will only use those nodes
        if nodes_from_random is None:
            nodes_from_random = self.get_random_nodes(nodes_from, bins = bins, n_random = n_random, min_bin_size = min_bin_size, seed = seed)
        if nodes_to_random is None:
            nodes_to_random = self.get_random_nodes(nodes_to, bins = bins, n_random = n_random, min_bin_size = min_bin_size, seed = seed)
        random_values_list = zip(nodes_from_random, nodes_to_random)
        values = np.empty(len(nodes_from_random)) #n_random
        for i, values_random in enumerate(random_values_list):
            nodes_from, nodes_to = values_random
            #values[i] = network_utilities.get_separation(network, lengths, nodes_from, nodes_to, distance, parameters = {})
            values[i] = self.calculate_closest_distance(nodes_from, nodes_to, lengths)
        #pval = float(sum(values <= d)) / len(values) # needs high number of n_random
        m, s = np.mean(values), np.std(values)
        if s == 0:
            z = 0.0
        else:
            z = (d - m) / s
        return d, z, (m, s) #(z, pval)
    
    # taken from https://github.com/emreg00/toolbox/blob/3d707221092937ed45f13409f8cee38b8dc0316e/wrappers.py#L602
    def calculate_closest_distance(self, nodes_from, nodes_to, lengths=None):
        values_outer = []
        if lengths is None:
            for node_from in nodes_from:
                values = []
                for node_to in nodes_to:
                    try:
                        val = nx.shortest_path_length(self.graph, node_from, node_to)
                        values.append(val)
                    except nx.exception.NetworkXNoPath:
                        pass
                if len(values) > 0:
                    d = np.min(values)
                    #print d,
                    values_outer.append(d)
        else:
            for node_from in nodes_from:
                values = []
                vals = lengths[node_from]
                for node_to in nodes_to:
                    val = vals[node_to]
                    values.append(val)
                d = np.min(values)
                values_outer.append(d)
        if len(values_outer) > 0:
            d = np.mean(values_outer)
        else:
            d = len(self.graph.nodes())
        #print d
        return d
    
    # taken from https://github.com/emreg00/toolbox/blob/3d707221092937ed45f13409f8cee38b8dc0316e/network_utilities.py#L999
    def get_degree_binning(self, bin_size, lengths=None):
        degree_to_nodes = {}
        for node, degree in self.graph.degree(): #.iteritems(): # iterator in networkx 2.0
            if lengths is not None and node not in lengths:
                continue
            degree_to_nodes.setdefault(degree, []).append(node)
        values = degree_to_nodes.keys()
        values = sorted(values)
        bins = []
        i = 0
        while i < len(values):
            low = values[i]
            val = degree_to_nodes[values[i]]
            while len(val) < bin_size:
                i += 1
                if i == len(values):
                    break
                val.extend(degree_to_nodes[values[i]])
            if i == len(values):
                i -= 1
            high = values[i]
            i += 1 
            #print i, low, high, len(val) 
            if len(val) < bin_size:
                low_, high_, val_ = bins[-1]
                bins[-1] = (low_, high, val_ + val)
            else:
                bins.append((low, high, val))
        return bins
    
    # taken from https://github.com/emreg00/toolbox/blob/3d707221092937ed45f13409f8cee38b8dc0316e/wrappers.py#L627
    def get_random_nodes(self, nodes, bins=None, n_random=1000, min_bin_size=100, degree_aware=True, seed=None):
        if bins is None:
            # Get degree bins of the network
            bins = self.get_degree_binning(min_bin_size) 
        nodes_random = self.pick_random_nodes_matching_selected(bins, nodes, n_random, degree_aware, seed=seed) 
        return nodes_random

    # taken from https://github.com/emreg00/toolbox/blob/3d707221092937ed45f13409f8cee38b8dc0316e/network_utilities.py#L1043
    def pick_random_nodes_matching_selected(self, bins, nodes_selected, n_random, degree_aware=True, connected=False, seed=None):
        """
        Use get_degree_binning to get bins
        """
        if seed is not None:
            random.seed(seed)
        values = []
        nodes = self.graph.nodes()
        for i in range(n_random):
            if degree_aware:
                if connected:
                    raise ValueError("Not implemented!")
                nodes_random = set()
                node_to_equivalent_nodes = self.get_degree_equivalents(nodes_selected, bins)
                for node, equivalent_nodes in node_to_equivalent_nodes.items():
                    #nodes_random.append(random.choice(equivalent_nodes))
                    chosen = random.choice(equivalent_nodes)
                    for k in range(20): # Try to find a distinct node (at most 20 times)
                        if chosen in nodes_random:
                            chosen = random.choice(equivalent_nodes)
                    nodes_random.add(chosen)
                nodes_random = list(nodes_random)
            else:
                if connected:
                    nodes_random = [ random.choice(nodes) ]
                    k = 1
                    while True:
                        if k == len(nodes_selected):
                            break
                        node_random = random.choice(nodes_random)
                        node_selected = random.choice(self.graph.neighbors(node_random))
                        if node_selected in nodes_random:
                            continue
                        nodes_random.append(node_selected)
                        k += 1
                else:
                    nodes_random = random.sample(nodes, len(nodes_selected))
            values.append(nodes_random)
        return values
    
    # taken from https://github.com/emreg00/toolbox/blob/3d707221092937ed45f13409f8cee38b8dc0316e/network_utilities.py#L1030
    def get_degree_equivalents(self, seeds, bins):
        seed_to_nodes = {}
        for seed in seeds:
            d = self.graph.degree(seed)
            for l, h, nodes in bins:
                if l <= d and h >= d:
                    mod_nodes = list(nodes)
                    mod_nodes.remove(seed)
                    seed_to_nodes[seed] = mod_nodes
                    break
        return seed_to_nodes
    
    