import numpy as np
import pandas as pd
import json
import warnings

warnings.filterwarnings("ignore")
np.set_printoptions(threshold=np.inf)

file  = open("dictionary.txt", "r")
lines = file.read().splitlines()
file.close()

full_dictionary = {}
sorted_dictionary = {}
limit = 50000
over_limit_words_array = []

#rozparsovanie
for line in lines:
    splitted_line = line.split(' ')
    full_dictionary[splitted_line[1]] = int(splitted_line[0])

#suma vsetkych vyskytov potrebna k vypocitaniu p pre kazdy kluc
sum_of_all_occurrences= sum(full_dictionary.values())

#pomocne pole stringov ktore sa vyskytuju > 50 000 krat
for k, v in full_dictionary.items():
    if v > 50000:
        over_limit_words_array.append(k)

#stale sa drzime lexikologickeho zoradenia
over_limit_words_array.sort()
#zosortovanie povodneho slovnika
sorted_dictionary_array=sorted(full_dictionary.keys(), key=lambda x:x.lower())
for string in sorted_dictionary_array:
    sorted_dictionary[string] = full_dictionary[string]

#kontrolny zapis do suboru, pouzity na overenia spravneho generovanie p a q hodnot
file = open('sorted_dict', 'w')
file.write(json.dumps(sorted_dictionary))
file.close()

#generovanie poli P a Q pre algoritmus
P = []
Q = []

#pomocne pole potrebne pre pocitanie parcialnych sum
sorted_dictionary_values = list(sorted_dictionary.values())

#funkcia pre vypocet q
def q_value_generator (bef_occ_index,now_index):
    cumulative_sum = 0
    if now_index == 0:
        return 0
    else:
        for i in range(bef_occ_index+1,now_index-1):
            cumulative_sum += sorted_dictionary_values[i]
        return cumulative_sum/sum_of_all_occurrences

before_occ_index = 0
index=0
for key, value in sorted_dictionary.items():
    if key in over_limit_words_array:
        P.append(value/sum_of_all_occurrences)
        Q.append(q_value_generator(before_occ_index,index))
        before_occ_index = index
    index+=1
#trosku ofajc pri vypocte posledneho prvku
Q.append(1-sum(P)-sum(Q))

#pomocne vypisy
file = open('P_Q_values', 'w')
file.write('P\n')
file.write(''.join(str(e) for e in P))
file.write('Q\n')
file.write(''.join(str(e) for e in Q))
file.close()

#dlzka mojho pola slov nad 50000
n = len(P)

#algorimtus pre vytvorenie OBST zo https://stackoverflow.com/questions/46160969/generating-an-optimal-binary-search-tree-cormen

p = pd.Series(P, index=range(1, n+1))
q = pd.Series(Q)

e = pd.DataFrame(np.diag(Q), index=range(1, n+2))
w = pd.DataFrame(np.diag(Q), index=range(1, n+2))
root = pd.DataFrame(np.zeros((n, n)), index=range(1, n+1), columns=range(1, n+1))

for l in range(1, n+1):
    for i in range(1, n-l+2):
        j = i+l-1
        e.set_value(i, j, np.inf)
        w.set_value(i, j, w.get_value(i, j-1) + p[j] + q[j])
        for r in range(i, j+1):
            t = e.get_value(i, r-1) + e.get_value(r+1, j) + w.get_value(i, j)
            if t < e.get_value(i, j):
                e.set_value(i, j, t)
                root.set_value(i, j, r)

print('e',e)
print('w',w)
print('r',root)

file = open('OBST_values', 'w')
file.write('r\n\n')
file.write(root.to_string())
file.close()

print('---------------------------------------------------')
print('Priemerny pocet krokov v strome pri vyhladavani prvku v mojom strome = ', e.iat[0,-1])

def construct_binary_bst(root, i, j, last):
    # if i == j
    #     return
    # if last == 0
    #     print root[i, j] + "is the root"
    # else if j < last:
    #     print root[i, j] + "is the left child of" + last
    # else
    #     print root[i, j] + "is the right child of" + last
    # CONSTRUCT-OPTIMAL-BST(root, i, root[i, j] - 1, root[i, j])
    # CONSTRUCT-OPTIMAL-BST(root, root[i, j] + 1, j, root[i, j])

def pocet_porovnani(word):
    return 0