from const import Square, construct
from collections import Counter
from typing import List
from functools import reduce

class Case(object):
    """ Creates a representation for possible solutions """

    ### Magic methods ###
    def __init__(self, _list, Square):
        self.list = _list
        self.sq = Square
        self.sq.case = self
        self.allowed = set()
        self.possible = set(range(1,10))

        # Tree-Consequence model
        self.assrt = 0
        self.assrt_lvl = 0

        self.update()

    def __len__(self):
        return len(self.possible)

    def __str__(self):
        return str(self.sq)

    ### Manipulation ###
    def update(self):
        """ Updates case's `possible` attribute """
        self.possible = (self.sq.row_rep.possible(allow=self.allowed) 
                         & self.sq.column_rep.possible(allow=self.allowed) 
                         & self.sq.field_rep.possible(allow=self.allowed))

    def allow(self,it):
        self.allowed.update(it)

    def final(self):
        """ Deletes the object if it's not an assertion """
        if self.assrt_lvl==-1:
            self.list.remove(self)
            self.sq.case = None

    def set_val(self, val: int):
        if self.assrt_lvl==0:
            self.sq.value = val
            self.assrt_lvl = -1
        else:
            self.assrt = val

    ### Strategies ###

    def naked_single(self):
        """ Method implements the 'naked single' strategy """
        if len(self)==1:
            val = self.possible.pop()
            self.set_val(val)
            print((self.assrt_lvl+1)*"\t",'naked single', str(self), "<-", val)
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
                    self.set_val(j)
                    print((self.assrt_lvl+1)*"\t",'hidden single', str(self), "<-", j)
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
                    print((self.assrt_lvl+1)*"\t", 'naked pair', str(self), '|', str(i))
                    self.update()
                    i.case.update()
                    return None
        return None

def gen_conseq(cases, lvl):
    cases.sort(key=len)
    is_change=True
    while is_change:
        is_change=False
        for i in cases:
            if i.assrt==0:
                i.update()
                # i.naked_pair()
                done = i.naked_single()
                if not done: done = i.hidden_single()
                if done: i.assrt_lvl = lvl
                is_change |= done
                #if done: printwhole(table)

def check_contra(cases: List[Case], level=0) -> bool:
    for i in cases:
        i.update()
        if len(i.possible)==0:
            print(level*"\t", "Contradiction at", i)
            return True 
    return False

def _layer(cases: List[Case], level: int) -> bool:
    # Generate existing consequences     
    gen_conseq(cases, level)
    if check_contra(cases, level=level):
        # Delete false assertion
        for i in cases:
            if i.assrt_lvl==level:
                i.assrt_lvl = 0
                i.assrt = 0
            i.update()
        return False
    elif len({ j for j in cases if j.assrt_lvl==0})==0:
        # Write asserted values
        for i in cases:
            i.sq.value = i.assrt 
        return True
    else:
        # Create assertion
        nextassert = min({ j for j in cases if j.assrt_lvl==0}, key=len)
        for i in nextassert.possible:
            print((nextassert.assrt_lvl+1)*"\t", f"Assert {nextassert} <- {i}; level {level+1}")
            nextassert.set_val(i)
            nextassert.assrt_lvl = level+1
            if _layer(cases, level+1):
                return True
        raise Exception("No possible value")

def layer_solve(cases: List[Case]):
    return _layer(cases, 0)

def env(table):
    """ Creates a case object for every unsolved cell in table"""
    cases = []
    for i in table:
        if i.get_value()==0:
            cases.append(Case(cases, i))
    return cases