#!/bin/bash

given=( 50 100 150 200 300 600 1000)
ours=( 50 100 150 200 300 600 1000)

java -cp ".:./jars/jipconsole.jar" TaxiBeatPro client.csv taxis.csv nodes.csv lines.csv traffic.csv 10 2 given yes

for i in "${given[@]}"
do
	java -cp ".:./jars/jipconsole.jar" TaxiBeatPro client.csv taxis.csv nodes.csv lines.csv traffic.csv $i 2 given no
done

java -cp ".:./jars/jipconsole.jar" TaxiBeatPro ourclient.csv ourtaxis.csv nodes.csv lines.csv traffic.csv 10 3 ours yes

for i in "${ours[@]}"
do
	java -cp ".:./jars/jipconsole.jar" TaxiBeatPro ourclient.csv ourtaxis.csv nodes.csv lines.csv traffic.csv $i 3 ours no
done