%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* new_temp();
char* new_label();
void gen_tac(const char *res, const char *arg1, const char *arg2, const char *op);

extern int yylex();
extern int yylineno;
extern char *yytext;
void yyerror(const char *s);

char *label_stack[100];
int label_top = -1;
void push_label(char *label) { label_stack[++label_top] = label; }
char *pop_label() { return label_stack[label_top--]; }
%}

%union {
    char *sval;
}

%token <sval> ID NUMBER RELOP
%token WHILE
%type <sval> expr condition assignment

%left '+' '-'
%left '*' '/'

%start program

%%

program: statements {
            printf("\n--- TAC Generation Complete ---\n");
            YYACCEPT;
         };

statements:
          | statements statement
          ;

statement: assignment ';'
         | while_loop
         | expr ';' { gen_tac("print", $1, NULL, NULL); }
         | error ';' { yyerrok; }
         ;

while_loop: WHILE {
                char *l_begin = new_label();
                printf("%s:\n", l_begin);
                push_label(l_begin);
           }
           '(' condition ')' {
                char *l_body = new_label();
                char *l_end = new_label();
                printf("if (%s) goto %s\n", $4, l_body);
                printf("goto %s\n", l_end);
                printf("%s:\n", l_body);
                push_label(l_end);
           }
           '{' statements '}' {
                char *l_end = pop_label();
                char *l_begin = pop_label();
                printf("goto %s\n", l_begin);
                printf("%s:\n", l_end);
           }
           ;

condition: expr RELOP expr {
               $$ = new_temp();
               gen_tac($$, $1, $3, $2);
           };

assignment: ID '=' expr {
                gen_tac($1, $3, NULL, "=");
                $$ = $1;
           };

expr: expr '+' expr {
          $$ = new_temp();
          gen_tac($$, $1, $3, "+");
      }
    | expr '-' expr {
          $$ = new_temp();
          gen_tac($$, $1, $3, "-");
      }
    | expr '*' expr {
          $$ = new_temp();
          gen_tac($$, $1, $3, "*");
      }
    | expr '/' expr {
          $$ = new_temp();
          gen_tac($$, $1, $3, "/");
      }
    | '(' expr ')' {
          $$ = $2;
      }
    | ID { $$ = $1; }
    | NUMBER { $$ = $1; }
    ;

%%

int temp_count = 0;
int label_count = 0;

char* new_temp() {
    char *temp = (char*)malloc(10 * sizeof(char));
    sprintf(temp, "t%d", temp_count++);
    return temp;
}

char* new_label() {
    char *label = (char*)malloc(10 * sizeof(char));
    sprintf(label, "L%d", label_count++);
    return label;
}

void gen_tac(const char *res, const char *arg1, const char *arg2, const char *op) {
    if (strcmp(op, "=") == 0) {
        printf("%s = %s\n", res, arg1);
    } else if (arg2 == NULL) {
        printf("%s %s\n", res, arg1);
    } else {
        printf("%s = %s %s %s\n", res, arg1, op, arg2);
    }
}

int main() {
    printf("Enter code to generate TAC. Press Ctrl+D when done.\n");
    printf("---------------------------------------------------\n");
    if (yyparse() == 0) {
    } else {
        printf("\n[FAILURE] Parsing failed.\n");
    }
    return 0;
}

void yyerror(const char *s) {
    fprintf(stderr, "[ERROR] Line %d near '%s': %s\n", yylineno, yytext, s);
}
