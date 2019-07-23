from construct import Square, construct


class Case(object):


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
    print('\n')

def end_check(table):
    sum = 0
    for i in table:
        sum += i.get_value()
    return sum==405


'''
def eval(self):
    """Evaluates possible values and if possible changes it"""
    if self.get_value()>0:
        return None
    possible = self.row_rep & self.column_rep & self.field_rep
    if len(possible) == 1:
        self.value = possible.pop()
        print('Square',str(self.get_place()),'rozwiazane')
'''