from my_parser import parsing
import tabl as t

counter_f = 0
counter_t = 0
counter_s = 0
counter_L = 0
counter_str = 1
counter_else = 0
counter_if = 0
counter_main = 0

key = "main"
goto_key_global = ''
list_of_registr = []
list_of_float = []
simbol_table = t.get_table('progg')


def sad(part, tmp=0):
    for i in part.parts:
        tmp += 1
    if tmp == 1: return False
    else: return True


def add_to_list_of_f():
    for key in simbol_table:
        for i in simbol_table[key]:
            if i == 'float':
                for j in simbol_table[key][i]:
                    list_of_float.append(j)


def ret_type(part):
    for key in simbol_table:
        for i in simbol_table[key]:
            if ret_fact(part) in simbol_table[key][i]:
                type_var = i
                return type_var

    print("Переменная не объявлена!!!!", ret_fact(part))


def ret_class_type(type_var):
    if type_var == 'int':
        return int
    elif type_var == 'float':
        return float


def ret_fact(leaf):
    if type(leaf) != (str or int or float):
        return leaf.parts[0]
    else:
        return leaf


def ret_s(part):
    return '_s'+str(list_of_registr.index(part)+1)


def ret_f(part):
    return '_f' + str(list_of_float.index(part) + 1)


def ret_func_args(part):
    tmp_arr = []

    for fcts in part.parts:
        tmp_arr.append(ret_fact(fcts.parts[0]))
    return tmp_arr


def init_var():
    global counter_t
    counter_t += 1
    return '_t' + str(counter_t)


def init_var_f():
    global counter_f
    counter_f += 1
    try:
        a = list_of_float[counter_f]
        tmp = init_var_f()
        return tmp
    except:
        return '_f' + str(counter_f)


def init_var_s():
    global counter_s
    counter_s += 1
    return '_s' + str(counter_s)


def init_loop():
    global counter_L
    counter_L += 1
    return '_L' + str(counter_L)


def init_if():
    global counter_if
    counter_if += 1
    return 'If' + str(counter_if)


def init_else():
    global counter_else
    counter_else += 1
    return 'Else' + str(counter_else)


def init_main():
    global counter_main
    counter_main += 1
    return 'Main' + str(counter_main)


def add_new_key(type):
    global tac_dict
    if type == 'main':
        temp_key = init_main()
    elif type == 'If':
        temp_key = init_if()
    elif type == 'Else':
        temp_key = init_else()
    else:
        temp_key = init_loop()
    tac_dict[temp_key] = []
    return temp_key


def add_eqstate(leaf1, leaf2, type_var, key='main'):
    global tac_dict, goto_key_global, counter_t, list_of_float
    counter_t = 0
    if type_var == 'int':
        if leaf1 not in list_of_registr:
            list_of_registr.append(leaf1)
            tmp = '_s' + str(list_of_registr.index(leaf1)+1)
        else:
            tmp = '_s' + str(list_of_registr.index(leaf1)+1)
        if leaf2 in list_of_registr:
            tac_dict[key].append([tmp, '=', '_s' + str(list_of_registr.index(leaf2)+1)])
        elif type(leaf2) == ret_class_type(type_var) or leaf2[0] == '_' or leaf2.startswith("LCall"):
            tac_dict[key].append([tmp, '=', leaf2])
            tac_dict[key].append([leaf1, '=', tmp])
        else:
            print("Неправильные типы!!!!")

    elif type_var == 'float':
        if leaf1 not in list_of_float:
            list_of_float.append(leaf1)
            tmp = '_f' + str(list_of_float.index(leaf1)+1)
        else:
            tmp = '_f' + str(list_of_float.index(leaf1)+1)
        if leaf2 in list_of_float:
            tac_dict[key].append([tmp, '=', '_f' + str(list_of_float.index(leaf2)+1)])
        elif type(leaf2) == ret_class_type(type_var) or str(leaf2)[0] == '_':
            tac_dict[key].append([tmp, '=', leaf2])
            tac_dict[key].append([leaf1, '=', tmp])
        elif leaf2.startswith("LCall"):
            tac_dict[key].append([tmp, '=', leaf2])
        else:
            print("Неправильные типы!!!!")


def add_no_leaf(index1, oper, index2, type_var, key='main'):
    global tac_dict, goto_key_global
    if type_var == 'int':
        tmp = init_var()
    else:
        tmp = init_var_f()
    tmp_list = [tmp, '=', index1, oper, index2]
    tac_dict[key].append(tmp_list)
    return tmp


