#!/bin/sh

# Ce script 

kill -9 `ps -aux | grep "python $1" | tr -s " " | cut -d" " -f2`1>/dev/null 2>&1
kill -9 `ps -aux | grep "python $1" | tr -s " " | cut -d" " -f2`1>/dev/null 2>&1
kill -9 `ps -aux | grep "python $1" | tr -s " " | cut -d" " -f2`1>/dev/null 2>&1
rm *.pyc 2>/dev/null 1>/dev/null
