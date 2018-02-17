# MS Apriori implementation

import sys
import math
import itertools

transactions = []
cannot_constraint = []
must_have = []
mis = {}

def input():
    input_file = open('input1.txt', 'r')
    parameter_file = open('parameter1.txt', 'r')
    for line in input_file:
        line = line.strip()[1:-2]
        data = line.split(', ')
        transactions.append(data)
        #print(data)

    for line in parameter_file:
        if line.find('MIS') is not -1:
            item = line[line.find('(')+1:line.find(')')]
            #print('Item >> ' + item)
            mis_val = line[line.find('=')+1:].strip()
            #print('MIS >> ' + mis_val)
            mis[item] = mis_val

        elif line.find('SDC') is not -1:
            global sdc_val
            sdc_val = line[line.find('=')+1:].strip()

        elif line.find('cannot_be_together') is not -1:
            line = line.split(':')[1].strip()
            while line.find('{') is not -1:
                open_pos = line.find('{')
                close_pos = line.find('}')
                itemset = line[open_pos+1:close_pos]
                cannot_constraint.append(itemset.split(', '))
                line = line[close_pos+1:]

        elif line.find('must-have') is not -1:
            line = line.split(':')[1].strip()
            items = line.split(' or ')
            must_have.extend(items)

    input_file.close()
    parameter_file.close()


def calc_support(item, transactions):
    total = sum(x.count(item) for x in transactions)
    return total/len(transactions)

def init_pass(M, transactions):
    global F
    L = []
    F1 = []
    F = []
    i = None
    for item in M:
        sup = calc_support(item, transactions)
        if i is None and sup < float(mis[item]):
            continue
        else:
            if i is None:
                L.append(item)
                if sup >= float(mis[item]):
                    F1.append(item)
                i = item
                #print('i >>>',i,' mis(i) >> ' , mis[i])
            else:
                #print(item,' sup >>>',calc_support(item,transactions))
                sup = calc_support(item,transactions)
                if sup >= float(mis[i]):
                    L.append(item)
                if sup >= float(mis[item]):
                    F1.append(item)

    #print('L >>>>',L)
    F.append(F1)
    #print('F >>>>', F)
    return L


def candidate_2_gen(L):
    C2 = []
    for item in L:
        if calc_support(item,transactions) >= float(mis[item]):
            for i in range(L.index(item)+1, len(L)):
                sup_i = calc_support(L[i], transactions)
                sup_item = calc_support(item, transactions)
                if (sup_i >= float(mis[item])) and (math.fabs(sup_i-sup_item) <= float(sdc_val)):
                    C2.append([item, L[i]])
    #print("C2", C2)
    return C2


def candidate_gen(Fk_1):
    Ck = []
    pairs = itertools.combinations(Fk_1, 2)
    for pair in pairs:
        f1 = pair[0]
        f2 = pair[1]
        if f1[0] == f2[0]:
            if float(f1[-1]) < float(f2[-1]) and math.fabs(calc_support(f1[-1],transactions) - calc_support(f2[-1],transactions)) <= float(sdc_val):
                c = list(f1)
                c.append(f2[-1])
                s = itertools.combinations(c,len(c)-1)
                Ck.append(c)
                for subset_k_1 in s:
                    if set(c[0]).issubset(set(subset_k_1)) or (mis[c[2]] == mis[c[1]]):
                        if list(subset_k_1) not in Fk_1:
                            Ck.remove(c)
                            break


    return Ck

def ms_apriori():
    Ck = []
    M = [x[0] for x in sorted(mis.items(), key = lambda x: x[1])]
    L = init_pass(M,transactions)
    #print(len(F[1]))

    for k in range(1, len(mis)):
        if k > len(F) or len(F[k-1]) is 0:
            break;
        else:
            #print(k)
            if k == 1:
                Ck = candidate_2_gen(L)
                #F.append(C2)
                #print(F)
            else:
                Ck = candidate_gen(F[k-1])

            Fk = []
            for c in Ck:
                count = 0
                tail_count = 0
                for transaction in transactions:
                    if set(c).issubset(set(transaction)):
                        count += 1

                    if set(c[1:]).issubset(set(transaction)):
                        tail_count += 1

                if (count/len(transactions)) >= float(mis[c[0]]):
                    Fk.append(c)

            if len(Fk) > 0:
                F.append(Fk)
                print('F>>',F)
    return F[-1]

def main():
    input()
    #print('SDC >>' + sdc_val)
    #print('Cannot constraints >>', cannot_constraint)
    #print('Must have >>', must_have)
    print('F>>>>',ms_apriori())


if __name__ == '__main__':
    main()