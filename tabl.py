from my_parser import parsing as ps


def check_same_names(var):
    for key in simbol_table:
        for type in simbol_table[key]:
            if var in simbol_table[key][type]:
                return False
    return True


def table(tree):
    global simbol_table
    for part in tree.parts:
        if type(part) != str and type(part) != int and type(part) != float:
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
                            if check_same_names(j):
                                simbol_table[part.scope][type_tmp].append(j)
                            else:
                                print("Названия переменных должны быть разными!!!")
            table(part)


def get_table(init_prog):
    global simbol_table
    simbol_table = {}
    with open(init_prog, 'r') as f:
        s = f.read()

    result = ps().parse(s)
    # print(result)
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
    var float x, c;
    var int y, z;


    funk lol (int v){
        v = 2;
        return v
    }
    
    x = lol(c)


    '''

    result = ps().parse(s)
    print(result)
    table(result)

    for key in simbol_table:
        print(key, ':')
        for i in simbol_table[key]:
            print('\t', i, '= ', simbol_table[key][i])
