from context import fennec
from fennec import OpampFactory, PassiveFilterFactory
from fennec.core import *
from fennec import utils

if __name__ == '__main__':
    opamp = OpampFactory('non-inverting', gain=10, total_resistance=10e5).create()
    filter = PassiveFilterFactory('low-pass', frequency=(20*10e3), minimum_resistance=10e4).create()

    audio_amp = Circuit()
    audio_amp.add_subcircuit(opamp)
    audio_amp.add_subcircuit(filter)
    audio_amp.add_net(Net('opamp_filt', [filter.get_net('output'), opamp.get_net('input')]))
    audio_amp.add_net(Net('ground', [filter.get_net('common'), opamp.get_net('common')]))

    utils.print_circuit(audio_amp)

#amalgamate multipart components eg two single op-amps into one dual op-amp (manual/automatic)
#partsChooser = PartsChooser(min_footprint="0402")
#concrete = partsChooser.process(audio_amp)
#bom = concrete.BOM()
#pcb = Pcb(concrete)
#pcb.place()
#pcb.route()
