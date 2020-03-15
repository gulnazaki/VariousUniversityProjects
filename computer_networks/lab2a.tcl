set ns [new Simulator]

$ns color 1 Blue
$ns color 2 Red

set nf [open lab2a.nam w]
$ns namtrace-all $nf

set f0 [open lab2a0.tr w]
set f1 [open lab2a1.tr w]

set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]

$ns duplex-link $n0 $n2 3Mb 8ms DropTail
$ns duplex-link $n1 $n2 3Mb 8ms DropTail
$ns duplex-link $n3 $n2 3Mb 8ms DropTail

$ns duplex-link-op $n0 $n2 orient right-down
$ns duplex-link-op $n1 $n2 orient right-up
$ns duplex-link-op $n2 $n3 orient right

$ns duplex-link-op $n2 $n3 queuePos 0.5


proc record {} {
global sink0 sink1 f0 f1
set ns [Simulator instance]
set time 0.25
set bw0 [$sink0 set bytes_]
set bw1 [$sink1 set bytes_]
set now [$ns now]
puts $f0 "$now [expr $bw0/$time*8/1000000]"
puts $f1 "$now [expr $bw1/$time*8/1000000]"
$sink0 set bytes_ 0
$sink1 set bytes_ 0
$ns at [expr $now+$time] "record"
}

proc finish {} {
    global ns nf f0 f1
    $ns flush-trace
    close $nf
    close $f0
    close $f1
    exit 0
}


set udp0 [new Agent/UDP]
$ns attach-agent $n0 $udp0
$udp0 set class_ 1

set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetSize_ 1500
$cbr0 set interval_ 0.005
$cbr0 attach-agent $udp0

set udp1 [new Agent/UDP]
$ns attach-agent $n1 $udp1
$udp1 set class_ 2

set cbr1 [new Application/Traffic/CBR]
$cbr1 set packetSize_ 1500
$cbr1 set interval_ 0.0045
$cbr1 attach-agent $udp1

set sink0 [new Agent/LossMonitor]
$ns attach-agent $n3 $sink0

set sink1 [new Agent/LossMonitor]
$ns attach-agent $n3 $sink1

$ns connect $udp0 $sink0
$ns connect $udp1 $sink1


$ns at 0.0 "record"
$ns at 0.4 "$cbr0 start"
$ns at 0.8 "$cbr1 start"
$ns at 7.0 "$cbr1 stop"
$ns at 7.5 "$cbr0 stop"
$ns at 8.0 "finish"

$ns run
