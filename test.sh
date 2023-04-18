#!/usr/bin/bash

mkdir tmp

rand=$RANDOM
mpirun -n 1 python main.py --seed $rand --method minimax --depth 7 > tmp/1.opt
for i in {2..5}; do
    mpirun -n $i python main.py --seed $rand --method minimax --depth 7 > tmp/$i.opt
    diff tmp/1.opt tmp/$i.opt
done
