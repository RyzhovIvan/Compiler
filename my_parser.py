import ply.yacc as yacc
from lexer import tokens


class Node:
    def parts_str(self):
        st = []
        for part in self.parts:
            st.append(str(part))
        return "\n".join(st)

    def __repr__(self):
        return self.type + ":\n\t" + self.parts_str().replace("\n", "\n\t")

    def add_parts(self, parts):
        self.parts += parts
        return self

    def __init__(self, type, parts):
        self.type = type
        self.parts = parts

    scope = 'global'


def p_program(p):  # Начало программы вызов переменных и тела проги
    '''
    program : declarations optional_statements
             '''
    p[0] = Node('Programm', [p[1], p[2]])  # Для того, чтобы создать узел я создаю экземпляр класса Node
                                           # в скобках первый аргумент это название узла (как будет выглядеть в дереве)
                                           # вторым аргументом я передаю его доцерние узлы, которые будут отображаться
                                           # чтобы понятнее было покажу как обозначаются элементы самой продукции
                                           # program : declarations optional_statements
                                           #  p[0]   :      p[1]           p[2]

def p_identifier_list(p):  # перечисление переменных
    '''identifier_list : ID
                       | identifier_list COMA ID '''
    if len(p) == 2:
        p[0] = Node("ID", [p[1]])          # В этой продукции у меня как может создаваться узел, так и добавляться
    else:                                  # к этому узлу дочерние ветки
        p[0] = p[1].add_parts([p[3]])      # Как видишь в функции add_parts я просто указываю к какому узлу добавить
                                           # и что добавить к нему


def p_declarations(p):  # обозначение переменных
    '''declarations : declarations VAR type identifier_list COLON
                    | empty'''
    if len(p) == 2:
        p[0] = Node('Var', [], )
    else:
        p[0] = p[1].add_parts([p[3], p[4]])


def p_type(p):  # Типы
    '''type : INT
            | FLOAT
            | STR'''
    p[0] = Node("Type", [p[1]])


def p_optional_statements(
        p):  # Продукция для всего, может быть как пусто, так и все, циклы, функции, условия, выражения
    '''optional_statements : statement_list
                           | empty'''
    p[0] = Node("optional_statements", [p[1]])


def p_statement_list(p):  # Различные состояния - вспомогательная продукция
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = Node('statement_list', [p[1]])
        p[1].scope = p[0].scope
    else:
        p[0] = p[1].add_parts([p[2]])


def p_statement(p):  # сами выражения которые могут быть
    '''statement : IF OPEN expression CLOSE THEN compound_statement ELSE compound_statement
                 | WHILE OPEN expression CLOSE compound_statement
                 | subprogram_declarations
                 | expression'''
    if len(p) == 2:
        p[0] = p[1]
        p[1].scope = p[0].scope
    elif len(p) == 6:
        p[0] = Node("While", [p[3], p[5]])
    else:
        p[0] = Node('If\Else', [p[3], p[6], p[8]])


def p_subprogram_declarations(
        p):  # Продукция для обозначения функций (любого их числа, т.е. их может быть много подряд)
    '''subprogram_declarations : subprogram_declaration
                               | subprogram_declarations subprogram_declaration'''
    if len(p) == 2:
        p[0] = Node('subprogram_declarations', [p[1]])
    else:
        p[0] = p[1].add_parts([p[2]])


def p_subprogram_declaration(p):  # Продукция чисто для определленной функции
    '''subprogram_declaration : subprogram_head declarations compound_statement'''
    p[0] = Node("Function", [p[1], p[2], p[3]])
    p[2].scope = p[1].scope


def p_subprogram_head(p):  # Оглавление функции
    '''subprogram_head : FUNK ID arguments '''
    p[0] = Node("Function_head", [p[1], p[2], p[3]])
    p[3].scope = p[2]
    p[0].scope = p[2]


def p_arguments(p):  # Тело аргументов, которые мы передаем в функцию "( аргументы )"
    '''arguments : OPEN parameter_list CLOSE'''
    p[0] = p[2]
    p[2].scope = p[0].scope


