set opt(nam) "lab5.nam"
set opt(tr) "lab5.tr"
set opt(seed) 0
set opt(starttraf) 0.4
set opt(stoptraf) 1.1
set opt(stopsim) 2.2
set opt(node) 15
set opt(qsize) 200
set opt(bw) 10000000
set opt(delay) 0.0000128
set opt(packetsize) 1500
set opt(rate) [expr 3*$opt(bw)/$opt(node)]

set opt(ll) LL
set opt(ifq) Queue/DropTail
set opt(mac) Mac/802_3
set opt(chan) Channel

proc create-topology {} {
	global ns opt
	global lan node

	set num $opt(node)

	for {set i 0} {$i < $num} {incr i} {
		set node($i) [$ns node]
		lappend nodelist $node($i)
	}

	set lan [$ns newLan $nodelist $opt(bw) $opt(delay) -llType $opt(ll) -ifqType $opt(ifq) -macType $opt(mac) -chanType $opt(chan)]
}

proc create-connections {} {
	global ns opt
	global node udp sink cbr
	for {set i 1} {$i < $opt(node)} {incr i} {
		set udp($i) [new Agent/UDP]
		$udp($i) set fid_ $i
		$udp($i) set packetSize_ $opt(packetsize)
		$ns attach-agent $node($i) $udp($i)
		set sink($i) [new Agent/Null]
		$ns attach-agent $node(0) $sink($i)
		$ns connect $udp($i) $sink($i)
		set cbr($i) [new Application/Traffic/CBR]
		$cbr($i) set rate_ $opt(rate)
		$cbr($i) set packetSize_ $opt(packetsize)
		$cbr($i) set random_ 1
		$cbr($i) attach-agent $udp($i)
		$ns at $opt(starttraf) "$cbr($i) start"
		$ns at $opt(stoptraf) "$cbr($i) stop"
	}
}

proc create-nam-trace {} {
	global ns opt
	set namf [open $opt(nam) w]
	$ns namtrace-all $namf
	return $namf
}

proc create-trace {} {
	global ns opt
	set trf [open $opt(tr) w]
	$ns trace-all $trf
	return $trf
}

proc finish {} {
	global ns trf namf
	$ns flush-trace
	close $trf
	close $namf
	exit 0
}

## MAIN ##
set ns [new Simulator]
set trf [create-trace]
set namf [create-nam-trace]
create-topology
create-connections
$ns at $opt(stopsim) "finish"

$ns run