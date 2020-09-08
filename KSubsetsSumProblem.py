import math
import time

def getAllPossibleSubsets(S, D, s, i): # This function gives subsets of indexes of appropriate elements in Set

    if s == 0:
        return [[]]
    SSofTaken = []
    SSofUnTaken = []

    if D[s][i] & 2:
        SSofTaken = getAllPossibleSubsets(S, D, s - S[i - 1], i - 1)
        SSofTaken = [k + [i - 1] for k in SSofTaken]

    if D[s][i] & 1:
        SSofUnTaken = getAllPossibleSubsets(S, D, s, i - 1)

    return SSofTaken + SSofUnTaken


def findSumEqualSubsets(S, SubSetSum, n):

    D = [[0 for i in range(0, n + 1)] for s in range(0, SubSetSum + 1)]
    for i in range(0, n + 1):
        D[0][i] = 1
    for s in range(1, SubSetSum + 1):
        for i in range(1, n + 1):
            if S[i - 1] > s:
                D[s][i] = 1 if D[s][i - 1] > 0 else 0
            else:
                D[s][i] += 1 if D[s][i - 1] > 0 else 0
                D[s][i] += 2 if D[s - S[i - 1]][i - 1] > 0 else 0

    return D

def AreSubsetsDisconnected(SS1, SS2, C):

    for i in SS1:
        C[i] = 1
    for i in SS2:
        if C[i]:
            for i in SS1:
                C[i] = 0
            return False
    for i in SS1 + SS2:
        C[i] = 0
    return True

def Is_K_SetDisconnected(KS, K, C, AllSubsets):

    for i in range(0, K - 1):
        for j in range(i + 1, K):
            if not AreSubsetsDisconnected(AllSubsets[KS[i]], AllSubsets[KS[j]], C):
                return False
    return True
### V1
# def RecKSetFind(SetsOfKDisSubsets, KS, K, c, C, AllSubSets, SubsetsNumb, BC):
#
#     if c == K:
#         if Is_K_SetDisconnected(KS, K, C, AllSubSets):
#             SetsOfKDisSubsets.append(KS.copy())
#         else:
#             BC[0] += 1
#         # print(f"Non Correct : {BC[0]}, Correct : {len(SetsOfKDisSubsets)}")
#         return
#
#     for i in range(KS[c - 1] + 1, SubsetsNumb - (K - c) + 1):
#         KS[c] = i
#         RecKSetFind(SetsOfKDisSubsets, KS, K, c + 1, C, AllSubSets, SubsetsNumb, BC)

### V2
def RecKSetFind(SetsOfKDisSubsets, KS, K, c, C, AllSubSets, SubsetsNumb, BC):

    if c == K:
        SetsOfKDisSubsets.append(KS.copy())
        return

    for i in range(KS[c - 1] + 1, SubsetsNumb - (K - c) + 1):
        KS[c] = i
        if Is_K_SetDisconnected(KS, c + 1, C, AllSubSets):
            RecKSetFind(SetsOfKDisSubsets, KS, K, c + 1, C, AllSubSets, SubsetsNumb, BC)


def find_K_EqualSumSubsets(S, K):

    n = len(S)
    SetSum = sum(S)
    if SetSum % K != 0:
        return None, None, None

    D = findSumEqualSubsets(S, SetSum // K, n)
    if not D[SetSum // K][n]:
        return None, None, None
    AllSubsets = getAllPossibleSubsets(S, D, SetSum // K, n)
    SubsetsNumb = len(AllSubsets)
    if SubsetsNumb < K:
        return None, None, None

    C = [0] * n
    SetsOfKDisSubsets = []
    KS = [-1] * K
    BC = [0]
    for i in range(0, SubsetsNumb - K + 1):
        KS[0] = i
        RecKSetFind(SetsOfKDisSubsets, KS, K, 1, C, AllSubsets, SubsetsNumb, BC)


    return SetsOfKDisSubsets, D, AllSubsets


def printCell(a, cellWidth):
    if a > 0:
        print(" " * (cellWidth - math.floor(math.log(a, 10)+ 1) + 1) + f"{a}", end="")
    else:
        print(" " * (cellWidth) + f"{a}", end="")


def printList(List, cellWidth):
    print("[", end="")
    for i in range(0, len(List) - 1):
        printCell(List[i], cellWidth)
        print(",", end = "")
    printCell(List[n - 1], cellWidth)
    print("]")

if __name__ == '__main__':
    start_time = time.time()

    S = [1, 4, 6, 2, 8, 4, 3, 6, 8, 10, 14, 4, 10, 5, 5]
    K = 5

    n = len(S)
    SetsOfKDisSets, D, AllSubsets = find_K_EqualSumSubsets(S, K)

    cellWidth =  math.floor(math.log(max(S), 10) + 1)
    SubSetSum = sum(S) // K
    sumIndexWidth = math.floor(math.log(SubSetSum, 10) + 1)

    if not SetsOfKDisSets:
        print("There is no solution")
        exit(0)
    else:
        print("D:__________________________")
        print("          ", end="")
        printList([i for i in range(0, n)], cellWidth)
        print("          ", end="")
        printList(S, cellWidth)
        for s in range(0, SubSetSum + 1):
            printCell(s, sumIndexWidth)
            print(" : ", end="")
            printList(D[s], cellWidth)

        print("\nK subsets:__________________")

        for i in range(0, len(SetsOfKDisSets)):
            print(f"{i}:______")
            for j in range(0, len(SetsOfKDisSets[i])):
                print(f"    {AllSubsets[SetsOfKDisSets[i][j]]} idx -> val {[S[k] for k in AllSubsets[SetsOfKDisSets[i][j]]]}")

    end_time = time.time()
    print(f"Time execution: {end_time - start_time}")