def add_right_leaf(index, oper, leaf, type_var, key='main'):
    global tac_dict, goto_key_global
    if type_var == "int":
        tmp = init_var()
    else:
        tmp = init_var_f()

    tac_dict[key].append([tmp, '=', index, oper, leaf])
    return tmp


def add_left_leaf(leaf, oper, index, type_var, key='main'):
    global tac_dict, goto_key_global
    if type_var == 'int':
        tmp = init_var()
        tac_dict[key].append([tmp, '=', leaf, oper, index])
        return tmp
    elif type_var == 'float':
        tmp = init_var_f()
        tac_dict[key].append([tmp, '=', leaf, oper, index])
        return tmp


def add_two_leaf(node, type_var, key='main'):
    global tac_dict, goto_key_global, list_of_registr
    if type_var == "int":
        tmp = init_var()
        if node.parts[0].parts[0] in list_of_registr:
            tmp_list = [tmp, '=', '_s'+str(list_of_registr.index(node.parts[0].parts[0])+1)]
            tac_dict[key].append(tmp_list)
        else:
            tac_dict[key].append([tmp, '=', node.parts[0].parts[0]])
        tmp_1 = init_var()

        if type(node.parts[2].parts[0]) == int:
            tac_dict[key].append([tmp_1, '=', tmp, node.parts[1], node.parts[2].parts[0]])
            return tmp_1
        elif node.parts[2].parts[0] in list_of_registr:
            tac_dict[key].append([tmp_1, '=', '_s'+str(list_of_registr.index(node.parts[2].parts[0])+1)])
            tmp_2 = init_var()
            goto_key_global = tmp_2
            tac_dict[key].append([tmp_2, '=', tmp, node.parts[1], tmp_1])
            return tmp_2
        else:
            print("Нет таких переменных!!!!")

    elif type_var == "float":
        tmp = init_var_f()
        if node.parts[0].parts[0] in list_of_float:
            tac_dict[key].append([tmp, '=', '_f'+str(list_of_float.index(node.parts[0].parts[0])+1)])
        else:
            tac_dict[key].append([tmp, '=', node.parts[0].parts[0]])

        tmp_1 = init_var_f()
        if node.parts[2].parts[0] in list_of_float:
            tac_dict[key].append([tmp_1, '=', '_f'+str(list_of_float.index(node.parts[2].parts[0])+1)])
        elif type(node.parts[2].parts[0]) == float:
            tac_dict[key].append([tmp_1, '=', node.parts[2].parts[0]])
        else:
            print("Не тот тип, или нет такой переменной")

        tmp_2 = init_var_f()
        tac_dict[key].append([tmp_2, '=', tmp, node.parts[1], tmp_1])
        return tmp_2


def add_exp_node(key_while, part1, oper, part2):
    global tac_dict, goto_key_global
    if part1 and part2 in list_of_registr:
        return [ret_s(part1), oper, ret_s(part2)]
    elif part1 and part2 in list_of_float:
        return [ret_f(part1), oper, ret_f(part2)]
    elif part1 in list_of_registr:
        return [ret_s(part1), oper, part2]
    else:
        print("Error\n Низя. Только 1 число. Число справа онли!")


def add_while_or_if_goto(key_after, key_before, goto_key='global', condition=None):
    if condition is not None:
        if goto_key == "while":
            tac_dict[key_after].append(["IfZ", condition[0], condition[1], condition[2], "Goto", key_before])
        else:
            tac_dict[key_after].append(["If", condition[0], condition[1], condition[2], "Goto", key_before])
    else:
        tac_dict[key_before].append(["Goto", key_after])


def add_func_call(key_after, part):
    tac_dict[key_after].append(["LCall", "_" + part.parts[0], ret_func_args(part.parts[1])])
    return "LCall _" + part.parts[0]


def add_func_node(key):
    tac_dict[key] = []


def add_func_vars(part):
    type_var = ret_type(part.parts[1])
    if type_var == 'int':
        for i in part.parts[1].parts:
            if i not in list_of_registr:
                list_of_registr.append(i)
    elif type_var == 'float':
        for i in part.parts[1].parts:
            if i not in list_of_float:
                list_of_float.append(i)


def add_ret_func(key, part):
    tac_dict[key].append(["return", part])


def add_print_node(key, part):
    tac_dict[key].append(['print', part])


def add_break(key_rec):
    tac_dict[key_rec].append(['Goto', key])


