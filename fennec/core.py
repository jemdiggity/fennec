class Pin:
    def __init__(self, name, component):
        self.name = name
        self.component = component

class Net:
    def __init__(self, name, connections = None):
        self.name = name
        if connections is None:
            self.connections = []
        else:
            self.connections = connections
    def add(self, other):
        self.connections.append(other)

class Circuit:
    def __init__(self, netlist = None, subcircuits = None):
        if netlist is None:
            self.netlist = {}
        else:
            self.netlist = {net.name:net for net in netlist}

        if subcircuits is None:
            self.subcircuits = []
        else:
            self.subcircuits = subcircuits
    def add_net(self, net):
        if net.name in self.netlist:
            raise Exception('Net exists')
        self.netlist[net.name] = net
    def get_net(self, name):
        return self.netlist[name]
    def add_subcircuit(self, subcircuit):
        self.subcircuits.append(subcircuit)

class Component:
    def __init__(self, pins = None):
        if pins is None:
            self.pins = {}
        else:
            self.pins = {pin.name:pin for pin in pins}
        self.concrete_component = None
    def get_pin(self, name):
        return self.pins[name]

class PassiveComponent(Component):
    def __init__(self, value):
        Component.__init__(self, [Pin(0, self), Pin(1, self)])
        self.value = value
