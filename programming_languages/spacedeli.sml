(* Delivery in space *)

(* Melistas Thomas *)
(* Patris Nikolas *)


(* makeMap reads file and returns a tuple of: our map as a 2d character array and the coordinates of start (map,(x,y)) *)
fun makeMap file =
    let
        fun parse file =
            let
                val fp = TextIO.openIn file
                val str = TextIO.inputAll fp
            	val closed = TextIO.closeIn fp
            in
                String.tokens Char.isSpace str
            end
        val charList = map explode (parse file)
        val charArray = Array2.fromList charList
        fun startCoordinates (chararray,x,y) =
        	let
        		val cols = Array2.nCols charArray
        	in
        		if (Array2.sub (charArray,x,y) = #"S") then (x,y)
        		else if (y < cols - 1) then startCoordinates (charArray,x,y+1)
        		else startCoordinates (charArray,x+1,0)
        	end
    in
        (charArray, startCoordinates (charArray,0,0))
    end


(* Getter: carrying a pizza? *)
fun get_pizza (x : bool * (int * int) * string * int) = #1 x

(* Getter: coordinates *)
fun get_coord (x : bool * (int * int) * string * int) = #2 x

(* Getter: path *)
fun get_path (x : bool * (int * int) * string * int) = #3 x

(* Getter: cost *)
fun get_cost (x : bool * (int * int) * string * int) = #4 x


(* inserts states in the list by priority (smallest cost first); (true,(0,0),"",~1) is a false state and we use it when we hit a dead end *)
fun insertToList l (true,(0,0),"",~1) = l
  | insertToList [] curr = [curr]
  | insertToList (h::t) curr = 
  	if ((get_cost curr) > (get_cost h)) then h::(insertToList t curr)
  	else if ((get_pizza curr) = (get_pizza h)) andalso ((get_coord curr) = (get_coord h)) then h::t
  	else curr::h::t


(* simply pop the head (smallest cost) *)
fun removeFromList [] = raise Empty
  | removeFromList (h::t) = (h,t)


(* We apply the following symbolisms (one character to cipher states (it may seem too complex but it saves us from a lot of memory)):
 S->start
 E->end
 A->end visited without pizza
 P->normal square visited with pizza
 N->normal square visited without pizza
 X->visited with and without pizza; or simply obstacle
 W->wormhole
 Y->visited wormhole with pizza
 Z->visited wormhole without pizza
*)fun editMap map (true,(0,0),"",~1) = ()
	| editMap map (pizza,(x,y),path,cost) =
	case pizza of                   
		true =>  ( case (Array2.sub (map,x,y)) of         
              		( #"S" | #"." ) => Array2.update (map,x,y,#"P")
              	  | ( #"N" | #"Z" ) => Array2.update (map,x,y,#"X")
               	  | #"W"      => Array2.update (map,x,y,#"Y")
               	  | #"A"      => Array2.update (map,x,y,#"A")
				  | #"E"      => Array2.update (map,x,y,#"E") )
	  | false => ( case (Array2.sub (map,x,y)) of         
                	#"E"      => Array2.update (map,x,y,#"A")
                  | ( #"S" | #"." ) => Array2.update (map,x,y,#"N")
                  | ( #"P" | #"Y" ) => Array2.update (map,x,y,#"X")
                  | #"W"      => Array2.update (map,x,y,#"Z") )


(* are we there yet? *)
fun isEnd (pizza,(x,y),path,cost) map =
	if (pizza = true) andalso ((Array2.sub (map,x,y) = #"E") orelse (Array2.sub (map,x,y) = #"A")) then true
	else false


(* can visit these squares with a pizza *)
fun pizzable (i,j) map =
	if (Array2.sub (map,i,j) = #"P") orelse (Array2.sub (map,i,j) = #"X") orelse (Array2.sub (map,i,j) = #"Y") then false
	else true


(* can visit these squares without a pizza *)
fun unpizzable (i,j) map =
	if (Array2.sub (map,i,j) = #"N") orelse (Array2.sub (map,i,j) = #"X") orelse (Array2.sub (map,i,j) = #"Z") orelse (Array2.sub (map,i,j) = #"A") then false
	else true


(* this function searches (bfs) for the best path; we use it mutually recursively with doNeighboursNow *)
fun searchPath spaceState map spaceList= 
	let
		val endFlag = (isEnd spaceState map)
		val spaceList = insertToList spaceList spaceState
		val _ = editMap map spaceState
		val newState = ((#1) (removeFromList spaceList))
		val spaceList = ((#2) (removeFromList spaceList))
	in
		if (endFlag) then ((get_cost spaceState),(get_path spaceState))
		else 
			doNeighboursNow newState map spaceList
	end	


(* doNeighboursNow checks for the neighbour squares and calls searchPath for those we haven't yet searched; puts also previous square again in the list until we don't need it *)
and doNeighboursNow (pizza,(x,y),path,cost) map spaceList =
	let
		val colLimit = (Array2.nCols map) - 1
		val rowLimit = (Array2.nRows map) - 1
	in
		case pizza of                   
		true  =>  if (Array2.sub (map,x,y) = #"Y") then 
					let
						val spaceList = insertToList spaceList (pizza,(x,y),path,cost)
					in
						searchPath (false,(x,y),path^"W",cost+1) map spaceList
					end
			 else if (x < rowLimit) andalso (pizzable (x+1,y) map) then 
					let
						val spaceList = insertToList spaceList (pizza,(x,y),path,cost)
					in
						searchPath (pizza,(x+1,y),path^"D",cost+2) map spaceList
					end
			 else if (x > 0)        andalso (pizzable (x-1,y) map) then 
			 		let
						val spaceList = insertToList spaceList (pizza,(x,y),path,cost)
					in
						searchPath (pizza,(x-1,y),path^"U",cost+2) map spaceList
					end
			 else if (y < colLimit) andalso (pizzable (x,y+1) map) then 
			 		let
						val spaceList = insertToList spaceList (pizza,(x,y),path,cost)
					in
						searchPath (pizza,(x,y+1),path^"R",cost+2) map spaceList
					end
			 else if (y > 0)        andalso (pizzable (x,y-1) map) then 
			 		let
						val spaceList = insertToList spaceList (pizza,(x,y),path,cost)
					in
						searchPath (pizza,(x,y-1),path^"L",cost+2) map spaceList
					end
			 else 		searchPath (true,(0,0),"",~1) map spaceList
	  | false =>  if (Array2.sub (map,x,y) = #"Z") then 
					let
						val spaceList = insertToList spaceList (pizza,(x,y),path,cost)
					in
						searchPath (true,(x,y),path^"W",cost+1) map spaceList
					end
			 else if (x < rowLimit) andalso (unpizzable (x+1,y) map) then 
					let
						val spaceList = insertToList spaceList (pizza,(x,y),path,cost)
					in
						searchPath (pizza,(x+1,y),path^"D",cost+1) map spaceList
					end
			 else if (x > 0)        andalso (unpizzable (x-1,y) map) then 
			 		let
						val spaceList = insertToList spaceList (pizza,(x,y),path,cost)
					in
						searchPath (pizza,(x-1,y),path^"U",cost+1) map spaceList
					end
			 else if (y < colLimit) andalso (unpizzable (x,y+1) map) then 
			 		let
						val spaceList = insertToList spaceList (pizza,(x,y),path,cost)
					in
						searchPath (pizza,(x,y+1),path^"R",cost+1) map spaceList
					end
			 else if (y > 0)        andalso (unpizzable (x,y-1) map) then 
			 		let
						val spaceList = insertToList spaceList (pizza,(x,y),path,cost)
					in
						searchPath (pizza,(x,y-1),path^"L",cost+1) map spaceList
					end
			 else 		searchPath (true,(0,0),"",~1) map spaceList
	end


(* initialises search *)
fun startPath (map,(startX,startY)) =

		searchPath (true,(startX,startY),"",0) map []


(* final function *)
fun spacedeli file =
	let
		val spaceMap = makeMap file
	in
		startPath spaceMap
	end