import TAC
import tabl

type_var = ''
MIPS_CODE = {'.data': [], '.text': {}}
counter_str = 1
counter_a = -1
list_of_a = []


def count_str():
    global counter_str
    counter_str += 1
    return counter_str


def count_a():
    global counter_a
    counter_a += 1
    return counter_a


def init_text_main(tac_dict):
    global type_var
    for key in tac_dict:
        MIPS_CODE['.text'][key] = []
        if len(tac_dict[key]) == 0:
            MIPS_CODE['.text'][key].append('b Main' + str(TAC.counter_main))
        for part in tac_dict[key]:
            # print(part[0])
            if len(part) > 3 and part[3] == '+':
                if type(part[2]) != (int or float) and type(part[4]) == int:
                    MIPS_CODE['.text'][key].\
                        append('addi $' + str(part[0][1:]) + ', $' + str(part[2][1:]) + ', ' + str(part[4]))

                elif type(part[2]) == int and type(part[4]) != (int or float):
                    MIPS_CODE['.text'][key].\
                        append('addi $' + str(part[0][1:]) + ', $' + str(part[4][1:]) + ', ' + str(part[2]))

                elif part[0][0:2] == '_f' and part[2][0:2] == '_f' and part[4][0:2] == '_f':
                    MIPS_CODE['.text'][key]. \
                        append('add.s $' + str(part[0][1:]) + ', $' + str(part[2][1:]) + ', $' + str(part[4][1:]))

                else:
                    MIPS_CODE['.text'][key]. \
                        append('addu $' + str(part[0][1:]) + ', $' + str(part[2][1:]) + ', $' + str(part[4][1:]))

            elif len(part) > 3 and part[3] == '-':
                if type(part[2]) != (int or float) and type(part[4]) == (int or float):
                    MIPS_CODE['.text'][key]. \
                        append('subi $' + str(part[0][1:]) + ', $' + str(part[2][1:]) + ', ' + str(part[4]))

                elif type(part[2]) == (int or float) and type(part[4]) != (int or float):
                    MIPS_CODE['.text'][key]. \
                        append('subi $' + str(part[0][1:]) + ', $' + str(part[4][1:]) + ', ' + str(part[2]))

                elif part[0][0:2] == '_f' and part[2][0:2] == '_f' and part[4][0:2] == '_f':
                    MIPS_CODE['.text'][key]. \
                        append('sub.s $' + str(part[0][1:]) + ', $' + str(part[2][1:]) + ', $' + str(part[4][1:]))

                else:
                    MIPS_CODE['.text'][key]. \
                        append('subu $' + str(part[0][1:]) + ', $' + str(part[2][1:]) + ', $' + str(part[4][1:]))

            elif len(part) > 3 and part[3] == '*':
                if type(part[2]) != (int or float) and type(part[4]) == (int or float):
                    MIPS_CODE['.text'][key]. \
                        append('mul $' + str(part[0][1:]) + ', $' + str(part[2][1:]) + ', ' + str(part[4]))

                elif type(part[2]) == (int or float) and type(part[4]) != (int or float):
                    MIPS_CODE['.text'][key]. \
                        append('mul $' + str(part[0][1:]) + ', $' + str(part[4][1:]) + ', ' + str(part[2]))

                elif part[0][0:2] == '_f' and part[2][0:2] == '_f' and part[4][0:2] == '_f':
                    MIPS_CODE['.text'][key]. \
                        append('mul.s $' + str(part[0][1:]) + ', $' + str(part[2][1:]) + ', $' + str(part[4][1:]))

                else:
                    MIPS_CODE['.text'][key]. \
                        append('mul $' + str(part[0][1:]) + ', $' + str(part[2][1:]) + ', $' + str(part[4][1:]))

            elif len(part) > 3 and part[3] == '/':
                if type(part[2]) != (int or float) and type(part[4]) == (int or float):
                    MIPS_CODE['.text'][key].\
                        append('div $' + str(part[0][1:]) + ', $' + str(part[2][1:]) + ', ' + str(part[4]))

                elif type(part[2]) == (int or float) and type(part[4]) != (int or float):
                    MIPS_CODE['.text'][key]. \
                        append('div $' + str(part[0][1:]) + ', $' + str(part[4][1:]) + ', ' + str(part[2]))

                elif part[0][0:2] == '_f' and part[2][0:2] == '_f' and part[4][0:2] == '_f':
                    MIPS_CODE['.text'][key]. \
                        append('div.s $' + str(part[0][1:]) + ', $' + str(part[2][1:]) + ', $' + str(part[4][1:]))

                else:
                    MIPS_CODE['.text'][key]. \
                        append('div $' + str(part[0][1:]) + ', $' + str(part[2][1:]) + ', $' + str(part[4][1:]))

            elif part[0] == 'print':
                _t = ""
                type_var = "str"
                for i in simbol_table['global']:
                    if part[1] in simbol_table['global'][i]:
                        type_var = i
                        break

                for i in tac_dict[key]:
                    if part[1] in i and type_var!='str':
                        _t = i[2][1:]
                        break

                if type_var == 'int' and _t != "":
                    MIPS_CODE['.text'][key].\
                        append('move $a0, $' + _t + '\n\tli $v0 1\n\tsyscall\n')

                    MIPS_CODE['.text'][key]. \
                        append('la $a0, string1\n\tli $v0 4\n\tsyscall\n')

                elif type_var == 'float' and _t != "":
                    MIPS_CODE['.text'][key].\
                        append('mov.s $f12, $' + _t + '\n\tli $v0 2\n\tsyscall\n')
                    MIPS_CODE['.text'][key]. \
                        append('la $a0, string1\n\tli $v0 4\n\tsyscall\n')

                elif type_var == 'str':
                    MIPS_CODE['.data']. \
                        append('\tstring' + str(count_str()) + ': .asciiz \"' + str(part[1]) + '\"')
                    MIPS_CODE['.text'][key]. \
                        append('la $a0, string'+str(counter_str)+'\n\tli $v0 4\n\tsyscall\n')
                    MIPS_CODE['.text'][key]. \
                        append('la $a0, string1\n\tli $v0 4\n\tsyscall\n')

            elif part[0] == 'If':
                if type(part[1]) != (int or float) and type(part[3]) == (int or float):
                    if part[2] == '==':
                        MIPS_CODE['.text'][key]. \
                            append('beq $' + str(part[1][1:]) + ', ' + str(part[3]) + ', ' + str(part[5]))
                    elif part[2] == '<':
                        MIPS_CODE['.text'][key]. \
                            append('blt $' + str(part[1][1:]) + ', ' + str(part[3]) + ', ' + str(part[5]))
                    elif part[2] == '<=':
                        MIPS_CODE['.text'][key]. \
                            append('ble $' + str(part[1][1:]) + ', ' + str(part[3]) + ', ' + str(part[5]))
                    elif part[2] == '>':
                        MIPS_CODE['.text'][key]. \
                            append('bgt $' + str(part[1][1:]) + ', ' + str(part[3]) + ', ' + str(part[5]))
                    elif part[2] == '>=':
                        MIPS_CODE['.text'][key]. \
                            append('bge $' + str(part[1][1:]) + ', ' + str(part[3]) + ', ' + str(part[5]))
                    elif part[2] == '!=':
                        MIPS_CODE['.text'][key]. \
                            append('bne $' + str(part[1][1:]) + ', ' + str(part[3]) + ', ' + str(part[5]))

                else:
                    if part[2] == '==':
                        MIPS_CODE['.text'][key]. \
                            append('beq $' + str(part[1][1:]) + ', $' + str(part[3][1:]) + ', ' + str(part[5]))
                    elif part[2] == '<':
                        MIPS_CODE['.text'][key]. \
                            append('blt $' + str(part[1][1:]) + ', $' + str(part[3][1:]) + ', ' + str(part[5]))
                    elif part[2] == '<=':
                        MIPS_CODE['.text'][key]. \
                            append('ble $' + str(part[1][1:]) + ', $' + str(part[3][1:]) + ', ' + str(part[5]))
                    elif part[2] == '>':
                        MIPS_CODE['.text'][key]. \
                            append('bgt $' + str(part[1][1:]) + ', $' + str(part[3][1:]) + ', ' + str(part[5]))
                    elif part[2] == '>=':
                        MIPS_CODE['.text'][key]. \
                            append('bge $' + str(part[1][1:]) + ', $' + str(part[3][1:]) + ', ' + str(part[5]))
                    elif part[2] == '!=':
                        MIPS_CODE['.text'][key]. \
                            append('bne $' + str(part[1][1:]) + ', $' + str(part[3][1:]) + ', ' + str(part[5]))
                    elif part[2] == 'and':
                        MIPS_CODE['.text'][key]. \
                            append('and $t' + str(TAC.counter_t) + ', $' + str(part[1][1:]) + ', $' + str(part[3][1:]) +
                                   '\n\tbeq $' + str(TAC.counter_t) + ', 1, ' + str(part[5]))
                    elif part[2] == 'or':
                        MIPS_CODE['.text'][key]. \
                            append('or $t' + str(TAC.counter_t) + ', $' + str(part[1][1:]) + ', $' + str(part[3][1:]) +
                                   '\n\tbeq $' + str(TAC.counter_t) + ', 1, ' + str(part[5]))

            elif part[0] == 'IfZ':
                if type(part[1]) != (int or float) and type(part[3]) == (int or float):
                    if part[2] == '==':
                        MIPS_CODE['.text'][key]. \
                            append('bne $' + str(part[1][1:]) + ', ' + str(part[3]) + ', ' + str(part[5]))
                    elif part[2] == '<':
                        MIPS_CODE['.text'][key]. \
                            append('bge $' + str(part[1][1:]) + ', ' + str(part[3]) + ', ' + str(part[5]))
                    elif part[2] == '<=':
                        MIPS_CODE['.text'][key]. \
                            append('bgt $' + str(part[1][1:]) + ', ' + str(part[3]) + ', ' + str(part[5]))
                    elif part[2] == '>':
                        MIPS_CODE['.text'][key]. \
                            append('ble $' + str(part[1][1:]) + ', ' + str(part[3]) + ', ' + str(part[5]))
                    elif part[2] == '>=':
                        MIPS_CODE['.text'][key]. \
                            append('blt $' + str(part[1][1:]) + ', ' + str(part[3]) + ', ' + str(part[5]))
                    elif part[2] == '!=':
                        MIPS_CODE['.text'][key]. \
                            append('beq $' + str(part[1][1:]) + ', ' + str(part[3]) + ', ' + str(part[5]))

                else:
                    if part[2] == '==':
                        MIPS_CODE['.text'][key]. \
                            append('bne $' + str(part[1][1:]) + ', $' + str(part[3][1:]) + ', ' + str(part[5]))
                    elif part[2] == '<':
                        MIPS_CODE['.text'][key]. \
                            append('bge $' + str(part[1][1:]) + ', $' + str(part[3][1:]) + ', ' + str(part[5]))
                    elif part[2] == '<=':
                        MIPS_CODE['.text'][key]. \
                            append('bgt $' + str(part[1][1:]) + ', $' + str(part[3][1:]) + ', ' + str(part[5]))
                    elif part[2] == '>':
                        MIPS_CODE['.text'][key]. \
                            append('ble $' + str(part[1][1:]) + ', $' + str(part[3][1:]) + ', ' + str(part[5]))
                    elif part[2] == '>=':
                        MIPS_CODE['.text'][key]. \
                            append('blt $' + str(part[1][1:]) + ', $' + str(part[3][1:]) + ', ' + str(part[5]))
                    elif part[2] == '!=':
                        MIPS_CODE['.text'][key]. \
                            append('beq $' + str(part[1][1:]) + ', $' + str(part[3][1:]) + ', ' + str(part[5]))
                    elif part[2] == 'and':
                        MIPS_CODE['.text'][key]. \
                            append('and $t' + str(TAC.counter_t) + ', $' + str(part[1][1:]) + ', $' + str(part[3][1:]) +
                                   '\n\tbeq $' + str(TAC.counter_t) + ', 1, ' + str(part[5]))
                    elif part[2] == 'or':
                        MIPS_CODE['.text'][key]. \
                            append('or $t' + str(TAC.counter_t) + ', $' + str(part[1][1:]) + ', $' + str(part[3][1:]) +
                                   '\n\tbeq $' + str(TAC.counter_t) + ', 1, ' + str(part[5]))

            elif part[0] == 'LCall':
                for i in simbol_table[part[1][1:]]:
                    for j in simbol_table[part[1][1:]][i]:
                        list_of_a.append(j)

                for i in part[2]:
                    if type(i) != (int or float):
                        if i in (TAC.list_of_registr or TAC.list_of_float):
                            MIPS_CODE['.text'][key].\
                                append('move $a' + str(count_a()) + ', $s' + str(TAC.list_of_registr.index(i)+1))
                    else:
                        MIPS_CODE['.text'][key]. \
                            append('li $a' + str(count_a()) + ', ' + str(i))
                MIPS_CODE['.text'][key]. \
                    append('jal ' + str(part[1][1:]))

            elif part[0] == 'return':
                # print(list_of_a)
                MIPS_CODE['.text'][key]\
                    .append('move $a'+str(list_of_a.index(part[1]))+', $s'+str(TAC.list_of_registr.index(part[1])+1))
                MIPS_CODE['.text'][key]. \
                        append('jr $ra')


            elif part[0] == 'Goto':
                MIPS_CODE['.text'][key].append('b ' + str(part[1]))

            elif len(part) == 3:
                if part[0][0:2] == "_t" and type(part[2]) == int:
                    MIPS_CODE['.text'][key].\
                        append('li $' + str(part[0][1:]) + ', ' + str(part[2]))
                elif part[0][0:2] == "_f" and type(part[2]) == float:
                    MIPS_CODE['.text'][key].\
                        append('li.s $' + str(part[0][1:]) + ', ' + str(part[2]))
                elif part[0][0:2] == "_t" and type(part[2]) != int:
                    MIPS_CODE['.text'][key]. \
                        append('move $' + str(part[0][1:]) + ', $' + str(part[2][1:]))
                elif part[0][0:2] == "_f" and type(part[2]) != float:
                    MIPS_CODE['.text'][key]. \
                        append('mov.s $' + str(part[0][1:]) + ', $' + str(part[2][1:]))
                elif part[0][0:2] == "_s":
                    if type(part[2]) == int:
                        MIPS_CODE['.text'][key]. \
                            append('li $' + str(part[0][1:]) + ', ' + str(part[2]))

                    elif type(part[2]) == float:
                        MIPS_CODE['.text'][key]. \
                            append('li.s $' + str(part[0][1:]) + ', ' + str(part[2]))

                    elif part[2][0] == "L":
                        MIPS_CODE['.text'][key]. \
                            append('move $' + str(part[0][1:]) + ', $a' + str(counter_a))
                    else:
                        MIPS_CODE['.text'][key]. \
                            append('move $' + str(part[0][1:]) + ', $' + str(part[2][1:]))

    if TAC.counter_main == 0:
        MIPS_CODE['.text']['main']. \
            append('j END')
    else:
        MIPS_CODE['.text']["Main"+str(TAC.counter_main)]. \
            append('j END')

    MIPS_CODE['.text']["END"] = []

if __name__ == '__main__':
    init_prog = 'progg'

    tac_dict = TAC.gen_tac(init_prog)
    simbol_table = tabl.get_table(init_prog)

    init_text_main(tac_dict)

    with open('out.a', 'w') as f:
        for key in MIPS_CODE:
            if key == ".data":
                f.write(key+'\n')
                f.write('\tstring1: .asciiz \"\\n\"\n')
                for part in MIPS_CODE[key]:
                    f.write(part + '\n')
            elif key == ".text":
                f.write(key + '\n')
                for part in MIPS_CODE[key]:
                    f.write(part+':\n')
                    for i in MIPS_CODE[key][part]:
                        f.write('\t'+str(i)+'\n')



    print("~~~~~~~~~~~~~Simbol~Table~~~~~~~~~~~~~")
    for key in simbol_table:
        print(key, ':')
        for i in simbol_table[key]:
            print('\t', i, '= ', simbol_table[key][i])
    print("\n~~~~~~~~~Three~Address~Code~~~~~~~~~")
    for key in tac_dict:
        print(key, ':')
        for i in tac_dict[key]:
            print('\t', end=' ')
            for j in i:
                print(j, end=' ')
            print('')

    # print(TAC.list_of_float)