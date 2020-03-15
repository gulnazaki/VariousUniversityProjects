canMoveFromTo(X,Y,S):-
	canGo(X,Y,R),
	priority(R,S).

suitableTaxi(T):-
	available(T),!,
	capacity(X,T),!,
	persons(Z),!,
	Z =< X,!,
	language(Y),!,
	language(Y,T),!.

valid(X):-
	canGo(X,_,_),!.

priority(R,S):-
	currtime(T),!,
	maxspeed(R,MS),!,
	(((T >= 19) ; (T =< 07)) ->
		(lit(R) ->
			DS = 1,!
		;	DS = 0.5,!
		)
	;	(traffic(R,T,high) ->
			DS = 0.6,!
		;	traffic(R,T,medium) ->
			DS = 0.8,!
		;	DS = 1,!
		)
	),
	(toll(R) ->
		TS is DS*0.5,!
	;	TS = DS,!
	),
	S is TS*MS,!.