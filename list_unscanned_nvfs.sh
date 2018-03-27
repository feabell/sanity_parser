#!/bin/bash

find . -mindepth 1 -maxdepth 1 -type d '!' -exec test -e "{}/hosts.txt" ';' -print | xargs -l -I {} wc -l '{}'/targets.txt | sort -n
