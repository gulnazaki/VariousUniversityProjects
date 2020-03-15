% Moredeli in Prolog %

%% Melistas Thomas %%
%% Patris Nikolaos %%

%% all reading predicates (read_input,read_lines,read_line,checkAndReadNext) were influenced by: http://www.learnprolognow.org/lpnpage.php?pagetype=html&pageid=lpn-htmlse54 -
%% - and "read_hopping_SWI.pl" and were modified a lot to better suit this program's needs

%% "wrapper" predicate, opens file and creates our Map as an association list of association lists
read_input(File, Map, StartX, StartY) :-
    open(File, read, Stream),
    read_lines(Stream, PairMap, StartX, StartY, 0),
    list_to_assoc(PairMap, Map).

%% reads all rows and returns StartX 
read_lines(Stream, [], _, _, _) :- 
	at_end_of_stream(Stream),
	!.
read_lines(Stream, [Index-Line|Lines], StartX, StartY, Index) :-
	NewIndex is Index + 1,
	read_line(Stream, Line, StartY),
	( nonvar(StartY), var(StartX) -> StartX = Index
	; true
	),
	read_lines(Stream, Lines, StartX, StartY, NewIndex).

%% reads one row, returns StartY - uses checkAndReadNext predicate to read characters one by one
read_line(Stream, Line, StartY):- 
	get_char(Stream, Char), 
    checkAndReadNext(Char, Chars, Stream, 0, StartY),
    list_to_assoc(Chars,Line).
    
%% checks if the character previously read is valid and if so reads next character (recursive) - also if we encounter S returns StartY
checkAndReadNext('\n', [], _, _, _) :- !. 
checkAndReadNext(end_of_file, [], _, _, _) :- !.
checkAndReadNext(Char, [Index-(Char,0)|Chars], Stream, Index, StartY):- 
    NewIndex is Index + 1,
    ( Char = 'S' -> StartY = Index
    ; true
    ),
    get_char(Stream, NextChar), 
    checkAndReadNext(NextChar, Chars, Stream, NewIndex, StartY).

%% if square is valid it updates our Map(sets best cost so far) else it fails
valid(Map, X, Y, Cost, NewMap) :-
	get_assoc(X, Map, Row),
	get_assoc(Y, Row, (Symbol,PrevCost)),
	( Symbol = '.' ; Symbol = 'E'),
	( PrevCost = 0 ; PrevCost > Cost ),
	put_assoc(Y, Row, (Symbol,Cost), NewRow),
	put_assoc(X, Map, NewRow, NewMap).

%% if neighbour square is valid (R here) updates map (via valid predicate) and our priority Queue
addR(Q, Map, Cost, ((X,Y),Path), NewQ, NewMap) :-
	NewY is Y + 1,
	NewCost is Cost + 1,
	( valid(Map, X, NewY, NewCost, NewMap) -> append(Path, [r], NewPath)
	, add_to_heap(Q, NewCost, ((X,NewY),NewPath), NewQ)
	; NewQ = Q
	, NewMap = Map
	).

addL(Q, Map, Cost, ((X,Y),Path), NewQ, NewMap) :-
	NewY is Y - 1,
	NewCost is Cost + 2,
	( valid(Map, X, NewY, NewCost, NewMap) -> append(Path, [l], NewPath)
	, add_to_heap(Q, NewCost, ((X,NewY),NewPath), NewQ)
	; NewQ = Q
	, NewMap = Map
	).

addD(Q, Map, Cost, ((X,Y),Path), NewQ, NewMap) :-
	NewX is X + 1,
	NewCost is Cost + 1,
	( valid(Map, NewX, Y, NewCost, NewMap) -> append(Path, [d], NewPath)
	, add_to_heap(Q, NewCost, ((NewX,Y),NewPath), NewQ)
	; NewQ = Q
	, NewMap = Map
	).

addU(Q, Map, Cost, ((X,Y),Path), NewQ, NewMap) :-
	NewX is X - 1,
	NewCost is Cost + 3,
	( valid(Map, NewX, Y, NewCost, NewMap) -> append(Path, [u], NewPath)
	, add_to_heap(Q, NewCost, ((NewX,Y),NewPath), NewQ)
	; NewQ = Q
	, NewMap = Map
	).

%% solving (recursive) predicate, removes minimum cost square from Q, if 'E' solution is found else inserts all valid neighbours
find_solution(Q, Map, Cost, Solution) :-
	get_from_heap(Q, CurrCost, ((CurrX,CurrY),CurrPath), QwithoutCurr),
	( get_assoc(CurrX, Map, Row), get_assoc(CurrY, Row, ('E',Cost)) -> Solution = CurrPath
	; addR(QwithoutCurr, Map, CurrCost, ((CurrX,CurrY),CurrPath), NewQ1, NewMap1)
	, addL(NewQ1, NewMap1, CurrCost, ((CurrX,CurrY),CurrPath), NewQ2, NewMap2)
	, addD(NewQ2, NewMap2, CurrCost, ((CurrX,CurrY),CurrPath), NewQ3, NewMap3)
	, addU(NewQ3, NewMap3, CurrCost, ((CurrX,CurrY),CurrPath), NewQ4, NewMap4)
	, find_solution(NewQ4, NewMap4, Cost, Solution)
	).

%% "main" predicate - reads input, creates our priority queue(heap) Q with start element and calls solving predicate
moredeli(File, Cost, Solution) :-
	read_input(File, Map, StartX, StartY),
	singleton_heap(Q, 0, ((StartX,StartY),[])),
	find_solution(Q, Map, Cost, Solution).