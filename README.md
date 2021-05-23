# Compiler

Курсовая работа. Язык основан на языке Pascal с нотками Python'a.

****
В данном репозитории присутствуют такие файлы как: 

Lexer - лексический анализатор

My_parser - синтаксический анализатор с построением AST

Tabl - таблица символов 

TAC - генерация трехадресного кода

MIPS_gen - генератор кода для ассемблера

Progg - исходный код программы
****
Пример программы, которая может быть подана на вход:
~~~~
var int x; var float b;
funk lol (int a; float b) {
   s = a + b * 4 + 23;
    return s
}

t = lol(3, 3.14)
if ( t < 10 ) then {
    kek = 148;
    print(kek);
}
while(x < 5){
   print(x);
}
~~~~
