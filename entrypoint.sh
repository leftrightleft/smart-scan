#!/bin/sh -l

echo "Heldlo $1"
time=$(date)
echo "time=$time" >> $GITHUB_OUTPUT