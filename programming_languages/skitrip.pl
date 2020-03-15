% Skitrip in Prolog %

%% Melistas Thomas %%
%% Patris Nikolaos %%

%% "read_input" and "read_line" predicates were copied from "read_hopping_SWI.pl" and modified accordingly
read_input(File, N, Stops) :-
    open(File, read, Stream),
    read_line(Stream, [N]),
    read_line(Stream, Stops).
    
read_line(Stream, List) :-
    read_line_to_codes(Stream, Line),
    ( Line = [] -> List = []
    ; atom_codes(A, Line),
      atomic_list_concat(As, ' ', A),
      maplist(atom_number, As, List)
    ).

%% predicate that creates L list from the stop list taken as input
makeL([LH|LT], [SH|ST], PrevMax, Index) :-
	NewIndex is Index + 1,
	( SH < PrevMax -> LH = (Index,SH)
	, makeL(LT, ST, SH, NewIndex)
	; makeL([LH|LT], ST, PrevMax, NewIndex)
	),
	!.
makeL([], _, _, _).

%% predicate that creates R list from the reversed stop list
makeR([RH|RT], [SH|ST], PrevMin, Index) :-
	NewIndex is Index - 1,
	( SH > PrevMin -> RH = (Index,SH)
	, makeR(RT, ST, SH, NewIndex)
	; makeR([RH|RT], ST, PrevMin, NewIndex)
	),
	!.
makeR([], _, _, _).

%% takes L and R(reversed) lists and following the "spoiler" algorithm computes the maximum distance
findSolution([(LI,LH)|LT], [(RI,RH)|RT], PrevDistance, MaxDistance, A) :-
	Distance is RI - LI,
	( LH > RH -> Dist is max(PrevDistance, MaxDistance)
	, findSolution(LT, [(RI,RH)|RT], Dist, Dist, A)
	; findSolution([(LI,LH)|LT], RT, Distance, MaxDistance, A)
    ),
    !.
findSolution([], _, _, A, A).
findSolution(_, [], _, A, A).

%% "main" predicate
skitrip(File, Answer) :-
	%% reads input from file and returns number of stops (N) and a list containing them(Stops)
	read_input(File, N, Stops),
	%% make L list (we use 1000000001 as max height)
	makeL(L, Stops, 1000000001, 0),
	%% reverse Stop list to create R
	reverse(Stops, RevStops),
	LastIndex is N - 1,
	%% create R and reverse it to iterate backwards
	makeR(R, RevStops, 0, LastIndex),
	reverse(R,RevR),
	%% final predicate (we pass first 0 as previous distance and second 0 as previous max distance)
	findSolution(L, RevR, 0, 0, Answer).