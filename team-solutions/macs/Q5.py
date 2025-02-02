#5
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
    q = move.NewQubitRegister(7)
    state = move.Init(qubits=[q[0],q[1],q[2],q[3],q[4],q[5],q[6]], indices=[0,1,2,3,4,5,6])

    state.gate[[0,2,4]] = move.Move(state.storage[[1,2,3]])
    state = local_hadamard(state,[0,2,4])
    state.storage[[1,2,3]] = move.Move(state.gate[[0,2,4]])

    state.gate[[0,1]] = move.Move(state.storage[[5,6]])
    state = local_hadamard(state, [0])
    state = move.GlobalCZ(state)
    state = local_hadamard(state, [0])
    state.storage[[5,6]] = move.Move(state.gate[[0,1]])

    state.gate[[0,1,2,3]] = move.Move(state.storage[[0,1,2,4]])
    state = local_hadamard(state, [0,3])
    state = move.GlobalCZ(state)
    state = local_hadamard(state, [0,3])
    state.storage[[0,1,2,4]] = move.Move(state.gate[[0,1,2,3]])

    
    state.gate[[0,1,2,3]] = move.Move(state.storage[[0,2,3,5]])
    state = local_hadamard(state, [0,5])
    state = move.GlobalCZ(state)
    state = local_hadamard(state, [0,5])
    state.storage[[0,2,3,5]] = move.Move(state.gate[[0,1,2,3]])

    state.gate[[0,1]] = move.Move(state.storage[[1,5]])
    state.gate[[2,3]] = move.Move(state.storage[[4,6]])
    state = local_hadamard(state, [1,2])
    state = move.GlobalCZ(state)
    state = local_hadamard(state, [1,2])
    state.storage[[1,5]] = move.Move(state.gate[[0,1]])
    state.storage[[4,6]] = move.Move(state.gate[[2,3]])

    state.gate[[0,1]] = move.Move(state.storage[[2,6]])
    state.gate[[2,3]] = move.Move(state.storage[[3,4]])
    state = local_hadamard(state, [1,3])
    state = move.GlobalCZ(state)
    state = local_hadamard(state, [1,3])
    state.storage[[2,6]] = move.Move(state.gate[[0,1]])
    state.storage[[3,4]] = move.Move(state.gate[[2,3]])

    state.gate[[0,1]] = move.Move(state.storage[[0,3]])
    state.gate[[2,3]] = move.Move(state.storage[[1,6]])
    state = local_hadamard(state, [0,3])
    state = move.GlobalCZ(state)
    state = local_hadamard(state, [0,3])
    state.storage[[0,3]] = move.Move(state.gate[[0,1]])
    state.storage[[1,6]] = move.Move(state.gate[[2,3]])

    state.gate[[0,1]] = move.Move(state.storage[[1,6]])
    state = local_hadamard(state, [1])
    state = move.GlobalCZ(state)
    state = local_hadamard(state, [1])
    state.storage[[1,6]] = move.Move(state.gate[[0,1]])
    
    move.Execute(state)

expected_qasm="""
// Generated from Cirq v1.4.1

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2), q(3), q(4), q(5), q(6)]
qreg q[7];


h q[1];
h q[2];
h q[3];
cx q[6],q[5];
cx q[1],q[0];
cx q[2],q[4];
cx q[3],q[5];
cx q[2],q[0];
cx q[1],q[5];
cx q[6],q[4];
cx q[2],q[6];
cx q[3],q[4];
cx q[3],q[0];
cx q[1],q[6];
"""

aggressive.Fold(move.vmove)(main)
scorer = MoveScorer(main, expected_qasm=expected_qasm)
#print(scorer.generate_qasm())
print(scorer.score())