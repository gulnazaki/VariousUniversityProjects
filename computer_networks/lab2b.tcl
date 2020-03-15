set ns [new Simulator]

set nf [open lab2b.nam w]
set f0 [open out0.tr w]
set f3 [open out3.tr w]
$ns namtrace-all $nf


proc record {} {
global sink0 sink3 f0 f3
set ns [Simulator instance]
set time 0.1
set bw0 [$sink3 set bytes_]
set bw3 [$sink0 set bytes_]
set now [$ns now]
puts $f0 "$now [expr (($bw0/$time)*8)/1000000]"
puts $f3 "$now [expr (($bw3/$time)*8)/1000000]"
$ns at [expr $now+$time] "record"
}

proc finish {} {
    global ns nf f0 f3
    $ns flush-trace
    close $nf
    close $f0
    close $f3
    exit 0
}

for {set i 0} {$i < 10} {incr i} {
  set n($i) [$ns node]
}

for {set i 0 } {$i < 8} {incr i} {
  $ns duplex-link $n($i) $n([expr ($i+1)%8]) 2Mb 30ms DropTail
  $ns cost $n($i) $n([expr ($i+1)%8]) 3
  $ns cost $n([expr ($i+1)%8]) $n($i) 3
}

$ns duplex-link $n(8) $n(3) 2Mb 10ms DropTail
$ns cost $n(8) $n(3) 1
$ns cost $n(3) $n(8) 1
$ns duplex-link $n(8) $n(4) 2Mb 10ms DropTail
$ns cost $n(8) $n(4) 1
$ns cost $n(4) $n(8) 1
$ns duplex-link $n(9) $n(4) 2Mb 10ms DropTail
$ns cost $n(9) $n(4) 1
$ns cost $n(4) $n(9) 1
$ns duplex-link $n(9) $n(6) 2Mb 30ms DropTail
$ns cost $n(9) $n(6) 3
$ns cost $n(6) $n(9) 3

set udp0 [new Agent/UDP]
$udp0 set packetSize_ 1500
$ns attach-agent $n(0) $udp0
$udp0 set fid_ 0
$ns color 0 red
set sink0 [new Agent/LossMonitor]
$ns attach-agent $n(0) $sink0

set udp3 [new Agent/UDP]
$udp3 set packetSize_ 1500
$ns attach-agent $n(3) $udp3
$udp3 set fid_ 3
$ns color 3 blue
set sink3 [new Agent/LossMonitor]
$ns attach-agent $n(3) $sink3

$ns connect $udp0 $sink3
$ns connect $udp3 $sink0

set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetSize_ 1500
$cbr0 set interval_ 0.025
$cbr0 attach-agent $udp0

set exp3 [new Application/Traffic/Exponential]
$exp3 set packetSize_ 1500
$exp3 set rate_ 750k
$exp3 attach-agent $udp3


$ns at 0.0 "record"
$ns at 0.4 "$cbr0 start"
$ns at 1.0 "$exp3 start"
$ns at 24.9 "$exp3 stop"
$ns at 24.9 "$cbr0 stop"
$ns at 25.0 "finish"
$ns run
