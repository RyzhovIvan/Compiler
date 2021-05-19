import TAC
import tabl

type_var = ''
MIPS_CODE = {'.data': [], '.text': {}}


def init_text_main(tac_dict):
    global type_var
    for key in tac_dict:
        MIPS_CODE['.text'][key] = []
        if len(tac_dict[key]) == 0:
            MIPS_CODE['.text'][key].append('b Main' + str(TAC.counter_main))
        for part in tac_dict[key]:
            if len(part) > 3 and part[3] == '+':
                if type(part[2]) != (int or float) and type(part[4]) == (int or float):
                    MIPS_CODE['.text'][key].\
                        append('addi $' + str(part[0][1:]) + ', $' + str(part[2][1:]) + ', ' + str(part[4]))

                elif type(part[2]) == (int or float) and type(part[4]) != (int or float):
                    MIPS_CODE['.text'][key].\
                        append('addi $' + str(part[0][1:]) + ', $' + str(part[4][1:]) + ', ' + str(part[2]))

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

                else:
                    MIPS_CODE['.text'][key]. \
                        append('div $' + str(part[0][1:]) + ', $' + str(part[2][1:]) + ', $' + str(part[4][1:]))

            elif part[0] == 'print':
                _t = ""
                for i in simbol_table['global']:
                    if part[1] in simbol_table['global'][i]:
                        type_var = i
                        break
                    else:
                        print("Нет такой переменной")

                for i in tac_dict['Main']:
                    if part[1] in i:
                        _t = i[2][1:]
                        break

                if type_var == 'int' and _t != "":
                    MIPS_CODE['.text'][key].\
                        append('move $a0, $' + _t + '\n\tli $v0 1\n\tsyscall\n')

                    MIPS_CODE['.text'][key]. \
                        append('la $a0, string1\n\tli $v0 4\n\tsyscall\n')

                else:
                    MIPS_CODE['.text'][key].\
                        append('move $f12, $' + _t + '\n\tli $v0 2\n\tsyscall\n')

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

            elif part[0] == 'Goto':
                MIPS_CODE['.text'][key].append('b ' + str(part[1]))

            elif len(part) == 3:
                if part[0][0] == "_" and type(part[2]) == (int or float):
                    MIPS_CODE['.text'][key].\
                        append('li $' + str(part[0][1:]) + ', ' + str(part[2]))
                elif part[0][0] == "_":
                    MIPS_CODE['.text'][key]. \
                        append('move $' + str(part[0][1:]) + ', $' + str(part[2][1:]))


if __name__ == '__main__':
    init_prog = 'progg'

    tac_dict = TAC.gen_tac(init_prog)
    simbol_table = tabl.get_table(init_prog)

    init_text_main(tac_dict)

    with open('out.a', 'w') as f:
        for key in MIPS_CODE:
            if key == ".data":
                f.write(key+':\n')
                f.write('\tstring1: .asciiz \"\\n\"\n')
            elif key == ".text":
                f.write(key + ':' + '\n')
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

