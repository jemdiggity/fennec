def print_circuit(circuit):
    if not circuit:
        return
    print('Circuit {} has {} nets and {} subcircuits'.format(
        circuit, len(circuit.netlist), len(circuit.subcircuits)))
    for key,value in circuit.netlist.items():
        print('Net {}:{}'.format(key,value))
    for subcircuits in circuit.subcircuits:
        print_circuit(subcircuits)
