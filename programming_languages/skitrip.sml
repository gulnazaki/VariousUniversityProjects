(* NONE LIST REVERSE *)


(* Melistas Thomas *)
(* Patris Nikolas *)


(* Parse file function returns a list of a one integer and two list, the second reversed from the first *)
(* fn : string -> int * (int list * int list) *)

(*file input parser, output (len,list,reverse_list)*)
fun parse file =
    let
    (* a function to read an integer from an input stream *)
        fun next_int input =
        Option.valOf (TextIO.scanStream (Int.scan StringCvt.DEC) input)
    (* open input file and read the two integers in the first line *)
        val stream = TextIO.openIn file
        val n = next_int stream
        val _ = TextIO.inputLine stream
    (* a function to read the pair of integer & real in subsequent lines *)
        fun scanner (0,x,y) = (x,y)
          | scanner (i,x,y) =
            let
                val d = next_int stream
            in
                scanner (i - 1,x @ [d],d::y)
            end
    in
        (n,  scanner (n,nil,nil))
    end

(*Getter: len of input*)
fun get_len (x : int * (int list * int list)) = #1 x

(*Getter: input list*)
fun get_input (x : int * (int list * int list)) = #1 (#2 x)

(*Getter: reverse input list*)
fun get_rinput (x : int * (int list * int list)) = #2 (#2 x)

(*Getter: index value*)
fun get_indx (x: (int * int )) = #1 x;

(*Getter: heigt value*)
fun get_hgt (x: (int * int )) = #2 x;

(*Progressively larger height: returns (index,height)*)
fun lrg_indx (nil, len) = raise Empty
    | lrg_indx ((x::xs), len) =
        let
            fun lrg (nil, max, index, acc) = acc
                | lrg (y::ys, max, index, acc) =
                    if (y > max) then lrg (ys, y, index - 1, (index - 1,y)::acc )
                    else lrg (ys, max, index - 1, acc)
        in
            lrg (xs, x, len, [(len,x)])
        end;

(*Progressively smaller height: returns  (index,height)*)
fun sml_indx nil = raise Empty
    | sml_indx (x::xs) =
        let
            fun sml (nil, min, index, acc) = acc
                | sml (y::ys, min, index, acc) =
                    if (y < min) then sml (ys, y, index + 1, acc @ [(index + 1,y)])
                    else sml (ys, min, index + 1, acc)
        in
            sml (xs, x, 1, [(1,x)])
        end;

(* Calculate the max distance between one height and all the heights that list contains *)
(* Return the difference between their indexes *)
fun max_endn (x,min_indx,min_hgt) =
        let
            fun endn (nil, w) = w
                | endn (y::ys, w) =
                    if ((get_indx y) > min_indx) andalso ((get_hgt y) > min_hgt) then
                        endn (ys,get_indx y)
                    else
                        endn (ys,w)
        in
            endn (x, 0)
        end;


(* startl: list with progressively larger indexes,heights *)
(* endl: list with progressively smaller indexes,heights *)
fun max_dist (startl: (int * int) list, endl: (int * int) list ) =
    let
        fun str (nil, z) = z
            | str (x::xs,z) =
                let
                    val min_hgt = get_hgt x
                    val min_indx = get_indx x
                    val diff = max_endn (startl,min_indx,min_hgt) - min_indx
                in
                    if (diff > z) then str(xs,diff) else str(xs,z)

                end
    in
        str (endl, 0)
    end;


(* final function *)
fun skitrip file =
    let
        val input = parse file
        val len = get_len input
        val l = get_input input
        val rl = get_rinput input
        val sl = sml_indx l
        val ll = lrg_indx (rl,len)
    in
        max_dist (ll,sl)
    end;
