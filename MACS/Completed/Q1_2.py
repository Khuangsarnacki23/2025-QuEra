#1.2
import math
from bloqade import move
from kirin.passes import aggressive
from iquhack_scoring import MoveScorer

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
def cx_layer(state: move.core.AtomState, storage_site: int, control_index: int, target_index: int)  -> move.core.AtomState:
    state = local_hadamard(state, [target_index])
    state.gate[[control_index]] = move.Move(state.storage[[storage_site]])
    state = move.GlobalCZ(state)
    state.storage[[storage_site]] = move.Move(state.gate[[control_index]])
    state = local_hadamard(state, [target_index])
    return state


@move.vmove
def main():
    q = move.NewQubitRegister(3)
    state = move.Init(qubits=[q[0],q[1],q[2]], indices=[0,1,2])

    state.gate[[0]] = move.Move(state.storage[[2]])
    state = local_hadamard(state, [0])

    state = cx_layer(state,1,1,0)
    state = move.LocalRz(state, -0.25*pi,[0])

    state = cx_layer(state,0,1,0)
    state = move.LocalRz(state, 0.25*pi,[0])

    state = cx_layer(state,1,1,0)
    state = move.LocalRz(state, -0.25*pi,[0])
    state.storage[[0]] = move.Move(state.gate[[2]])
    state.gate[[1]] = move.Move(state.storage[[1]])
    state = move.LocalRz(state, 0.25*pi,[1])

    state.gate[[0]] = move.Move(state.storage[[2]])
    state.storage[[1]] = move.Move(state.gate[[1]])

    state = cx_layer(state,0,1,0)
    state = move.LocalRz(state, 0.25*pi,[0])
    state = local_hadamard(state, [0])

    state.storage[[2]] = move.Move(state.gate[[0]])

    state.gate[[0]] = move.Move(state.storage[[1]])
    state = cx_layer(state,0,1,0)

    state = move.LocalRz(state, -0.25*pi, [0])
    state.storage[[1]] = move.Move(state.gate[[0]])

    state.gate[[1]] = move.Move(state.storage[[0]])
    state = move.LocalRz(state, 0.25*pi, [1])
    state.storage[[0]] = move.Move(state.gate[[1]])

    state.gate[[0]] = move.Move(state.storage[[1]])
    state = cx_layer(state,0,1,0)
    #state.storage[[1]] = move.Move(state.gate[[0]])

    move.Execute(state)

expected_qasm="""
// Generated from Cirq v1.4.1

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2)]
qreg q[3];


ccx q[0],q[1],q[2];
"""

aggressive.Fold(move.vmove)(main)
scorer = MoveScorer(main, expected_qasm=expected_qasm)
#print(scorer.generate_qasm())
print(scorer.score())