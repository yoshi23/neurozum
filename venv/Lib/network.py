from collections import OrderedDict

from neuron import Neuron
from synapse import Synapse

import networkx as nx

import math

import yaml

import matplotlib.pyplot as plt

class MissingEntityError(Exception):
    pass
class DuplicateIdError(Exception):
    pass

class Network(object):
    next_id = 0
    taken_ids = []

    def __init__(self, id = None):
        if (id is not None) and (id in Network.taken_ids):
            raise DuplicateIdError("ID given for new network is already taken.")
        elif (id is None) and (Network.next_id in Network.taken_ids): #previous and this case is separated because if user has given the ID, we want to raise error
            #but in case of simple incrementation, just increment until it's ok.
            while Network.next_id in Network.taken_ids:
                Network.next_id += 1
            id = Network.next_id
        self.network_id  = id
        Network.taken_ids.append(self.network_id)


        self.subnetworks = OrderedDict()
        self.neurons = OrderedDict()
        self.synapses = set()

    def addSubnetwork(self, sub_network):
        self.subnetworks[sub_network.network_id] = sub_network

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
        pos = {i: (i/10 * math.cos(i * 2* math.pi / (self.get_num_of_neurons())), i/10 * math.sin(i * 2* math.pi / (self.get_num_of_neurons()))) for i in range(n_nodes)}
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
    def makeNetwork(config = None, id = None):
        if config is None:
            return Network(id)
        else:
            return NetworkFactory._buildNetworkFromConfig(config)
    @staticmethod
    def makeNeuron():
        return Neuron()
    @staticmethod
    def makeSynapse(pre_id, post_id):
        return Synapse(pre_id, post_id)

    @staticmethod
    def configurationLoader(filename):
        try:
            with open(filename) as f:
                config = yaml.load(f)
        except FileNotFoundError:
            raise
        except Exception:
            raise

        if 'root' not in config:
            raise MissingEntityError("Not a valid config file, missing 'root' from the top level")
        else:
            return config
            #if config['entity'] == 'subnetwork':
            #    new_network = NetworkFactory.makeNetwork()

        #for key,value in config.items():
        #    print('{key}: {value}'.format(key=key,value=value))

    @staticmethod
    def _buildNetworkFromConfig(config):
        networks = []
        print(type(config))
        print(config)
        for entry, subentry in config.items():
            print(entry)
            print('subentry: {}'.format(subentry))
            if subentry['type'] == 'network':
                network = Network(subentry.get('id'))
                for i in range(len(subentry.get('content'))):
                    print('i: {}'.format(i))
                    print("subentry['content']i: %s"%subentry['content'][i])
                    sub_networks = NetworkFactory._buildNetworkFromConfig(subentry['content'][i])
                for i in range(len(sub_networks)):
                    network.addSubnetwork(sub_networks[i])
            if subentry['type'] == 'neuron':
                networks.append(NetworkFactory.makeNeuron())

        return networks