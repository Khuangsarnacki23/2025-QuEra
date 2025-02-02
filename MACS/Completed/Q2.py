#2
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
def local_crz_05(state: move.core.AtomState, storage_site: int, control_index: int, target_index: int) -> move.core.AtomState:
    angle = pi*0.25

    state = move.LocalRz(state, angle, [target_index])
    state = cx_layer(state, storage_site, control_index, target_index)

    state = move.LocalRz(state, -angle, [target_index])
    state = cx_layer(state, storage_site, control_index, target_index)

    return state

@move.vmove
def local_crz_025(state: move.core.AtomState, storage_site: int, control_index: int, target_index: int) -> move.core.AtomState:
    angle = pi*0.25*0.5

    state = move.LocalRz(state, angle, [target_index])
    state = cx_layer(state, storage_site, control_index, target_index)

    state = move.LocalRz(state, -angle, [target_index])
    state = cx_layer(state, storage_site, control_index, target_index)

    return state


@move.vmove
def main():
    q = move.NewQubitRegister(3)
    state = move.Init(qubits=[q[0],q[1],q[2]], indices=[0,1,2])

    state.gate[[0]] = move.Move(state.storage[[2]])
    state = local_hadamard(state,[0])

    state = local_crz_05(state, 1, 1, 0)
    state = local_crz_025(state, 2, 1, 0)

    state.storage[[2]] = move.Move(state.gate[[0]])

    state.gate[[1]] = move.Move(state.storage[[1]])
    state = local_hadamard(state, [1])
    state = local_crz_05(state, 0, 0, 1)

    state.storage[[1]] = move.Move(state.gate[[1]])

    state.gate[[0]] = move.Move(state.storage[[0]])

    state = local_hadamard(state, [0])

    move.Execute(state)


expected_qasm="""
// Equivalent Circuit

OPENQASM 2.0;
include "qelib1.inc";
gate xy(x, a) qarg {
  rz (a) qarg;
  rx (x) qarg;
  rz (-a) qarg;
}
qreg q[3];
xy (0.7853981633974483, 1.5707963267948966) q[2];
// Local XY
rz (3.141592653589793) q[2];
// Local Rz
xy (-0.7853981633974483, 1.5707963267948966) q[2];
// Local XY
rz (0.7853981633974483) q[2];
// Local Rz
xy (0.7853981633974483, 1.5707963267948966) q[2];
// Local XY
rz (3.141592653589793) q[2];
// Local Rz
xy (-0.7853981633974483, 1.5707963267948966) q[2];
// Local XY
cz q[2], q[1];
// Global CZ
xy (0.7853981633974483, 1.5707963267948966) q[2];
// Local XY
rz (3.141592653589793) q[2];
// Local Rz
xy (-0.7853981633974483, 1.5707963267948966) q[2];
// Local XY
rz (-0.7853981633974483) q[2];
// Local Rz
xy (0.7853981633974483, 1.5707963267948966) q[2];
// Local XY
rz (3.141592653589793) q[2];
// Local Rz
xy (-0.7853981633974483, 1.5707963267948966) q[2];
// Local XY
cz q[2], q[1];
// Global CZ
xy (0.7853981633974483, 1.5707963267948966) q[2];
// Local XY
rz (3.141592653589793) q[2];
// Local Rz
xy (-0.7853981633974483, 1.5707963267948966) q[2];
// Local XY
rz (0.39269908169872414) q[2];
// Local Rz
xy (0.7853981633974483, 1.5707963267948966) q[2];
// Local XY
rz (3.141592653589793) q[2];
// Local Rz
xy (-0.7853981633974483, 1.5707963267948966) q[2];
// Local XY
// Global CZ
xy (0.7853981633974483, 1.5707963267948966) q[2];
// Local XY
rz (3.141592653589793) q[2];
// Local Rz
xy (-0.7853981633974483, 1.5707963267948966) q[2];
// Local XY
rz (-0.39269908169872414) q[2];
// Local Rz
xy (0.7853981633974483, 1.5707963267948966) q[2];
// Local XY
rz (3.141592653589793) q[2];
// Local Rz
xy (-0.7853981633974483, 1.5707963267948966) q[2];
// Local XY
// Global CZ
xy (0.7853981633974483, 1.5707963267948966) q[2];
// Local XY
rz (3.141592653589793) q[2];
// Local Rz
xy (-0.7853981633974483, 1.5707963267948966) q[2];
// Local XY
xy (0.7853981633974483, 1.5707963267948966) q[1];
// Local XY
rz (3.141592653589793) q[1];
// Local Rz
xy (-0.7853981633974483, 1.5707963267948966) q[1];
// Local XY
rz (0.7853981633974483) q[1];
// Local Rz
xy (0.7853981633974483, 1.5707963267948966) q[1];
// Local XY
rz (3.141592653589793) q[1];
// Local Rz
xy (-0.7853981633974483, 1.5707963267948966) q[1];
// Local XY
cz q[0], q[1];
// Global CZ
xy (0.7853981633974483, 1.5707963267948966) q[1];
// Local XY
rz (3.141592653589793) q[1];
// Local Rz
xy (-0.7853981633974483, 1.5707963267948966) q[1];
// Local XY
rz (-0.7853981633974483) q[1];
// Local Rz
xy (0.7853981633974483, 1.5707963267948966) q[1];
// Local XY
rz (3.141592653589793) q[1];
// Local Rz
xy (-0.7853981633974483, 1.5707963267948966) q[1];
// Local XY
cz q[0], q[1];
// Global CZ
xy (0.7853981633974483, 1.5707963267948966) q[1];
// Local XY
rz (3.141592653589793) q[1];
// Local Rz
xy (-0.7853981633974483, 1.5707963267948966) q[1];
// Local XY
xy (0.7853981633974483, 1.5707963267948966) q[0];
// Local XY
rz (3.141592653589793) q[0];
// Local Rz
xy (-0.7853981633974483, 1.5707963267948966) q[0];
// Local XY
"""

aggressive.Fold(move.vmove)(main)
scorer = MoveScorer(main, expected_qasm=expected_qasm)
print(scorer.score())
