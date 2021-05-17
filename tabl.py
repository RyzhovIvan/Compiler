from my_parser import parsing as ps


def table(tree):
    global simbol_table
    for part in tree.parts:
        if type(part) != str and type(part) != int:
            if part.type == 'Var' or part.type == 'parameter_list':
                for i in part.parts:
                    if i.type == 'Type':
                        type_tmp = i.parts[0]
                    if i.type == 'ID':
                        if part.scope not in simbol_table.keys():
                            simbol_table[part.scope] = {}
                            simbol_table[part.scope][type_tmp] = []
                        elif type_tmp not in simbol_table[part.scope].keys():
                            simbol_table[part.scope][type_tmp] = []
                        for j in i.parts:
                            simbol_table[part.scope][type_tmp].append(j)

            table(part)


def get_table(init_prog):
    global simbol_table
    simbol_table = {}
    with open(init_prog, 'r') as f:
        s = f.read()

    result = ps().parse(s)
    table(result)

    return simbol_table


if __name__=="__main__":
    simbol_table = {}
    a = '''
    var int x;
    while ( result < 10 ) {
        y = 1 * ((2 + 2) +  1);
        print(sadfafs);
    }
    funk fuckc (int a, d; float b) {
        s = s + 1; 
    }
    if ( r < 10 ) then {
        kek = ddd;
        print(llllll);
    }
    else{
        lol = lol;
        while (t == 0){
            a = (a + 1) * 2;
            break
            a = 2;
            break
        }
    }
    funk ass (int a, d; float b) {
        s = s + 1; 
    }
    '''
    s = '''
    var int x; var float b;
    funk assasin (int a, d; float c) var float xyz; {
        s = s + 1; 
    }
    funk duck (int a, d; float b) {
        s = s + 1; 
    }
    '''

    result = ps().parse(s)
    table(result)

    for key in simbol_table:
        print(key, ':')
        for i in simbol_table[key]:
            print('\t', i, '= ', simbol_table[key][i])
