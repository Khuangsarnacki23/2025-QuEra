#3
import math
from bloqade import move
from kirin.passes import aggressive
from iquhack_scoring import MoveScorer

import networkx as nx
import cirq
import matplotlib.pyplot as plt

pi = math.pi
#Have to move to gate zone to execute
#Leaves qbit in gate zone afterwards
@move.vmove
def local_hadamard(state: move.core.AtomState, indices) -> move.core.AtomState:
    state = move.LocalXY(state, 0.25 * pi, 0.5 * pi, indices)
    state = move.LocalRz(state, pi, indices)
    state = move.LocalXY(state, -0.25 * pi, 0.5 * pi, indices)
    return state

@move.vmove
def global_hadamard(state: move.core.AtomState) -> move.core.AtomState:
    state = move.GlobalXY(state, 0.25*pi, 0.5*pi)
    state = move.GlobalRz(state, pi)
    state = move.GlobalXY(state, -0.25 * pi, 0.5 * pi)
    return state

@move.vmove
def cx_layer(state: move.core.AtomState, storage_site: int, gate_index: int):
    state.gate[[gate_index]] = move.Move(state.storage[[storage_site]])
    state = local_hadamard(state, [gate_index])
    state = move.GlobalCZ(state)
    state = local_hadamard(state, [gate_index])
    state.storage[[storage_site]] = move.Move(state.gate[[gate_index]])
    return state

@move.vmove
def main(int alpha, int beta):
    q = move.NewQubitRegister(4)
    state = move.Init(qubits=[q[0],q[1],q[2],q[4]], indices=[0,1,2,3])

    state = global_hadamard(state)
    state.gate[[0,1]] = move.Move(state.storage[[0,1]])
    



def qaoa_generator(gamma:list[float],beta:list[float],N:int,seed:int=None):
    G = nx.random_regular_graph(3,N,seed)
    
    # Draw the graph
    plt.figure(figsize=(4, 3))
    nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1000, font_size=15)
    plt.title("Graph Plot")
    plt.show()

    qubits = {i:cirq.LineQubit(i) for i,_ in enumerate(G.nodes)}
    circuit = cirq.Circuit()
    for q in qubits.values():
        circuit.append(cirq.H(q))
    for g,b in zip(gamma,beta):
        for e in G.edges:
            circuit.append(cirq.CZ(qubits[e[0]],qubits[e[1]])**g)
        for q in qubits.values():
            circuit.append(cirq.X(q)**b)
    return circuit


gamma = [0.4877097327098487/math.pi, 0.8979876956225422/math.pi]
beta = [0.5550603400685824/math.pi, 0.29250781484335187/math.pi]

qaoa_generator(gamma,beta,4,1)

