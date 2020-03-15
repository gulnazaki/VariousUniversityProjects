%{
#include <stdio.h>
#include <stdlib.h>

void yyerror (const char *msg);

extern int linecnt;
%}

%token T_byte   "byte"
%token T_else   "else"
%token T_false  "false"
%token T_if     "if"
%token T_int    "int"
%token T_proc   "proc"
%token T_ref    "reference"
%token T_return "return"
%token T_while  "while"
%token T_true   "true"
%token T_id   
%token T_const_int 
%token T_const_char 
%token T_const_str 
%token T_eq     "=="
%token T_neq    "!="
%token T_leq    "<="
%token T_geq    ">="

%left '|'
%left '&'
%nonassoc EQ NEQ '>' '<' LE GE
%left '+' '-'
%left '*' '/' '%'
%precedence POS NEG '!'

%%

program:
  func_def
;

func_def:
  T_id '(' opt_fpar_list ')' ':' r_type local_def_list compound_stmt
;

opt_fpar_list:
  %empty
| fpar_list
;

fpar_list:
  fpar_def
| fpar_def ',' fpar_list
;

fpar_def:
  T_id ':' type
| T_id ':' "reference" type
;

data_type:
  "int"
| "byte"
;

type:
  data_type
| data_type '['']'
;

r_type:
  data_type
| "proc"
;

local_def_list:
  %empty
| local_def local_def_list
;

local_def:
  func_def
| var_def
;

var_def:
  T_id ':' data_type ';'
| T_id ':' data_type '[' T_const_int ']' ';'
;

stmt:
  ';'
| l_value '=' expr ';'
| compound_stmt
| func_call ';'
| "if" '(' cond ')' stmt 
| "if" '(' cond ')' stmt "else" stmt
| "while" '(' cond ')' stmt 
| "return" ';'
| "return" expr ';'
;

compound_stmt:
  '{' stmt_list '}'
;

stmt_list:
  stmt
| stmt_list stmt
;

func_call:
  T_id '(' ')'
| T_id '(' expr_list ')'
;

expr_list:
  expr
| expr_list ',' expr
;

expr:
  T_const_int
| T_const_char
| l_value
| '(' expr ')'
| func_call 
| '+' expr         %prec POS
| '-' expr         %prec NEG
| expr '+' expr
| expr '-' expr
| expr '*' expr
| expr '/' expr
| expr '%' expr
;

l_value:
  T_id
| T_id '[' expr ']'
| T_const_str
;

cond:
  "true"
| "false"
| '(' cond ')'
| '!' cond 
| expr "==" expr    %prec EQ
| expr "!=" expr    %prec NEQ
| expr '<'  expr    
| expr '>' expr    
| expr "<=" expr    %prec LE
| expr ">=" expr    %prec GE
| cond '&' cond
| cond '|' cond
;

%%
void yyerror (const char *msg) {
  fprintf(stderr, "Alan error: %s\n", msg);
  fprintf(stderr, "Aborting, I've had enough with line %d...\n",
          linecnt);
  exit(1);
}

int main() {
  if (yyparse()) return 1;
  printf("Compilation was successful.\n");
  return 0;
}
		


