(* More delivery in space *)

(* Melistas Thomas *)
(* Patris Nikolaos *)


(* Most functions were copied from program "spacedeli" of the first set and modified accordingly *)


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


(* Getter: coordinates *)
fun get_coord (x : (int * int) * string * int) = #1 x

(* Getter: path *)
fun get_path (x : (int * int) * string * int) = #2 x

(* Getter: cost *)
fun get_cost (x : (int * int) * string * int) = #3 x


(* inserts states in the list by priority (smallest cost first); (true,(0,0),"",~1) is a false state and we use it when we hit a dead end *)
fun insertToList l ((0,0),"",~1) endFlag= l
  | insertToList [] curr endFlag= [curr]
  | insertToList (h::t) curr endFlag= 
  	if endFlag then (t) 
  	else
  	if ((get_cost curr) > (get_cost h)) then h::(insertToList t curr endFlag)
  	else if (get_coord curr) = (get_coord h) andalso (get_cost h) <= (get_cost curr) then h::t
  	else curr::h::t


fun costInList [] coord = 0
  |	costInList (h::t) coord = 
	if (get_coord h) = coord then (get_cost h)
	else costInList t coord


(* simply pop the head (smallest cost) *)
fun removeFromList [] = (((0,0),"",~1),[])
  | removeFromList (h::t) = (h,t)


(* We apply the following symbolisms (one character to cipher states (it may seem too complex but it saves us from a lot of memory)):
 S->start
 E->end
 V->visited
 X->obstacle
*)fun editMap map ((0,0),"",~1) endFlag = ()
	| editMap map ((x,y),path,cost) true = ()
	| editMap map ((x,y),path,cost) false = Array2.update (map,x,y,#"V")
	

(* if we have visited this square before or if it is an obstacle this function returns false *)
fun valid (x,y) map cost spaceList =
	if (Array2.sub (map,x,y) = #"X") orelse (Array2.sub (map,x,y) = #"V" andalso cost >= (costInList spaceList (x,y))) then false
	else true


(* are we there yet? *)
fun isEnd ((x,y),path,cost) map =
	if Array2.sub (map,x,y) = #"E" then true
	else false


(* this function searches for the best path; we use it mutually recursively with doNeighboursNow *)
fun searchPath spaceState map spaceList = 
	let
		val endFlag = (isEnd spaceState map)
		val spaceList = insertToList spaceList spaceState endFlag
		val _ = editMap map spaceState endFlag
		val newState = ((#1) (removeFromList spaceList))
		val spaceList = ((#2) (removeFromList spaceList))
	in
		doNeighboursNow newState map spaceList endFlag ((get_cost spaceState),(get_path spaceState))
	end	


(* doNeighboursNow checks for the neighbour squares and calls searchPath for those we haven't yet searched; puts also previous square again in the list until we don't need it *)
and doNeighboursNow ((x,y),path,cost) map spaceList endFlag (prev_cost,prev_path) =
	let
		val colLimit = (Array2.nCols map) - 1
		val rowLimit = (Array2.nRows map) - 1
	in
		if endFlag then
			if cost < 0 then (prev_cost,prev_path)
	else if (x < rowLimit) andalso ((cost+1)<prev_cost) andalso (isEnd ((x+1,y),path,cost) map) then 
				(cost+1,path^"D")
   else if (y < colLimit) andalso ((cost+1)<prev_cost) andalso (isEnd ((x,y+1),path,cost) map) then 
	 			(cost+1,path^"R")
   else if (y > 0)        andalso ((cost+2)<prev_cost) andalso (isEnd ((x,y-1),path,cost) map) then 
				(cost+2,path^"L")
   else if (x > 0)        andalso ((cost+3)<prev_cost) andalso (isEnd ((x-1,y),path,cost) map) then 
	 			(cost+3,path^"U")
	 else 		(prev_cost,prev_path)

		else
		if (x < rowLimit) andalso (valid (x+1,y) map (cost+1) spaceList) then 
			let
				val spaceList = insertToList spaceList ((x,y),path,cost) endFlag
			in
				searchPath ((x+1,y),path^"D",cost+1) map spaceList
			end
   else if (y < colLimit) andalso (valid (x,y+1) map (cost+1) spaceList) then 
	 		let
				val spaceList = insertToList spaceList ((x,y),path,cost) endFlag
			in
				searchPath ((x,y+1),path^"R",cost+1) map spaceList
			end
   else if (y > 0)        andalso (valid (x,y-1) map (cost+2) spaceList) then 
			let
				val spaceList = insertToList spaceList ((x,y),path,cost) endFlag
			in
				searchPath ((x,y-1),path^"L",cost+2) map spaceList
			end
   else if (x > 0)        andalso (valid (x-1,y) map (cost+3) spaceList) then 
	 		let
				val spaceList = insertToList spaceList ((x,y),path,cost) endFlag
			in
				searchPath ((x-1,y),path^"U",cost+3) map spaceList
			end
	 else 		searchPath ((0,0),"",~1) map spaceList
	end



(* initialises search *)
fun startPath (map,(startX,startY)) =

		searchPath ((startX,startY),"",0) map []


(* final function *)
fun moredeli file =
	let
		val spaceMap = makeMap file
	in
		startPath spaceMap
	end