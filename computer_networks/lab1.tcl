set ns [new Simulator]
set nf [open lab1.nam w]
$ns namtrace-all $nf

set f [open lab1.tr w]

proc record {} {
global sink f
set ns [Simulator instance]
set time 0.12
set bw [$sink set bytes_]
set now [$ns now]
puts $f "$now [expr ((($bw/$time)*8)/1000000)]"
$sink set bytes_ 0
$ns at [expr $now+$time] "record"
}

proc finish {} {
    global ns nf f
    $ns flush-trace
    close $nf
    close $f
    exit 0
}

set n0 [$ns node]
set n1 [$ns node]
$ns duplex-link $n0 $n1 4Mb 10ms DropTail

set udp0 [new Agent/UDP]
$udp0 set packetSize_ 1500
$ns attach-agent $n0 $udp0

set traffic0 [new Application/Traffic/Exponential]

$traffic0 set packetSize_ 1500
$traffic0 set interval_ 0.01
$traffic0 attach-agent $udp0

set sink [new Agent/LossMonitor]
$ns attach-agent $n1 $sink

$ns connect $udp0 $sink

$ns at 0.0 "record"
$ns at 2.0 "$traffic0 start"
$ns at 22.0 "$traffic0 stop"
$ns at 24.0 "finish"
$ns run
