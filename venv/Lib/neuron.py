import math

class ForcedNeuralStateError(Exception):
    pass

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
        self.memory = 0.5
        self.tau = 4

    def add_connection(self, synapse):
        if synapse.pre_id == self.neuron_id:
            self.presynaptic_connections.append(synapse)
        elif synapse.post_id == self.neuron_id:
            self.postsynaptic_connections.append(synapse)
        else:
            raise UnkownSynapseError("ID of provided synapse does not match neuron %s; synapse: %s, %s"%(self.neuron_id, synapse.pre_id, synapse.post_id))

    def simulate(self):
        def sigmoid(x):
            return 1 / (1 + math.exp(- self.tau * x))

        new_state = 0
        for incoming_stimulus in self.postsynaptic_connections:
            new_state += incoming_stimulus.activity *incoming_stimulus.weight
            print("new state: {}; weight: {}".format(new_state, incoming_stimulus.weight))
        self._state = sigmoid(self._state * self.memory + new_state)

        for outgoing_stimulus in self.presynaptic_connections:
            outgoing_stimulus.activity = self._state


    @property
    def state(self):
        return self._state

    @state.getter
    def state(self):
        return self._state

    @state.setter
    def state(self, *args):
        raise ForcedNeuralStateError("Tried to modify state of neuron manually: {}".format(self.neuron_id))




