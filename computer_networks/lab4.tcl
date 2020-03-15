set ns [new Simulator]
set nf [open lab4.nam w]
$ns namtrace-all $nf
set trf [open lab4.tr w]
$ns trace-all $trf


proc finish {} {
global ns nf trf
$ns flush-trace
close $nf
close $trf
exit 0
}

set n(0) [$ns node]
set n(1) [$ns node]
$ns at 0.0 "$n(0) label SRPsender_03114149"
$ns at 0.0 "$n(1) label SRPreceiver_03114149"
$ns duplex-link $n(0) $n(1) 120Mb 110ms DropTail
$ns queue-limit $n(0) $n(1) 100
$ns queue-limit $n(1) $n(0) 100

$ns duplex-link-op $n(0) $n(1) orient left

set tcp0 [new Agent/TCP/Reno]
$tcp0 set window_ 61
$tcp0 set windowInit_ 61
$tcp0 set syn_ false
$tcp0 set packetSize_ 4970
$ns attach-agent $n(0) $tcp0
set sink0 [new Agent/TCPSink]
$ns attach-agent $n(1) $sink0
$ns connect $tcp0 $sink0

set ftp0 [new Application/FTP]
$ftp0 attach-agent $tcp0

$ns at 1.3 "$ftp0 start"
$ns at 6.2 "$ftp0 stop"
$ns at 6.5 "finish"
$ns run
