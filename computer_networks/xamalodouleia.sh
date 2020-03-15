#!/bin/bash
## we learn programming for a reason

sed -i "7s/.*/set opt(node) 15/" lab5.tcl

mkdir -p packetsizes
 for packetsize in 64 128 200 300 400 500 600 700 800 900 1000 1100 1200 1300 1400 1500; do
 	sed -i "11s/.*/set opt(packetsize) $packetsize/" lab5.tcl
 	ns lab5.tcl
 	awk -f lab5.awk < lab5.tr > packetsizes/results_$packetsize.txt
 done

 mkdir -p nodes
 for node_nr in 5 10 15 20; do
 	sed -i "7s/.*/set opt(node) $node_nr/" lab5.tcl
 	ns lab5.tcl
 	awk -f lab5.awk < lab5.tr > nodes/results_$node_nr.txt
 done