from my_parser import parsing as ps


def table(tree):
    for part in tree.parts:
        temp = []
        temp_t = []
        if type(part) != str and type(part) != int:
            if part.type == 'Var' or part.type == 'parameter_list':
                for i in part.parts:
                    if i.type == 'Type':
                        type_tmp = i.parts[0]
                    if i.type == 'ID':
                        for j in i.parts:
                            temp.append(type_tmp)
                            temp.append(j)
                            temp.append(part.scope)
                            temp_t.append(temp)
                            temp = []

            if len(temp_t) > 0: simbol_table.append(temp_t)
            table(part)


if __name__=="__main__":
    simbol_table = []
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

    for line in simbol_table:
        print(line)