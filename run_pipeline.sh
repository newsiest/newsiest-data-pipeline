#!/bin/bash
last_updated="$(cat last_updated.txt 2> /dev/null)"
python main.py "$last_updated" && echo "$(date)" > last_updated.txt