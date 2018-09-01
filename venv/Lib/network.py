from collections import OrderedDict

from neuron import Neuron
from synapse import Synapse

import networkx as nx

import math


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
                print("{} - {}".format(synapse.pre_id, synapse.post_id))
                if synapse not in self.synapses:
                    self.synapses.add(synapse)
        return self.synapses

    def get_num_of_neurons(self):
        return len(self.neurons)


    draw_counter = -1
    def draw(self):

        print("counter: %s"%Network.draw_counter)
        Network.draw_counter += 1

        #https://networkx.github.io/documentation/networkx-1.9/examples/drawing/labels_and_colors.html

        #https://stackoverflow.com/questions/28910766/python-networkx-set-node-color-automatically-based-on-number-of-attribute-opt  2
        graph = nx.Graph()
        tempedgelist = [(s.pre_id, s.post_id) for s in self.get_synapses()]
        weightlist = [s.weight for s in self.get_synapses()]



        graph.add_edges_from(tempedgelist)

        n_nodes = self.get_num_of_neurons()
        pos = {i: (math.cos(i * 2* math.pi / (self.get_num_of_neurons())), math.sin(i * 2* math.pi / (self.get_num_of_neurons()))) for i in range(n_nodes)}
        pos_right = {key : (value[0]+max(pos.values())[0] * 0.1, value[1]+max(pos.values())[0] *(Network.draw_counter / 20)) for key, value in pos.items()}

        #for node in
        nx.draw_networkx_nodes(graph, pos, edge_labels=True)
        nx.draw_networkx_edges(graph, pos)

        neuron_ids = {i:i for i in range(n_nodes)}
        neuron_activities = {i:'It: {}, act: {}'.format(Network.draw_counter, round(self.neurons[i].state, 2)) for i in self.neurons.keys()}
        nx.draw_networkx_labels(graph, pos, labels=neuron_ids, font_size=12, font_color='k', font_family='sans-serif', font_weight='normal', alpha=1.0, bbox=None, ax=None)
        nx.draw_networkx_labels(graph, pos_right, labels=neuron_activities, font_size=12, font_color='k', font_family='sans-serif', font_weight='normal', alpha=1.0, bbox=None, ax=None)

        plt.show(block=False)
        #plt.show()

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