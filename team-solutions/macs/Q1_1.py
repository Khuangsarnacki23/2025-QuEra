#1.1
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
    q = move.NewQubitRegister(3)
    state = move.Init(qubits=[q[0],q[1],q[2]], indices=[0,1,2])
    
    state.gate[[0,1]] = move.Move(state.storage[[0,1]])
    state = move.GlobalCZ(state)
    state.storage[[0]] = move.Move(state.gate[[0]])

    state = local_hadamard(state, [1])

    state.gate[[0]] = move.Move(state.storage[[2]])
    state = move.GlobalCZ(state)
    
    state = local_hadamard(state,[1])    
    
    move.Execute(state)


expected_qasm="""
OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
cz q[0],q[1];
cx q[2],q[1];
"""
aggressive.Fold(move.vmove)(main)
scorer = MoveScorer(main, expected_qasm=expected_qasm)
print(scorer.score())