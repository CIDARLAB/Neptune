#!/bin/bash


mkdir $1
cd $1
#Loop from 1 to 500 and print the number
for i in {1..10}; do
    
    touch "${i}.txt"
done