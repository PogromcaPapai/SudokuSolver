from time import perf_counter

columns = [{1,2,3,4,5,6,7,8,9} for i in range(9)]
rows = [{1,2,3,4,5,6,7,8,9} for i in range(9)]
fields = [{1,2,3,4,5,6,7,8,9} for i in range(9)]

class Region(object):
    
    def __init__(self):
        self.possible = {1,2,3,4,5,6,7,8,9}
        self.squares = []
    
    def append(self, object):
        self.squares.append(object)
    
    def pop(self, number):
        self.possible.discard(number)

columns = [Region() for i in range(9)]
rows = [Region() for i in range(9)]
fields = [Region() for i in range(9)]

class Square(object): #TODO: stworzyć narzędzia do porównywania pól ze sobą
    """ Serves as a representation for 1 field """
    def __init__(self, id, val):
        self.id = id
        self.row = id//9
        self.column = id - (self.row)*9
        self.field = 3*((self.row)//3)+((self.column)//3) # rown and column in <0,8>
        self.row_rep = rows[self.row]
        self.row_rep.append(self)
        self.column_rep = columns[self.column]
        self.column_rep.append(self)
        self.field_rep = fields[self.field]
        self.field_rep.append(self)
        if val in ['1','2','3','4','5','6','7','8','9']:
            self.value = int(val)
        elif val == ' ':
            self.value = 0
        else:
            raise TypeError
        
    def __repr__(self):
        return str(self.value)

    def right(self, distance = 1):
        return self.row_rep.squares[self.row+distance]
    
    def left(self, distance = 1):
        pass

    def up(self, distance = 1):
        pass
    
    def down(self, distance = 1):
        pass

    def get_value(self):
        return self.value
    
    def eval(self):
        """Evaluates possible values and if possible changes it"""
        if self.get_value()>0:
            return None
        possible = self.row_rep & self.column_rep & self.field_rep
        if len(possible) == 1:
            self.value = possible.pop()
            print('Square',str(self.get_place()),'rozwiazane')

    def get_place(self):
        return self.column, self.row, self.field
    
def construct():
    id = 0
    table = []
    for i in range(9):
        new = list(input())
        assert len(new)==9
        for i in new:
            table.append(Square(id, i))
            id += 1
    return table

def judge(table):
    for i in table:
        i.row_rep.discard(i.get_value())
        i.field_rep.discard(i.get_value())
        i.column_rep.discard(i.get_value())
    for i in table:
        i.eval()

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

if __name__ == '__main__':
    table = construct()
    print('trwa rozwiązywanie')
    start = perf_counter()
    while not end_check(table):
        judge(table)
        print('koniec tury')
    printwhole(table)
    print('Czas w sekundach:',perf_counter()-start)