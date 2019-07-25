from functools import total_ordering
from random import randint

class Region(object):
    """ Serves as a representation of a column, a row or a field """
    
    def __init__(self):
        self.used = set()
        self.blocked = set()
        self.squares = []

    def __getitem__(self, num):
        return self.squares[num]
    
    def __len__(self):
        return len(self.possible())
    
    def __repr__(self):
        return str(self.possible())
    
    def append(self, object):
        self.squares.append(object)
    
    def block(self, it):
        self.blocked.update(it)

    def addused(self, number):
        self.used.add(number)

    def possible(self, allow=set()):
        return set(range(1,10)) - (self.used | (self.blocked - allow))

class Square(object):
    """ Serves as a representation for a field """
    
    ### Magic functions ###
    
    def __init__(self, id, val):
        """
        Creates a field

        Arguments:
            id : int : key in the parent list
            val : string : value entered for a field (' ' or '.' for fields to solve)
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
            self.value = int(val)
            self.case = None
            self.update()
        elif val == ' ' or val == '-':
            self.value = 0
        else:
            raise TypeError

    def __repr__(self):
        return str(self.value)

    ### Manipulation ###

    def update(self):
        """ Updates regions `possible` attribute """
        self.row_rep.addused(self.get_value())
        self.field_rep.addused(self.get_value())
        self.column_rep.addused(self.get_value())

    ### Movement ###

    def right(self, distance = 1):
        """ Returns a cell on the right of current cell """
        return self.row_rep[self.row+distance]
    
    def left(self, distance = 1):
        """ Returns a cell on the left of current cell """
        return self.row_rep[self.row-distance]

    def up(self, distance = 1):
        """ Returns a cell above the current cell """
        return self.column_rep[self.column-distance]
    
    def down(self, distance = 1):
        """ Returns a cell under the current cell """
        return self.column_rep[self.column+distance]

    ### Get functions ###

    def get_value(self):
        """ Returns the value of the cell """
        return self.value
    
def createfield():
    """ Creates representations for columns, rows and fields """
    global columns; columns = [Region() for i in range(9)]
    global rows; rows = [Region() for i in range(9)]
    global fields; fields = [Region() for i in range(9)]
    

def construct(test=False):
    """
    Returns a functioning representation of the playing field

    `test=True` assigns random values
    """
    createfield()
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
    table = construct()