from time import perf_counter
from functools import total_ordering
from random import randint

class Region(object):
    
    def __init__(self):
        self.possible = {1,2,3,4,5,6,7,8,9}
        self.squares = []

    def __getitem__(self, num):
        return self.squares[num]
    
    def __len__(self):
        return len(self.possible)
    
    def __repr__(self):
        return str(self.possible)
    
    def append(self, object):
        self.squares.append(object)
    
    def pop(self, number):
        self.possible.discard(number)


@total_ordering
class Square(object):
    """
    Serves as a representation for a field
    """
    
    ### Magic functions ###
    
    def __init__(self, id, val):
        """
        Creates a field

        Parameters:
            id (int) : key in the parent list
            val (string) : value entered for a field (' ' or '.' for fields to solve)
        """
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
            self.value = val
            self.update()
        elif val == ' ' or val == '.':
            self.value = 0
            self.update()
        else:
            raise TypeError

    def __repr__(self):
        return str(self.value)

    def __len__(self):
        return len(self.possible)

    def __eq__(self, other):
        return len(self)==len(other)
    
    def __le__(self, other):
        return len(self)<=len(other)

    ### Manipulation ###

    def update(self):
        """ Updates regions and field's `possible` attribute """
        if self.get_value()!=0:
            self.row_rep.pop(self.get_value())
            self.field_rep.pop(self.get_value())
            self.column_rep.pop(self.get_value())
            self.possible = {}
        else:
            self.possible = self.row_rep.possible & self.column_rep.possible & self.field_rep.possible

    ### Movement ###

    def right(self, distance = 1):
        return self.row_rep[self.row+distance]
    
    def left(self, distance = 1):
        return self.row_rep[self.row-distance]

    def up(self, distance = 1):
        return self.column_rep[self.column-distance]
    
    def down(self, distance = 1):
        return self.column_rep[self.column+distance]

    ### Get functions ###

    def get_value(self):
        return self.value

    def get_place(self):
        return self.column, self.row, self.field
    
def createfield():
    global columns; columns = [Region() for i in range(9)]
    global rows; rows = [Region() for i in range(9)]
    global fields; fields = [Region() for i in range(9)]
    

def construct(test=False):
    id = 0
    table = []
    if test==False:
        for i in range(9):
            new = list(input())
            assert len(new)==9
            for i in new:
                table.append(Square(id, i))
                id += 1
    else:
        for i in range(9**2):
            table.append(Square(id, str(randint(1,9))))
            id += 1
    return table

if __name__ == '__main__':
    createfield()
    table = construct()