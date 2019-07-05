from .core import PassiveComponent, Circuit, Net
import math

class PassiveFilterFactory:
    filter_type_options = ['low-pass', 'high-pass']
    def __init__(self, filter_type, frequency, minimum_resistance):
        if filter_type not in self.filter_type_options:
            raise Exception('unknown filtertype {}'.format(filter_type))
        self.filter_type = filter_type
        self.frequency = frequency
        self.minimum_resistance = minimum_resistance
    def createLowPassFilter(self):
        resistor = PassiveComponent({'value':self.minimum_resistance, 'unit':'ohm'})
        capacitor = PassiveComponent({'value':(1/(2 * math.pi * self.frequency * self.minimum_resistance)), 'unit':'farad'})
        circuit = Circuit()
        circuit.add_net(Net('input', [resistor.pins[0]]))
        circuit.add_net(Net('output', [resistor.pins[1], capacitor.pins[0]]))
        circuit.add_net(Net('common', [capacitor.pins[1]]))
        return circuit
    def createHighPassFilter(self):
        resistor = PassiveComponent({'value':self.minimum_resistance, 'unit':'ohm'})
        capacitor = PassiveComponent({'value':(1/(2 * math.pi * self.frequency * self.minimum_resistance)), 'unit':'farad'})
        circuit = Circuit()
        circuit.add_net(Net('input', [capacitor.pins[0]]))
        circuit.add_net(Net('output', [resistor.pins[1], capacitor.pins[0]]))
        circuit.add_net(Net('common', [resistor.pins[1]]))
        return circuit
    def create(self):
        if self.filter_type == 'low-pass':
            return self.createLowPassFilter()
        elif self.filter_type == 'high-pass':
            return self.createHighPassFilter()
        else:
            raise Exception('unknown filter type')

class ResistorDividerFactory:
    def __init__(self, ratio, total_resistance):
        self.ratio = ratio
        self.total_resistance = total_resistance
    def create(self):
        resistance_top = self.ratio * self.total_resistance
        resistance_bottom = self.total_resistance = resistance_top
        resistance_parallel = (resistance_top * resistance_bottom) / (resistance_top + resistance_bottom)
        resistor_top = PassiveComponent({'value': resistance_top, 'unit':'ohm'})
        resistor_bottom = PassiveComponent({'value': resistance_bottom, 'unit':'ohm'})
        circuit = Circuit()
        circuit.add_net(Net('1', [resistor_top.pins[0]]))
        circuit.add_net(Net('2', [resistor_top.pins[1], resistor_bottom.pins[0]]))
        circuit.add_net(Net('3', [resistor_bottom.pins[1]]))
        return circuit
