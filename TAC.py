from my_parser import parsing

counter_t = 0
counter_L = 0
key = "Main"
goto_key_global = ''


def sad(part, tmp=0):
    for i in part.parts:
        tmp += 1
    if tmp == 1: return False
    else: return True


def ret_fact(leaf):
    return leaf.parts[0]


def ret_func_args(part):
    tmp_arr = []
    for fcts in part.parts:
        tmp_arr.append(ret_fact(fcts.parts[0]))
    return tmp_arr


def init_var():
    global counter_t
    counter_t += 1
    return '_t' + str(counter_t)


def init_func():
    global counter_L
    counter_L += 1
    return '_L' + str(counter_L)


def add_new_key():
    global tac_dict
    temp_key_l = init_func()
    tac_dict[temp_key_l] = {}
    return temp_key_l


def add_eqstate(leaf1, leaf2, key='Main'):
    global tac_dict, goto_key_global
    goto_key_global = leaf1
    tac_dict[key][leaf1] = leaf2


def add_no_leaf(index1, oper, index2, key='Main'):
    global tac_dict, goto_key_global
    tmp = init_var()
    goto_key_global = tmp
    tac_dict[key][tmp] = [index1, oper, index2]
    return tmp


def add_right_leaf(index, oper, leaf, key='Main'):
    global tac_dict, goto_key_global
    tmp = init_var()
    goto_key_global = tmp
    tac_dict[key][tmp] = [index, oper, leaf]
    return tmp


def add_left_leaf(leaf, oper, index, key='Main'):
    global tac_dict, goto_key_global
    tmp = init_var()
    goto_key_global = tmp
    tac_dict[key][tmp] = [leaf, oper, index]
    return tmp


def add_two_leaf(node, key='Main'):
    global tac_dict, goto_key_global
    tmp_arr = []
    tmp = init_var()
    goto_key_global = tmp
    for leaf in node.parts:
        if type(leaf) != str: tmp_arr.append(leaf.parts[0])
        else: tmp_arr.append(leaf)
    tac_dict[key][tmp] = tmp_arr
    return tmp


def add_exp_node(key_while, part1, oper, part2):
    global tac_dict, goto_key_global
    tmp = init_var()
    goto_key_global = tmp
    tac_dict[key_while][tmp] = [part1, oper, part2]
    return tmp


def add_while_or_if_goto(key_after, key_before, goto_key='global', condition=None):
    tmp = init_var()
    if condition is not None:
        tac_dict[key_after][tmp] = ["IfZ", condition, "Goto", key_before, goto_key]
    else:
        tac_dict[key_before][tmp] = ["Goto", key_after, goto_key]


def add_func_call(key_after, part):
    tmp = init_var()
    tac_dict[key_after][tmp] = ["LCall", "_" + part.parts[0], ret_func_args(part.parts[1])]
    return tmp


def add_func_node(key):
    tac_dict[key] = {}
    tac_dict[key]['_opt_'] = "BeginFunc"


def add_ret_func(key, part):
    tac_dict[key]['ret_opt'] = ["return", part]


def add_print_node(key, part):
    tac_dict[key]['print'] = part


def recurs(tree, key='Main'):
    global tac_dict
    for part in tree.parts:
        if type(part) != str and type(part) != int:
            if part.type == "simple_expression":
                simpl_expr(part, key)
                continue
            if part.type == "While":
                while_stmt(part, key_after=key)
                continue
            if part.type == "If\Else":
                if_else_stmt(part, key)
                continue
            if part.type == "Function":
                func_stmt(part, key)
                continue
            if part.type == "out":
                add_print_node(key, simpl_expr(part))
                continue
            if part.type == "return":
                ret_stmt(part, key)
                continue
            recurs(part, key)


