#!/bin/bash

# checks .riceable programs against the programs installed on the system
# tested on archlinux and debian jessie

> ~/.ricebowl/.pkgs # empties .pkgs

INSTALLED=()  # an array of all the commands
readarray RICEABLE < ~/.ricebowl/.riceable

IFS=: read -ra dirs_in_path <<< "$PATH"
for dir in "${dirs_in_path[@]}"; do
        for file in "$dir"/*; do
                [[ -x $file && -f $file ]] && INSTALLED+=("${file##*/}") #printf '%s\n' "${file##*/}"
        done
done

echo "riceable programs:" # installed && riceable
for rice in ${RICEABLE[@]}; do
        for i in ${INSTALLED[@]}; do
                if [ "$i" == "$rice" ] ; then
                        echo $rice | tee -a ~/.ricebowl/.pkgs; break;
                fi
        done
done
