from const import Square, construct
from collections import Counter
from typing import List
from functools import reduce


class Case(object):
    """ Creates a representation for possible solutions """

    ### Magic methods ###
    def __init__(self, _list: list, square: Square):
        self.list = _list
        self.sq = square
        self.sq.case = self
        self.possible = set(range(1, 10))

        # Tree-Consequence model
        self.assrt = 0
        self.assrt_lvl = 0

        self.update()

    def __len__(self):
        return len(self.possible)

    def __str__(self):
        return str(self.sq)

    def __repr__(self):
        return str(self.sq)

    ### Manipulation ###
    def update(self):
        """ Updates case's `possible` attribute """
        unused = (self.sq.row_rep.possible()
                  & self.sq.column_rep.possible()
                  & self.sq.field_rep.possible())
        self.possible = unused | ({self.sq.get_value()} - {0})
        return self.possible

    def final(self):
        """ Deletes the object if it's not an assertion """
        if self.assrt_lvl == -1:
            self.list.remove(self)
            self.sq.case = None

    def set_val(self, val: int, lvl: int):
        if lvl == 0:
            self.sq.value = val
            self.assrt_lvl = -1
        else:
            self.assrt = val
            self.assrt_lvl = lvl

    ### Strategies ###

    def naked_single(self, lvl: int):
        """ Method implements the 'naked single' strategy """
        if len(self) == 1:
            val = self.possible.pop()
            self.possible.add(val)
            self.set_val(val, lvl)
            print((self.assrt_lvl)*"\t", 'naked single', str(self), "<-", val)
            self.final()
            return True
        else:
            return False

    def hidden_single(self, lvl: int):
        """ Method implements the 'hidden single' strategy """
        for i in [self.sq.row_rep, self.sq.column_rep, self.sq.field_rep]:
            count = Counter()
            for k in i:
                try:
                    count = count + Counter(k.case.possible)
                except AttributeError:
                    count = count + Counter([k.get_value()])
            for j in self.possible:
                if count[j] == 1:
                    self.set_val(j, lvl)
                    print((self.assrt_lvl)*"\t",
                          'hidden single', str(self), "<-", j)
                    self.final()
                    return True
        return False

### Tree-Consequence Model ###


def gen_conseq(cases, lvl: int):
    """ Generates consequences of assertions and values """
    cases.sort(key=len)
    is_change = True
    while is_change:
        is_change = False
        for i in cases:
            if i.assrt == 0:
                i.update()
                # i.naked_pair()
                done = i.naked_single(lvl)
                if not done:
                    done = i.hidden_single(lvl)
                is_change |= done
                #if done: printwhole(table)


def check_contra(cases: List[Case], tab_level=0) -> bool:
    """ Checks case list for contradisctions """
    for i in cases:
        if len(i.update()) == 0:
            print(tab_level*"\t", "Contradiction at", i)
            return True
    return False


def _layer(cases: List[Case], level: int) -> bool:
    """ USE `self.layer_solve` INSTEAD """

    # Generate existing consequences
    gen_conseq(cases, level)
    if check_contra(cases, tab_level=level):
        # Delete false assertion and consequences
        return False
    elif len({j for j in cases if j.assrt_lvl == 0}) == 0:
        # Write asserted values
        for i in cases:
            i.sq.value = i.assrt
        return True
    else:
        # Create assertion
        nextassert = min({j for j in cases if j.assrt_lvl == 0}, key=len)
        for i in nextassert.possible.copy():
            print(level*"\t", f"Assert {nextassert} <- {i}; level {level+1}")
            nextassert.set_val(i, level+1)
            if _layer(cases, level+1):
                return True
            else:
                for i in cases:
                    if i.assrt_lvl > level:
                        i.assrt_lvl = 0
                        i.assrt = 0
                for i in cases:
                    i.update()
        return False


def layer_solve(cases: List[Case]) -> bool:
    """ Uses assertions and their consequences to solve a sudoku """
    _layer(cases, 0)

### Misc ###


def env(table) -> List[Case]:
    """ Creates a case object for every unsolved cell in table"""
    cases = []
    for i in table:
        if i.get_value() == 0:
            cases.append(Case(cases, i))
    return cases
