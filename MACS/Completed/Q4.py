#4
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
def main():
    q = move.NewQubitRegister(9)
    state = move.Init(qubits=[q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8]], indices=[0,1,2,3,4,5,6,7,8])

    state.gate[[0,1]] = move.Move(state.storage[[0,3]])
    state = local_hadamard(state, [1])
    state = move.GlobalCZ(state)
    state = local_hadamard(state, [1])

    state.storage[[3]] = move.Move(state.gate[[1]])
    state.gate[[1]] = move.Move(state.storage[[6]])
    state = local_hadamard(state, [1])
    state = move.GlobalCZ(state)
    state = local_hadamard(state, [1])

    state.storage[[6]] = move.Move(state.gate[[1]])
    state.gate[[1,2,3,4,5]] = move.Move(state.storage[[1,3,4,6,7]])
    state = local_hadamard(state,[0,2,4])
    state = local_hadamard(state, [1,3,5])
    state = move.GlobalCZ(state)
    state = local_hadamard(state, [1,3,5])
    state.storage[[1,4,7]] = move.Move(state.gate[[1,3,5]])

    state.gate[[1,3,5]] = move.Move(state.storage[[2,5,8]])
    state = local_hadamard(state, [1,3,5])
    state = move.GlobalCZ(state)
    state = local_hadamard(state, [1,3,5])
    state.storage[[2,5,8]] = move.Move(state.gate[[1,3,5]])
    
    move.Execute(state)


expected_qasm="""
// Generated from Cirq v1.4.1

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1), q(2), q(3), q(4), q(5), q(6), q(7), q(8)]
qreg q[9];


cx q[0],q[3];
cx q[0],q[6];
h q[3];
h q[0];
h q[6];
cx q[3],q[4];
cx q[0],q[1];
cx q[6],q[7];
cx q[3],q[5];
cx q[0],q[2];
cx q[6],q[8];
"""
aggressive.Fold(move.vmove)(main)
scorer = MoveScorer(main, expected_qasm=expected_qasm)
print(scorer.score())
#ani = scorer.animate()
#ani.save("test2.gif")