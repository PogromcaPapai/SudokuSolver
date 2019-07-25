from time import perf_counter
from functools import reduce

import const
import solve

def printrow(row, table):
    """
    Prints a series of nine elements from a list

    Arguments:
        row : int : which series of element to print
        table : list : list of elements to print
    """
    text = ''
    for i in range(9*row,9*row+9):
        digit = str(table[i])
        if digit == '0': digit = ' '
        text+=digit
    print(text)

def printwhole(table):
    """
    Prints whole list in form of a 9x9 array

    Arguments:
        table : list : list of elements to print
    """
    for i in range(9):
        printrow(i, table)
    print('----')

def end_check(table):
    """
    Checks if all cells in the table are properly solved
    """
    return reduce(lambda x, y: x+y.get_value(), table, 0)==405

if __name__ == "__main__":
    table = const.construct()
    start = perf_counter() #Time measurement starts
    cases = solve.env(table)
    turn=0
    while end_check(table)==False:
        turn += 1
        cases.sort(key=len)
        for i in cases:
            i.update()
            done = i.naked_pair()
            if not done: done = i.naked_single()
            if not done: done = i.hidden_single()
            if done: printwhole(table)
        if turn>=1000: break
    stop = perf_counter()
    printwhole(table)
    print('Solved in', str(round(stop-start,3)),'seconds')