def add_continue(key_rec, key_after):
    tac_dict[key_rec].append(['Goto', key_after])


def recurs(tree, key_rec=key, key_after=''):
    global tac_dict, key
    for part in tree.parts:
        if type(part) != str and type(part) != int and type(part) != float:
            if part.type == "simple_expression":
                simpl_expr(part, key=key_rec,  key_after_1=key_after)
                continue
            if part.type == "While":
                tmp_key = while_stmt(part, key_after=key_rec, key_after_1=key_after)
                key_rec = tmp_key
                continue
            if part.type == "If\Else":
                tmp_key = if_else_stmt(part, key_into=key_rec, key_after=key_after)
                key_rec = tmp_key
                continue
            if part.type == "Function":
                func_stmt(part, key_rec)
                continue
            if part.type == "out":
                out_stmt(part, key_rec)
                continue
            if part.type == "return":
                ret_stmt(part, key_rec)
                continue
            recurs(part, key_rec, key_after)


def simpl_expr(node, type_var='', key='main',  key_after_1=''):
    global counter_str
    # type_var = "Error"
    for part in node.parts:
        if node.type == "Factor" and node.parts[0] == '\"':
            counter_str += 1
            return node.parts[1]
        if type(part) != str and type(part) != int and type(part) != float:

            if node.type == "Factor" and node.parts[0] == '(':
                variable = simpl_expr(node.parts[1], type_var, key)
                return variable

            elif part.type == "Factor" and part.parts[0] == "break":
                add_break(key)

            elif part.type == "Factor" and part.parts[0] == "continue":
                add_continue(key, key_after_1)

            elif part.type == "Func_call":
                variable = add_func_call(key, part)
                return variable

            elif part.type == "Factor" and part.parts[0] == 'return':
                if sad(part.parts[1]):
                    add_ret_func(key, simpl_expr(part.parts[1], ret_fact(part.parts[1])))
                else:
                    add_ret_func(key, ret_fact(part.parts[1].parts[0]))

            elif part.type == "eqstate":
                type_var = ret_type(part.parts[0])
                # print(type_var, '- ', part.parts[0])
                if sad(part.parts[2]):
                    add_eqstate(ret_fact(part.parts[0]), simpl_expr(part, type_var, key), type_var, key)
                else:
                    add_eqstate(ret_fact(part.parts[0]), ret_fact(part.parts[2]), type_var, key)

            elif part.type == "term" or part.type == "dvml":
                if sad(part.parts[0]) and sad(part.parts[2]):
                    variable = add_no_leaf(simpl_expr(part.parts[0], type_var, key), part.parts[1],
                                           simpl_expr(part.parts[2], type_var, key), type_var, key)
                    return variable
                elif sad(part.parts[0]):
                    variable = add_right_leaf(simpl_expr(part.parts[0], type_var, key), part.parts[1],
                                              ret_fact(part.parts[2]), type_var, key)
                    return variable
                elif sad(part.parts[2]):
                    variable = add_left_leaf(ret_fact(part.parts[0]), part.parts[1], simpl_expr(part.parts[2], type_var, key), type_var, key)
                    return variable
                else:
                    variable = add_two_leaf(part, type_var, key)
                    return variable

            elif node.type == "term" or node.type == "dvml":
                if sad(node.parts[0]) and sad(node.parts[2]):
                    variable = add_no_leaf(simpl_expr(part.parts[0], type_var, key), node.parts[1],
                                           simpl_expr(node.parts[2], type_var, key), type_var, key)
                    return variable
                elif sad(node.parts[0]):
                    variable = add_right_leaf(simpl_expr(part.parts[0], type_var, key), node.parts[1], ret_fact(node.parts[2]), type_var, key)
                    return variable
                elif sad(node.parts[2]):
                    variable = add_left_leaf(ret_fact(node.parts[0]), node.parts[1], simpl_expr(node.parts[2], type_var, key), type_var, key)
                    return variable
                else:
                    variable = add_two_leaf(node, type_var, key)
                    return variable


