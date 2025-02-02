
toOptim = [
    (0,1, 'cz'),
    (0,3, 'cz'),
    (0,2, 'cz'),
    (0, 'x'),
    (1,2, 'cz'),
    (1,3, 'cz'),
    (1, 'x'),
    (2,3, 'cz'),
    (0,1, 'cz'),
    (2, 'x'),
    (3, 'x'),
    (0, 3, 'cz'),
    (0, 2, 'cz'),
    (0, 'x'),
    (1, 2, 'cz'),
    (1, 3, 'cz'),
    (1, 'x'),
    (2, 3, 'rz'),
    (2, 'x'),
    (3, 'x')
]

flag = 0

def first_pass_old():
    global flag

    for i in range(len(toOptim)):

        cur = toOptim[i]
        j = i+1
        cur_src = cur[0]

        if type(cur_tgt := cur[1]) == str:
            cur_tgt = 0
        else:
            cur_tgt = 2**cur_tgt

        flag = cur_tgt

        while flag != 15 and j<len(toOptim):

            cur = toOptim[j]
            src = cur[0]
            if type(tgt := cur[1]) == str:
                tgt = 0
            else:
                tgt = 2**tgt

            j+=1

            if 2**cur_src ^ cur_tgt ^ 2**src ^ tgt == 15 :
                if i+2<len(toOptim) and (flag & tgt) == 0:
                    save = toOptim[j-1]
                    for k in range(j-1, i+1, -1):
                        toOptim[k] = toOptim[k-1]
                    toOptim[i+1] = save
                    break

            if tgt!=0:
                flag = flag | tgt
            else:
                flag = flag | 2**src

def first_pass():
    for i in range(len(toOptim)):
        cur = toOptim[i]
        cur_src = cur[0]
        cur_tgt = 0 if isinstance(cur[1], str) else 1 << cur[1]

        flag = cur_tgt

        for j in range(i + 1, len(toOptim)):
            nxt = toOptim[j]
            nxt_src = nxt[0]
            nxt_tgt = 0 if isinstance(nxt[1], str) else 1 << nxt[1]

            if (1 << cur_src) ^ cur_tgt ^ (1 << nxt_src) ^ nxt_tgt == 15:
                if (i + 2 < len(toOptim)) and (flag & nxt_tgt) == 0:
                    # Move the current gate to just after the initial gate
                    toOptim.insert(i + 1, toOptim.pop(j))
                    break

            flag |= nxt_tgt if nxt_tgt else 1 << nxt_src

def second_pass():

    for i in range(len(toOptim)):
        cur = toOptim[i]
        
        if len(cur) == 2 and cur[1] == 'x':
            if cur[0] < 3 and cur[1] == 'x':
                while toOptim[i+1][1] != 'x' and toOptim[i+1][0] != 3:
                    toOptim[i+1], toOptim[i] = toOptim[i], toOptim[i+1]

    for i in range(len(toOptim)):
        cur = toOptim[i]
        if len(cur) == 2 and cur[1] == 'x':
            if cur[0] == 0:
                while toOptim[i+1][1] != 'x' and toOptim[i+1][0] != 1:
                    toOptim[i+1], toOptim[i] = toOptim[i], toOptim[i+1]


def printGates():
    thisList = []

    for item in toOptim:
        thisList.append([str(elem) for elem in item])

    for i in range(len(thisList)):
        print(f"{i}: {', '.join(thisList[i])}")


expected = """
0: 0, 1, cz
1: 0, 3, cz
2: 0, 2, cz
3: 1, 3, cz
4: 0, x
5: 1, 2, cz
6: 1, x
7: 2, 3, cz
8: 0, 1, cz
9: 2, x
10: 3, x
11: 0, 3, cz
12: 0, 2, cz
13: 1, 3, cz
14: 0, x
15: 1, 2, cz
16: 1, x
17: 2, 3, rz
18: 2, x
19: 3, x
"""

print('\n--------x-------\n')
printGates()
print('\n--------x-------\n')
first_pass()
printGates()
print('\n--------x-------\n')
second_pass()
printGates()

#input()
