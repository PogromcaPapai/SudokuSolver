from const import Square, construct


class Case(object):

    ### Magic methods ###
    def __init__(self, list, Square):
        self.list = list
        self.sq = Square
        self.sq.case = self
        self.update()

    def __len__(self):
        return len(self.possible)

    ### Manipulation ###
    def update(self):
        """ Updates case's `possible` attribute """
        self.possible = self.sq.row_rep.possible & self.sq.column_rep.possible & self.sq.field_rep.possible

    def final(self):
        self.list.remove(self)
        del self

    ### Strategies ###

    def naked_single(self):
        if len(self)==1:
            self.sq.value = self.possible.pop()
            print('koniec')
            self.sq.update()
            self.final()
            return True
        else:
            return False
  
        
def env(table):
    cases = []
    for i in table:
        if i.get_value()==0:
            cases.append(Case(cases, i))
    return cases