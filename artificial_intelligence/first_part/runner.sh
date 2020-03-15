#!/bin/bash

given=( 1 5 10 20 30 40 50 75 100 125 150 200 300 400 500 600 )
ours=( 1 5 10 20 30 40 50 75 100 125 150 200 250 300 )

for i in "${given[@]}"
do
	java Taxibeat client.csv taxis.csv nodes.csv $i given
done

for i in "${ours[@]}"
do
	java Taxibeat ourclient.csv ourtaxis.csv nodes.csv $i ours
done