def simpl_expr(node, key='Main'):
    for part in node.parts:
        if type(part) != str and type(part) != int:

            if node.type == "Factor" and node.parts[0] == '(':
                variable = simpl_expr(node.parts[1], key)
                return variable

            elif part.type == "Func_call":
                variable = add_func_call(key, part)
                return variable

            elif part.type == "Factor" and part.parts[0] == '\"':
                return part.parts[1]

            elif part.type == "Factor" and part.parts[0] == 'return':
                if sad(part.parts[1]):
                    add_ret_func(key, simpl_expr(part.parts[1]))
                else:
                    add_ret_func(key, ret_fact(part.parts[1].parts[0]))

            elif part.type == "eqstate":
                if sad(part.parts[2]):
                    add_eqstate(ret_fact(part.parts[0]), simpl_expr(part, key), key)
                else:
                    add_eqstate(ret_fact(part.parts[0]), ret_fact(part.parts[2]), key)

            elif part.type == "term" or part.type == "dvml":
                if sad(part.parts[0]) and sad(part.parts[2]):
                    variable = add_no_leaf(simpl_expr(part.parts[0], key), part.parts[1], simpl_expr(part.parts[2], key), key)
                    return variable
                elif sad(part.parts[0]):
                    variable = add_right_leaf(simpl_expr(part.parts[0], key), part.parts[1], ret_fact(part.parts[2]), key)
                    return variable
                elif sad(part.parts[2]):
                    variable = add_left_leaf(ret_fact(part.parts[0]), part.parts[1], simpl_expr(part.parts[2], key), key)
                    return variable
                else:
                    variable = add_two_leaf(part, key)
                    return variable

            elif node.type == "term" or node.type == "dvml":
                if sad(node.parts[0]) and sad(node.parts[2]):
                    variable = add_no_leaf(simpl_expr(part.parts[0], key), node.parts[1], simpl_expr(node.parts[2], key), key)
                    return variable
                elif sad(node.parts[0]):
                    variable = add_right_leaf(simpl_expr(part.parts[0], key), node.parts[1], ret_fact(node.parts[2]), key)
                    return variable
                elif sad(node.parts[2]):
                    variable = add_left_leaf(ret_fact(node.parts[0]), node.parts[1], simpl_expr(node.parts[2], key), key)
                    return variable
                else:
                    variable = add_two_leaf(node, key)
                    return variable


def while_stmt(node, key_after='Main'):
    key_while = add_new_key()
    add_while_or_if_goto(key_while, key_after)
    for part in node.parts:
        if part.type == 'expression':
            goto_key = goto_key_global
            if sad(part.parts[0]) and sad(part.parts[2]):
                condition = add_exp_node(key_while,
                                         simpl_expr(part.parts[0], key=key_while),
                                         part.parts[1],
                                         simpl_expr(part.parts[2], key=key_while))
            elif sad(part.parts[0]):
                condition = add_exp_node(key_while,
                                         simpl_expr(part.parts[0], key=key_while),
                                         part.parts[1],
                                         ret_fact(part.parts[2].parts[0]))
            elif sad(part.parts[2]):
                condition = add_exp_node(key_while,
                                         ret_fact(part.parts[0].parts[0]),
                                         part.parts[1],
                                         simpl_expr(part.parts[2], key=key_while))
            else:
                condition = add_exp_node(key_while,
                                         ret_fact(part.parts[0].parts[0]),
                                         part.parts[1],
                                         ret_fact(part.parts[2].parts[0]))

            add_while_or_if_goto(key_while, key_after, goto_key=goto_key, condition=condition)

        elif part.type == "compound_statement":

            recurs(part, key=key_while)

    add_while_or_if_goto(key_while, key_while)


def if_else_stmt(node, key='Main'):
    second = False
    key_else = add_new_key()
    for part in node.parts:
        if part.type == 'expression':
            if sad(part.parts[0]) and sad(part.parts[2]):
                condition = add_exp_node(key,
                                         simpl_expr(part.parts[0], key=key),
                                         part.parts[1],
                                         simpl_expr(part.parts[2], key=key))
            elif sad(part.parts[0]):
                condition = add_exp_node(key,
                                         simpl_expr(part.parts[0], key=key),
                                         part.parts[1],
                                         ret_fact(part.parts[2].parts[0]))
            elif sad(part.parts[2]):
                condition = add_exp_node(key,
                                         ret_fact(part.parts[0].parts[0]),
                                         part.parts[1],
                                         simpl_expr(part.parts[2], key=key))
            else:
                condition = add_exp_node(key,
                                         ret_fact(part.parts[0].parts[0]),
                                         part.parts[1],
                                         ret_fact(part.parts[2].parts[0]))

            add_while_or_if_goto(key, key_else, condition=condition)

        elif part.type == "compound_statement" and not second:
            recurs(part)
            second = True

        elif part.type == "compound_statement" and second:
            goto_key = goto_key_global
            recurs(part, key=key_else)
            add_while_or_if_goto(key, key_else, goto_key=goto_key)


def func_stmt(node, key):
    key_func = ''
    for part in node.parts:
        if part.type == "Function_head":
            key_func = part.parts[1]
            add_func_node(key_func)
        elif part.type == "compound_statement":
            recurs(part, key=key_func)


def ret_stmt(node, key):
    if sad(node.parts[0]):
        add_ret_func(key, simpl_expr(node.parts[0]))
    else:
        add_ret_func(key, ret_fact(node.parts[0].parts[0]))

if __name__ == '__main__':
    with open('progg', 'r') as f:
        s = f.read()

    tac_dict = {'Main': {}}

    tree = parsing().parse(s)
    print(tree)

    recurs(tree)

    for key in tac_dict:
        print(key, ':')
        for i in tac_dict[key]:
            print('\t', i, '= ', tac_dict[key][i])