def while_stmt(node, key_after='main', key_after_1=''):
    global key
    key_while = add_new_key("L")
    add_while_or_if_goto(key_while, key_after)
    key_after_2 = add_new_key("L")
    for part in node.parts:
        if part.type == 'expression':
            if part.parts[1] != ('and' or 'or'):
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

                if key_after_1 != '':
                    add_while_or_if_goto(key_while, key_after_1, goto_key='while', condition=condition)
                else:
                    key_main = add_new_key("main")
                    key = key_main
                    add_while_or_if_goto(key_while, key, goto_key='while', condition=condition)
            else:
                if sad(part.parts[0].parts[0]) and sad(part.parts[2].parts[0]):
                    condition = add_exp_node(key_while,
                                             simpl_expr(part.parts[0], key=key_while),
                                             part.parts[1],
                                             simpl_expr(part.parts[2], key=key_while))
                elif sad(part.parts[0].parts[0]):
                    condition = add_exp_node(key_while,
                                             simpl_expr(part.parts[0], key=key_while),
                                             part.parts[1],
                                             ret_fact(part.parts[2].parts[0]))
                elif sad(part.parts[2].parts[0]):
                    condition = add_exp_node(key_while,
                                             ret_fact(part.parts[0].parts[0]),
                                             part.parts[1],
                                             simpl_expr(part.parts[2], key=key_while))
                else:
                    condition = add_exp_node(key_while,
                                             ret_fact(part.parts[0].parts[0]),
                                             part.parts[1],
                                             ret_fact(part.parts[2].parts[0]))

                if key_after_1 != '':
                    add_while_or_if_goto(key_while, key_after_1, goto_key='while', condition=condition)
                else:
                    key_main = add_new_key("main")
                    key = key_main
                    add_while_or_if_goto(key_while, key, goto_key='while', condition=condition)

        elif part.type == "compound_statement":
            recurs(part, key_rec=key_while, key_after=key_after_2)

    add_while_or_if_goto(key_after_2, key_while)
    add_while_or_if_goto(key_while, key_after_2)
    if key_after_1 != '':
        return key_after_1
    else:
        return key_main


def if_else_stmt(node, key_into='main', key_after=''):
    global key
    second = False
    key_if = add_new_key('If')
    for part in node.parts:
        if part.type == 'expression':
            if sad(part.parts[0]) and sad(part.parts[2]):
                condition = add_exp_node(key_into,
                                         simpl_expr(part.parts[0], key=key_into),
                                         part.parts[1],
                                         simpl_expr(part.parts[2], key=key_into))
            elif sad(part.parts[0]):
                condition = add_exp_node(key_into,
                                         simpl_expr(part.parts[0], key=key_into),
                                         part.parts[1],
                                         ret_fact(part.parts[2].parts[0]))
            elif sad(part.parts[2]):
                condition = add_exp_node(key_into,
                                         ret_fact(part.parts[0].parts[0]),
                                         part.parts[1],
                                         simpl_expr(part.parts[2], key=key_into))
            else:
                condition = add_exp_node(key_into,
                                         ret_fact(part.parts[0].parts[0]),
                                         part.parts[1],
                                         ret_fact(part.parts[2].parts[0]))
            add_while_or_if_goto(key_into, key_if, goto_key='if', condition=condition)

        elif part.type == "compound_statement" and not second:
            recurs(part, key_rec=key_if, key_after=key_after)

    if key_after != '':
        add_while_or_if_goto(key_after, key_if)
    else:
        key_main = add_new_key('main')
        key = key_main
        add_while_or_if_goto(key, key_if)

    return key


def func_stmt(node, key):
    key_func = ''
    for part in node.parts:
        if part.type == "Function_head":
            key_func = part.parts[1]
            add_func_node(key_func)
            add_func_vars(part.parts[2])
        elif part.type == "compound_statement":
            recurs(part, key_func)
    key = key_func


def ret_stmt(node, key):
    if sad(node.parts[0]):
        add_ret_func(key, simpl_expr(node.parts[0]))
    else:
        add_ret_func(key, ret_fact(node.parts[0].parts[0]))


def out_stmt(node, key):
    if sad(node.parts[1]):
        add_print_node(key, simpl_expr(node.parts[1]))
    else:
        add_print_node(key, ret_fact(node.parts[1]))


def gen_tac(init_prog):
    global tac_dict
    with open(init_prog, 'r') as f:
        s = f.read()

    tac_dict = {'main': []}

    tree = parsing().parse(s)
    add_to_list_of_f()
    recurs(tree)

    return tac_dict


if __name__ == '__main__':
    with open('progg', 'r') as f:
        s = f.read()

    simbol_table = t.get_table('progg')

    tac_dict = {'main': []}

    tree = parsing().parse(s)
    print(tree)
    add_to_list_of_f()
    print(list_of_float)
    recurs(tree)

    for key in tac_dict:
        print(key, ':')
        for i in tac_dict[key]:
            print('\t', i)