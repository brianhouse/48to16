K = 36
S = 38
H = 42

C1 = 24
Db1 = 25
D1 = 26
Eb1 = 27
E1 = 28
F1 = 29
Gb1 = 30
G1 = 31
Ab1 = 32
A1 = 33
Bb1 = 34
B1 = 35

C2 = 36
Db2 = 37
D2 = 38
Eb2 = 39
E2 = 40
F2 = 41
Gb2 = 42
G2 = 43
Ab2 = 44
A2 = 45
Bb2 = 46
B2 = 47

C3 = 48
Db3 = 49
D3 = 50
Eb3 = 51
E3 = 52
F3 = 53
Gb3 = 54
G3 = 55
Ab3 = 56
A3 = 57
Bb3 = 58
B3 = 59

C = C4 = 60
Db = Db4 = 61
D = D4 = 62
Eb = Eb4 = 63
E = E4 = 64
F = F4 = 65
Gb = Gb4 = 66
G = G4 = 67
Ab = Ab4 = 68
A = A4 = 69
Bb = Bb4 = 70
B = B4 = 71

C5 = 72
Db5 = 73
D5 = 74
Eb5 = 75
E5 = 76
F5 = 77
Gb5 = 78
G5 = 79
Ab5 = 80
A5 = 81
Bb5 = 82
B5 = 83

C6 = 84
Db6 = 85
D6 = 86
Eb6 = 87
E6 = 88
F6 = 89
Gb6 = 90
G6 = 91
Ab6 = 92
A6 = 93
Bb6 = 94
B6 = 95

C7 = 96
Db7 = 97
D7 = 98
Eb7 = 99
E7 = 100
F7 = 101
Gb7 = 102
G7 = 103
Ab7 = 104
A7 = 105
Bb7 = 106
B7 = 107

MAJ = ION = {1:0, 2:2, 3:4, 4:5, 5:7, 6:9, 7:11, 8:12}
DOR = {1:0, 2:2, 3:3, 4:5, 5:7, 6:9, 7:10, 8:12}
PRG = SUSb9 = {1:0, 2:1, 3:3, 4:5, 5:7, 6:8, 7:10, 8:12}
LYD = {1:0, 2:2, 3:4, 4:6, 5:7, 6:9, 7:11, 8:12}
MYX = DOM = {1:0, 2:2, 3:4, 4:5, 5:7, 6:9, 7:10, 8:12}
AOL = {1:0, 2:2, 3:3, 4:5, 5:7, 6:8, 7:10, 8:12}
LOC = {1:0, 2:1, 3:3, 4:5, 5:6, 6:8, 7:10, 8:12}
MIN = {1:0, 2:2, 3:3, 4:5, 5:7, 6:8, 7:11, 8:12}
DRUMS = {1:0, 2:4}

names = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def get_note_name(n):
    n -= 24
    i = n % 12
    return names[i]

# ledgers = {'C': 5, 'Db': 6, 'D': 6, 'Eb': 7, 'E': 7, 'F': 8, 'Gb': 9, 'G': 9, 'Ab': 10, 'A': 10, 'Bb': 11, 'B': 12} # for voice 3
ledgers = {'B': 4, 'C': 5, 'Db': 6, 'D': 6, 'Eb': 7, 'E': 7, 'F': 8, 'Gb': 9, 'G': 9, 'Ab': 10, 'A': 10, 'Bb': 11}
def get_bass_ledger(n):
    name = get_note_name(n)
    return ledgers[name]


# need an extension to dict that if accessed with a negative number, subtracts 12
# harmony = -12 + abs(harmony) if harmony < 0 else harmony


# actually, the notes should be objects. can then override add, etc.
