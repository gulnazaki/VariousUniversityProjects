%{
#include "parser.h"
#define T_eof 0

void yyerror (const char msg []);

int linecnt = 1;
int nested_cnt = 0;
%}


L [a-zA-Z]
D [0-9]
W [ \t\r]
Esc (\\n)|(\\t)|(\\r)|(\\0)|(\\\\)|(\\\')|(\\\")|(\\[x][0-9a-fA-F]{2})
P [\040\041\043-\046\050-\133\135-\177]

%x COMMENT
%option nounput noinput noyywrap
%%

"byte"       {return T_byte;}
"else"       {return T_else;}
"false"      {return T_false;}
"if"         {return T_if;}
"int"        {return T_int;}
"proc"       {return T_proc;}
"reference"  {return T_ref;}
"return"     {return T_return;}
"while"      {return T_while;}
"true"       {return T_true;}
"=="         {return T_eq;}
"!="         {return T_neq;}
"<="         {return T_leq;}
">="         {return T_geq;}

[()\{\}\[\],:;=\+\-\*/%!&<>]   {return yytext[0];}
{L}({L}|{D}|_)*              {return T_id;}
{D}+                         {return T_const_int;}
\'({P}|{Esc})\'              {return T_const_char;}
\"({P}|{Esc})*\"             {return T_const_str;}
[\n]			{ linecnt++;}
{W}+            { /* nothing */}
--.*\n          { linecnt++;}
"(*"			{ BEGIN(COMMENT); nested_cnt++;}
<COMMENT>"(*"        { nested_cnt++;}
<COMMENT>"*)"	{ if (--nested_cnt==0) BEGIN(INITIAL);}
<COMMENT>\n 	{ linecnt++;}
<COMMENT>.     { /* nothing */}
.               { yyerror("Illegal token");}

%%
