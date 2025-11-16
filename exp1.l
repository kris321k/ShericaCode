%{
#include <stdio.h>
%}
%%
-?[0-9]+              { printf("%s : Integer\n", yytext); }
[0-9]+"."[0-9]+       { printf("%s : Real Number\n", yytext); }
[a-zA-Z]+             { printf("%s : Word\n", yytext); }
.|\n                  { /* ignore other characters */ }
%%
int main() {
    yylex();
    return 0;
}
int yywrap() {
    return 1;
}
