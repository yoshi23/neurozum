from network import NetworkFactory


if __name__ == '__main__':
    print("dicsak")

    network = NetworkFactory.makeNetwork()

    post_synaptic_element = None

    for i in range(10):
        print("creating neuron number: %s"%i)
        neuron = NetworkFactory.makeNeuron()

        network.addNeuron(neuron)

        if i > 0:
            for j in range(1,i):
                synapse = NetworkFactory.makeSynapse(neuron.neuron_id - j, neuron.neuron_id)
                synapse.weight = -1 #random.random()
                neuron.add_connection(synapse)
                network.neurons.get(neuron.neuron_id-j).add_connection(synapse)

    first_neuron  = network.neurons.get(0)
    last_neuron = network.neurons.get(list(network.neurons.keys())[-1])
    synapse = NetworkFactory.makeSynapse(last_neuron.neuron_id, first_neuron.neuron_id)
    synapse.weight = 0 #-1 #random.random()
    first_neuron.add_connection(synapse)
    last_neuron.add_connection(synapse)

    """
    synapse = NetworkFactory.makeSynapse(4,8)
    synapse. weight = -1
    network.neurons.get(4).add_connection(synapse)
    network.neurons.get(8).add_connection(synapse)
    """

    for i in range(5):

        print("round %s"%i)
        for neuron in network.neurons.values():
            pre_synapses = []
            post_synapses = []
            print("neuron: %s"%(neuron.neuron_id))
            if len(neuron.presynaptic_connections) > 0:
                for s in range(len(neuron.presynaptic_connections)):
                    pre_synapses.append(neuron.presynaptic_connections[s].post_id)
            if len(neuron.postsynaptic_connections) > 0:
                for s in range(len(neuron.postsynaptic_connections)):
                    post_synapses.append(neuron.postsynaptic_connections[s].pre_id)
            print("state before: {}\n connected with: \n modified by: {} and modifies: {}".format(neuron._state, post_synapses, pre_synapses ))
            neuron.simulate()
            print("state after: {}\n\n\n".format(neuron._state))

    network.draw()
    print("csajé")

