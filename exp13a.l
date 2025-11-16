%{
#include <stdio.h>
int line_number = 0;
%}
%%
.*\n    { line_number++; printf("Line %d: %s", line_number, yytext); }
.+      ;
%%
int main() {
    yylex();
    return 0;
}
int yywrap() {
    return 1;
}
