class ActivityError(Exception):

    def __init__(self, pre_id, post_id):
        self.pre_id = pre_id
        self.post_id = post_id

class UnkownSynapseError(Exception):
    pass

class ConstantViolationError(Exception):
    pass

class Synapse(object):

    def __init__(self, pre_id, post_id):
        self._pre_id = pre_id
        self._post_id = post_id
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


class Neuron(object):
    next_id = 0

    def __init__(self):
        self.neuron_id = Neuron.next_id
        Neuron.next_id += 1
        self.state = 0
        self.input = 0
        self.presynaptic_connections = []
        self.postsynaptic_connections = []

    def add_connection(self, synapse):
        if synapse.pre_id == self.neuron_id:
            self.presynaptic_connections.append(synapse)
        elif synapse.post_id == self.neuron_id:
            self.postsynaptic_connections.append(synapse)
        else:
            raise UnkownSynapseError("ID of provided synapse does not match neuron %s"%self.neuron_id)

class Network(object):

    def __init__(self):
        self.neurons = {}
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

        synapse = NetworkFactory.makeSynapse(neuron.neuron_id, neuron.neuron_id + 1)


        neuron.add_connection(synapse)
        if i > 0:
            neuron.add_connection(post_synaptic_element)
        post_synaptic_element = synapse

        network.addNeuron(neuron)

    print("csajé")



