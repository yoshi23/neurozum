


class SynapseError(Exception):
    def __init__(self, pre_id, post_id):
        self.pre_id = pre_id
        self.post_id = post_id

class UnkownSynapseError(Exception):
    pass


class ActivityError(Exception):
    pass

class WeightError(Exception):
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
