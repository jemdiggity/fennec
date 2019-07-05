from .core import Component, Circuit, Pin, Net
from .passive import ResistorDividerFactory

class OpampComponent(Component):
    def __init__(self):
        Component.__init__(self, [Pin('in-', self), Pin('in+', self), Pin('out', self), Pin('vcc', self), Pin('vss', self)])

class OpampFactory():
    configurations = ['inverting', 'non-inverting']
    def __init__(self, configuration, gain, total_resistance):
        if configuration not in self.configurations:
            raise Exception("unknown configuration")
        self.configuration = configuration
        self.gain = gain
        self.total_resistance = total_resistance
    def create(self):
        circuit = Circuit()
        opamp = OpampComponent()
        if self.configuration == 'inverting':
            rdiv = ResistorDividerFactory(1/self.gain - 1, self.total_resistance).create()
            circuit.add_subcircuit(rdiv)
            nets = [Net('input', [rdiv.get_net('3')]),
                Net('inverting', [opamp.get_pin('in-'), rdiv.get('2')]),
                Net('output', [opamp.get_pin('out'), rdiv.get_net('1')]),
                Net('common', [opamp.get_pin('in+')]),
                Net('vcc', [opamp.get_pin('vcc')]),
                Net('vss', [opamp.get_pin('vss')])]
            for net in nets:
                circuit.add_net(net)
        elif self.configuration == 'non-inverting':
            rdiv = ResistorDividerFactory(self.gain - 1, self.total_resistance).create()
            circuit.add_subcircuit(rdiv)
            nets = [Net('input', [opamp.get_pin('in+')]),
                Net('inverting', [opamp.get_pin('in-'), rdiv.get_net('2')]),
                Net('output', [opamp.get_pin('out'), rdiv.get_net('1')]),
                Net('common', [rdiv.get_net('3')]),
                Net('vcc', [opamp.get_pin('vcc')]),
                Net('vss', [opamp.get_pin('vss')])]
            for net in nets:
                circuit.add_net(net)
        return circuit
