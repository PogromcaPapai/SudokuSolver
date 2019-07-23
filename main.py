from time import perf_counter
from functools import reduce

import const
import solve

def printrow(row, table):
    text = ''
    for i in range(9*row,9*row+9):
        digit = str(table[i])
        if digit == '0': digit = ' '
        text+=digit
    print(text)

def printwhole(table):
    for i in range(9):
        printrow(i, table)
    print('----')

def end_check(table):
    return reduce(lambda x, y: x+y.get_value(), table, 0)==405

if __name__ == "__main__":
    const.createfield()
    table = const.construct()
    cases = solve.env(table)
    start = perf_counter() #Time measurement starts
    while end_check(table)==False:
        cases.sort(key=len)
        for i in cases:
            i.update()
            done = i.naked_single()
            if not done: done = i.hidden_single()
            #printwhole(table)
        print('koniec tury')
    
    printwhole(table)
    print('Solved in', str(round(perf_counter()-start,3)),'seconds')
