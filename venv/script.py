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

#generovanie poli P a Q pre algoritmus
P = []
Q = []
last_occ_index = 0
index=0
for key, value in sorted_dictionary.items():
    if key in over_limit_words_array:
        P.append(value/sum_of_all_occurrences)
        indices = [last_occ_index, index]
        last_occ_index = index
        ################################################################
        print(sum(sorted_dictionary.values() for i in indices))
    index+=1


#dlzka mojho pola slov nad 50000
n = len(over_limit_words_array)












#algorimtus pre vytvorenie OBST zo https://stackoverflow.com/questions/46160969/generating-an-optimal-binary-search-tree-cormen

# p = pd.Series(P, index=range(1, n+1))
# q = pd.Series(Q)
#
# e = pd.DataFrame(np.diag(Q), index=range(1, n+2))
# w = pd.DataFrame(np.diag(Q), index=range(1, n+2))
# root = pd.DataFrame(np.zeros((n, n)), index=range(1, n+1), columns=range(1, n+1))
#
# print(p)
# print(q)
# for l in range(1, n+1):
#     for i in range(1, n-l+2):
#         j = i+l-1
#         e.set_value(i, j, np.inf)
#         w.set_value(i, j, w.get_value(i, j-1) + p[j] + q[j])
#         for r in range(i, j+1):
#             t = e.get_value(i, r-1) + e.get_value(r+1, j) + w.get_value(i, j)
#             if t < e.get_value(i, j):
#                 e.set_value(i, j, t)
#                 root.set_value(i, j, r)
#
# print(e)
# print(w)
# print(root)