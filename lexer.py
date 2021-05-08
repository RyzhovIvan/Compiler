import ply.lex as lexer
from ply.lex import TOKEN
import re

states = (
   ('string','exclusive'),
)

reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'continue': 'CONTINUE',
    'break': 'BREAK',
    'int': 'INT',
    'float': 'FLOAT',
    'str': 'STR',
    'funk': 'FUNK',
    'return': 'RETURN',
    'input': 'INPUT',
    'print': 'PRINT',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'var': 'VAR'
}

tokens = [
    'EQUAL', 'ID', 'FLOAT_NUM', 'MARK',
    'STRING', 'COLON', 'COMA', 'RELOP',
    'OPEN', 'CLOSE', 'NUM', 'PLUSMINUS', 'DIVMUL',
    'CLOSE_CONSTR', 'OPEN_CONSTR', 'COMMENT'
] + list(reserved.values())


ident = r'[a-z]\w*'

t_MARK = r'"'
t_ANY_VAR = r'[a-z]\w*'
t_EQUAL = r'\='
t_COLON = r';'
t_COMA = r','
t_OPEN = r'\('
t_CLOSE = r'\)'
t_OPEN_CONSTR = r'\{'
t_CLOSE_CONSTR = r'\}'
t_PLUSMINUS = r'\+|\-'
t_DIVMUL = r'/|\*'
t_RELOP = r'\==|\<=|\>=|\>|\<|\!='


@TOKEN(ident)
def t_ID(t):
    t.type = reserved.get(t.value, 'ID')
    return t


def t_COMMENT(t):
    r'\^\_\^.*\^\_\^'
    pass

def t_FLOAT_NUM(t):
    r'\d+\.\d+'
    '[-+]?[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)'
    t.value = float(t.value)
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ANY_MARK(t):
    r'"'
    if t.lexer.current_state() == 'string':
        t.lexer.begin('INITIAL')
    else:
        t.lexer.begin('string')
    return t

t_string_STRING = r'(\\.|[^$"])+'

t_string_ignore = ''


def t_string_error(t):
    print( "Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# здесь мы игнорируем незначащие символы. Нам ведь все равно, написано $var=$value или $var   =  $value
t_ignore = ' \r\t\f'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# а здесь мы обрабатываем ошибки. Кстати заметьте формат названия функции
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lexer.lex(reflags=re.UNICODE | re.DOTALL | re.IGNORECASE)

if __name__=="__main__":
    data = '''
    var int x = 5;
    x  =  x + 3 ;
    while (result <10) {
    print(result);
    y = y + 1;
    }^_^лексер готов^_^
    funk bdfy(){
    a==v
    s = s + c;
    continue
    break
    float c = 3.2
    str kek = "Это строка"
    }
    '''

    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok: break
        print(tok)
# Вопрос: типы переменных - это зарезервированное слово?
# Разобраться с кавычками: оставлять их в строке или нет? Если нет то как называется токен?