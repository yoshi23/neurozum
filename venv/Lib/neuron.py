import math
import random
from collections import OrderedDict

class SynapseError(Exception):
    def __init__(self, pre_id, post_id):
        self.pre_id = pre_id
        self.post_id = post_id

class ActivityError(Exception):
    pass

class WeightError(Exception):
    pass

class UnkownSynapseError(Exception):
    pass

class ConstantViolationError(Exception):
    pass

class Synapse(object):

    def __init__(self, pre_id, post_id):
        self._pre_id = pre_id
        self._post_id = post_id
        self._weight = 0
        self._activity = 0

    @property
    def pre_id(self):
        return self._pre_id

    @pre_id.setter
    def pre_id(self, value):
        raise ConstantViolationError("tried to modify synape's pre-synaptic element")

    @property
    def post_id(self):
        return self._post_id

    @post_id.setter
    def post_id(self, value):
        raise ConstantViolationError("tried to modify synape's post-synaptic element")

    @property
    def activity(self):
        return self._activity

    @activity.setter
    def activity(self, activity):
        if activity > 1 or activity < -1:
            raise ActivityError(self.pre_id, self._post_id)
        else:
            self._activity = activity

    @activity.getter
    def activity(self):
        return self._activity


    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, weight):
        if weight > 1 or weight < -1:
            raise WeightError(self.pre_id, self._post_id)
        else:
            self._weight = weight

    @weight.getter
    def weight(self):
        return self._weight


class Neuron(object):
    next_id = 0

    def __init__(self):
        self.neuron_id = Neuron.next_id
        Neuron.next_id += 1
        self._state = 0
        self.input = 0
        self.presynaptic_connections = []
        self.postsynaptic_connections = []
        self.bias = 0
        self.memory = 0

    def add_connection(self, synapse):
        if synapse.pre_id == self.neuron_id:
            self.presynaptic_connections.append(synapse)
        elif synapse.post_id == self.neuron_id:
            self.postsynaptic_connections.append(synapse)
        else:
            raise UnkownSynapseError("ID of provided synapse does not match neuron %s; synapse: %s, %s"%(self.neuron_id, synapse.pre_id, synapse.post_id))

    def simulate(self):
        def sigmoid(x):
            return 1 / (1 + math.exp(-x))

        new_state = 0
        for incoming_stimulus in self.postsynaptic_connections:
            new_state += incoming_stimulus.activity *incoming_stimulus.weight
            print("new state: {}; weight: {}".format(new_state, incoming_stimulus.weight))
        self._state = sigmoid(self._state * self.memory + new_state)

        for outgoing_stimulus in self.presynaptic_connections:
            outgoing_stimulus.activity = self._state


class Network(object):

    def __init__(self):
        self.neurons = OrderedDict()
        self.connections = {}

    def addNeuron(self, neuron):
        self.neurons[neuron.neuron_id] = neuron

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

if __name__ == '__main__':
    print("dicsak")

    network = NetworkFactory.makeNetwork()

    post_synaptic_element = None

    for i in range(10):
        print("creating neuron number: %s"%i)
        neuron = NetworkFactory.makeNeuron()

        network.addNeuron(neuron)

        if i > 0:

            synapse = NetworkFactory.makeSynapse(neuron.neuron_id - 1, neuron.neuron_id)
            synapse.weight = -1 #random.random()
            neuron.add_connection(synapse)
            network.neurons.get(neuron.neuron_id-1).add_connection(synapse)

    first_neuron  = network.neurons.get(0)
    last_neuron = network.neurons.get(list(network.neurons.keys())[-1])
    synapse = NetworkFactory.makeSynapse(last_neuron.neuron_id, first_neuron.neuron_id)
    synapse.weight = 0 #-1 #random.random()
    first_neuron.add_connection(synapse)
    last_neuron.add_connection(synapse)

    for i in range(5000):

        print("round %s"%i)
        for neuron in network.neurons.values():
            print("neuron: %s"%(neuron.neuron_id))
            if len(neuron.presynaptic_connections) > 0:
                pre_synapse = neuron.presynaptic_connections[0].post_id
            else:
                pre_synapse = None
            if len(neuron.postsynaptic_connections):
                post_synapse = neuron.postsynaptic_connections[0].pre_id
            else:
                post_synapse = None
            print("state before: {}\n connected with: \n modified by: {} and modifies: {}".format(neuron._state, post_synapse, pre_synapse ))
            neuron.simulate()
            print("state after: {}\n\n\n".format(neuron._state))


    print("csajé")



