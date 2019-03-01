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
for key, v in full_dictionary.items():
    if v > 50000:
        over_limit_words_array.append(key)

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
print('------------------------------------------')

# rekurzivny algortimus pre vytvorenie bst z https://walkccc.github.io/CLRS/Chap15/15.5/
def construct_optimal_bst():
    k = int(root.iat[1,len(p)-1])
    print(over_limit_words_array[k],'je korenom stromu')

    left, right = [(1, k - 1,)], [(k + 1, len(p)-1,)]
    print(left)
    print(right)
    p_arr = [k]
    while p_arr:
        if left:
            i, j = left.pop(0)
            if j < i:
                print(over_limit_words_array[j],'je lavym potomkom',over_limit_words_array[p_arr[0]])
            else:
                k = int(root.iat[i, j])
                print(over_limit_words_array[k],'je lavym potomkom',over_limit_words_array[p_arr[0]])
                p_arr[:0] = [k]
                left.insert(0, (i, k - 1,))
                right.insert(0, (k + 1, j))
        else:
            i, j = right.pop(0)
            if j < i:
                print(over_limit_words_array[j],'je pravym potomkom',over_limit_words_array[p_arr.pop(0)])
            else:
                k = int(root.iat[i, j])
                print(over_limit_words_array[k],'je pravym potomkom',over_limit_words_array[p_arr.pop(0)])
                p_arr[:0] = [k]
                left.insert(0, (i, k - 1))
                right.insert(0, (k + 1, j,))


construct_optimal_bst()

def pocet_porovnani(word):
    return 0