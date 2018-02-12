# MS Apriori implementation

import sys

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
    global L
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
                print('i >>>',i,' mis(i) >> ' , mis[i])
            else:
                print(item,' sup >>>',calc_support(item,transactions))
                sup = calc_support(item,transactions)
                if sup >= float(mis[i]):
                    L.append(item)
                if sup >= float(mis[item]):
                    F1.append(item)

    print('L >>>>',L)

    F.append(F1)
    print('F >>>>', F)

def main():
    input()
    #print('SDC >>' + sdc_val)
    #print('Cannot constraints >>', cannot_constraint)
    #print('Must have >>', must_have)
    M = [x[0] for x in sorted(mis.items(), key = lambda x: x[1])]
    init_pass(M,transactions)
    #print(M)

    gen = (k for k in range(2,len(mis)) if F[k-1] is not len(F[k-1]) is not 0)
    for k in gen:
        print(k)
        #if k == 2:
            #candidate_2_gen()

if __name__ == '__main__':
    main()