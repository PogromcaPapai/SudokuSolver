from const import Square, construct
from collections import Counter

class Case(object):
    """ Creates a representation for possible solutions """

    ### Magic methods ###
    def __init__(self, list, Square):
        self.list = list
        self.sq = Square
        self.sq.case = self
        self.allowed = set()
        self.update()

    def __len__(self):
        return len(self.possible)

    ### Manipulation ###
    def update(self):
        """ Updates case's `possible` attribute """
        self.possible = (self.sq.row_rep.possible(allow=self.allowed) 
                         & self.sq.column_rep.possible(allow=self.allowed) 
                         & self.sq.field_rep.possible(allow=self.allowed))

    def allow(self,it):
        self.allowed.update(it)


    def final(self):
        """ Deletes the object """
        self.list.remove(self)
        self.sq.case = None
        del self

    ### Strategies ###

    def naked_single(self):
        """ Method implements the 'naked single' strategy """
        if len(self)==1:
            self.sq.value = self.possible.pop()
            print('naked single', self.sq.row, self.sq.column)
            self.sq.update()
            self.final()
            return True
        else:
            return False
    
    def hidden_single(self):
        """ Method implements the 'hidden single' strategy """
        for i in [self.sq.row_rep, self.sq.column_rep, self.sq.field_rep]:
            count = Counter()
            for k in i:
                try:
                    count = count + Counter(k.case.possible)
                except AttributeError:
                    count = count + Counter([k.get_value()])
            for j in self.possible:
                if count[j]==1:
                    self.sq.value = j
                    print('hidden single', self.sq.row, self.sq.column)
                    self.sq.update()
                    self.final()
                    return True
        return False

    def naked_pair(self):
        """ Method implements the 'naked pair' strategy """   
        if len(self)==2:
            checked = self.sq.row_rep.squares+self.sq.column_rep.squares+self.sq.field_rep.squares
            for i in set(checked):
                if i.case != None and self.possible==i.case.possible and self.sq!=i:
                    if i.field_rep == self.sq.field_rep:
                        i.case.allow(self.possible)
                        self.allow(self.possible)
                        i.field_rep.block(self.possible)
                    if i.row_rep == self.sq.row_rep:
                        i.case.allow(self.possible)
                        self.allow(self.possible)
                        i.row_rep.block(self.possible)
                    elif i.column_rep == self.sq.column_rep:
                        i.case.allow(self.possible)
                        self.allow(self.possible)
                        i.column_rep.block(self.possible)
                    print('naked pair', self.sq.row, self.sq.column, '|', i.row, i.column)
                    self.update()
                    i.case.update()
                    return None
        return None

def env(table):
    """ Creates a case object for every unsolved cell in table"""
    cases = []
    for i in table:
        if i.get_value()==0:
            cases.append(Case(cases, i))
    return cases