def p_parameter_list(p):  # Сам вид аргументов, как их передавать в функцию (int a, float b)
    '''parameter_list : type identifier_list
                      | parameter_list COLON type identifier_list'''
    if len(p) == 3:
        p[0] = Node("parameter_list", [p[1], p[2]])
        p[2].scope = p[0].scope
    else:
        p[0] = p[1].add_parts([p[3], p[4]])
        p[4].scope = p[0].scope


def p_compound_statement(p):  # фигурные скобки и продукция - для всего, та самая сверху
    '''compound_statement : OPEN_CONSTR optional_statements CLOSE_CONSTR'''
    p[0] = Node("compound_statement", [p[2]])


"""
def p_w_compound(p): # фигурные скобки для while, так как там должны быть break и continue
    '''w_compound : OPEN_CONSTR w_optional_statements CLOSE_CONSTR'''
    p[0] = Node("w_compound", [p[2]])


def p_w_optional_statements(p): # Вспомогательная продукция для while, список
    '''w_optional_statements : statement_limb_operators
                             | w_optional_statements statement_limb_operators'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node("w_optional_statements", [p[1], p[2]])


def p_statement_limb_operators(p): # Что конкретно пишем внутри и что выбираем из операторов
    ''' statement_limb_operators : optional_statements BREAK
                                 | optional_statements CONTINUE
                                 | optional_statements '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node("statement_limb_operators", [p[1], p[2]])

"""


def p_expression_list(p):  # Список выражений
    '''expression_list : expression
                       | expression_list COMA expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node("expression_list", [p[1], p[3]])


def p_expression(p):  # Сами выражения(здесь могут быть логические выр, оператооры сравнения и просто выражения)
    '''expression : NOT simple_expression
                  | expression AND simple_expression
                  | expression OR simple_expression
                  | simple_expression RELOP simple_expression
                  | simple_expression'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = Node("expression", [p[1], p[2]])
    else:
        p[0] = Node("expression", [p[1], p[2], p[3]])


def p_simple_expression(p):  # Обычные простые выражения,  включая принт и инпут
    '''simple_expression : term
                         | simple_expression PLUSMINUS term
                         | eqstate
                         | in
                         | out'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node("simple_expression", [p[1], p[2], p[3]])


def p_eqstate(p):  # Оператор присваивания
    '''eqstate : factor EQUAL term
               | factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node("eqstate", [p[1], p[2], p[3]])


def p_term(p):  # Делить умножать
    '''term : factor
            | term DIVMUL factor '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node("term", [p[1], p[2], p[3]])


def p_out(p):
    '''out : PRINT OPEN factor CLOSE COLON '''
    p[0] = Node("out", [p[1], p[3]])


def p_in(p):
    '''in : INPUT OPEN CLOSE COLON'''
    p[0] = Node("in", [p[1]])


def p_factor(p):
    '''factor : ID
              | ID OPEN expression_list CLOSE
              | NUM
              | CONTINUE
              | BREAK
              | FLOAT_NUM
              | OPEN expression CLOSE
              | type factor
              | NOT factor
              | MARK STRING MARK
              | factor COLON'''
    if len(p) == 2:
        p[0] = Node("Factor", [p[1]])
    elif len(p) == 3:
        if p[2] == ";":
            p[0] = p[1]
        else:
            p[0] = Node("Factor", [p[1], p[2]])
    elif len(p) == 4:
        p[0] = Node("Factor", [p[1], p[2], p[3]])
    else:
        p[0] = Node("Factor", [p[1], p[3]])


def p_empty(p):
    'empty :'
    pass


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOT'),
    ('left', 'EQUAL'),
    ('left', 'PLUSMINUS'),
    ('left', 'DIVMUL'),
)

def parsing():
    parser_data = yacc.yacc()
    return parser_data

if __name__ == "__main__":
    a = '''
    var int x;
    while ( result < 10 ) {
        y = 1 * ((2 + 2) +  1);
        print(sadfafs);
    }
    funk fuckc (int a, d; float b) {
        s = s + 1; 
    }
    
    funk ass (int a, d; float b) {
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
    '''

    result = parsing().parse(a)
    print(result)
