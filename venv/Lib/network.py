from collections import OrderedDict

from neuron import Neuron
from synapse import Synapse

import networkx as nx

import math
import random


import matplotlib.pyplot as plt

class Network(object):

    def __init__(self):
        self.neurons = OrderedDict()
        self.synapses = set()

    def addNeuron(self, neuron):
        self.neurons[neuron.neuron_id] = neuron

    def get_synapses(self):
        #TODO: should be improved, wastes CPU
        for neuron in self.neurons.values():
            for synapse in neuron.presynaptic_connections:
                if synapse not in self.synapses:
                    self.synapses.add(synapse)
        return self.synapses

    def get_num_of_neurons(self):
        return len(self.neurons)

    def get_network_state(self):
        pas

    def draw(self):
        #https://networkx.github.io/documentation/networkx-1.9/examples/drawing/labels_and_colors.html

        #https://stackoverflow.com/questions/28910766/python-networkx-set-node-color-automatically-based-on-number-of-attribute-opt  2
        G_1 = nx.Graph()
        tempedgelist = [(s.pre_id, s.post_id) for s in self.get_synapses()]
        weightlist = [s.weight for s in self.get_synapses()]
        G_1.add_edges_from(tempedgelist)

        n_nodes = self.get_num_of_neurons()
        pos = {i: (math.cos(i * 2* math.pi / (self.get_num_of_neurons() - 1)), math.sin(i * 2* math.pi / (self.get_num_of_neurons() - 1))) for i in range(n_nodes)}

        #for node in
        nx.draw_networkx_nodes(G_1, pos, edge_labels=True)
        nx.draw_networkx_edges(G_1, pos)
        plt.show()
        print("problem")

class NetworkFactory(object):
    @staticmethod
    def makeNetwork():
        return Network()
    @staticmethod
    def makeNeuron():
        return Neuron()
    @staticmethod
    def makeSynapse(pre_id, post_id):
        return Synapse(pre_id, post_id)