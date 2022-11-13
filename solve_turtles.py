"""Solve the turtles' game."""

from collections.abc import Sequence
import typing
import os
import os.path
import cplex
from cplex_errors_mgmt import CODES, error_str
from utils import var_name, border_name
from data_structures import Card, CardPool, vCard, ExtMap
from GUI import card_selection, select_solve_mode, final_pattern


DIR_CARDS = 'cards'


def get_full_list(dir=DIR_CARDS) -> typing.Tuple[Card]:
    res = []
    for entry in os.listdir(dir):
        res.append(Card.from_file(os.path.join(dir, entry)))
    return res


def modelize(rot_cards:typing.List[CardPool], pattern:map):
    var_dict = {}
    cp = cplex.Cplex()
    for key in pattern:
        key_cards = []
        for rc in rot_cards:
            for c in rc:
                v_name = var_name(c, key)
                key_cards.append(v_name)
                var_dict[v_name] = c
                cp.variables.add(types=[cp.variables.type.binary], names=[v_name])

        cp.linear_constraints.add(
            lin_expr=[cplex.SparsePair(ind=key_cards, val=len(key_cards)*[1])],
            senses=['E'],
            rhs=[1],
            names=['c_' + str(key)]
        )
    
    for rc in rot_cards:
        key_cards=[]
        for c in rc:
            for key in pattern:
                key_cards.append(var_name(c, key))
        cp.linear_constraints.add(
            lin_expr=[cplex.SparsePair(ind=key_cards, val=len(key_cards)*[1])],
            senses=['L'], # ou 'E' si nb exact de cartes
            rhs=[rc.number],
            names=['c_' + str(rc)]
        )
    
    border_dict = {}
    for key1 in pattern:
        for key2 in pattern.neighb(key1):
            const_name = border_name(key1, key2)
            if not(border_dict.get(const_name, False)):
                key1_cards = []
                key2_cards = []
                for rc in rot_cards:
                    key1_cards += [var_name(c, key1) for c in rc]
                    key2_cards += [var_name(c, key2) for c in rc]
                orient = (key2[0]-key1[0], key2[1]-key1[1])
                inv_orient = (-orient[0], -orient[1])
                key1_val = [var_dict[name][orient] for name in key1_cards]
                key2_val = [var_dict[name][inv_orient] for name in key2_cards]
                cp.linear_constraints.add(
                    lin_expr=[cplex.SparsePair(ind=key1_cards+key2_cards, val=key1_val+key2_val)],
                    senses=['E'],
                    rhs=[0],
                    names=[const_name]
                )
                # if const_name == border_name((0,0),(0,1)):
                #    print(key1_cards)
                #    print(key2_cards)
                #    print(key1_val)
                #    print(key2_val)
                #    print("\n\n")
                border_dict[const_name] = True
    return cp, var_dict


def full_solve(): # Next step : choosing the number of each card and reducing the number of variables by taking symmetries into account
    subset = card_selection(get_full_list())
    pattern = ExtMap(select_solve_mode(len(subset)))
    rot_cards = [CardPool(c) for c in subset]
    cp, var_dict = modelize(rot_cards, pattern)
    cp.solve()
    rcode = cp.solution.get_status()
    print(rcode)
    print(cp.solution.get_status_string())
    if (
        rcode != CODES['MIP_OPTIMAL']
        and rcode != CODES['MIP_TOL_OPTIMAL']
        and rcode != CODES['MIP_OPTIMAL_POPULATED']
        and rcode != CODES['MIP_TOL_OPTIMAL_POPULATED']
        and rcode != CODES['OPTIMAL']
    ):
        pre_str = "Oops ! Something went wrong when searching for a solution : "
        cplex_str_error = cp.solution.get_status_string()
        print(pre_str + error_str(rcode) + " -> " + cplex_str_error)
        return
    
    var_name_list = [v_name for v_name in cp.variables.get_names() \
        if cp.solution.get_values(v_name) != 0]
    final_pic = final_pattern(var_name_list, var_dict)
    final_pic.show()


if __name__ == '__main__':
    full_solve()