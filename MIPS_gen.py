import TAC
import tabl


if __name__ == '__main__':
    init_prog = 'progg'

    tac_dict = TAC.gen_tac(init_prog)
    simbol_table = tabl.get_table(init_prog)

    print("~~~~~~~~~~~~~Simbol~Table~~~~~~~~~~~~~")
    for key in simbol_table:
        print(key, ':')
        for i in simbol_table[key]:
            print('\t', i, '= ', simbol_table[key][i])
    print("\n~~~~~~~~~Three~Address~Code~~~~~~~~~")
    for key in tac_dict:
        print(key, ':')
        for i in tac_dict[key]:
            print('\t', i, '= ', tac_dict[key][i])
