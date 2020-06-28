#!/usr/bin/env bash

while true; do nc -l 7777 > /dev/hidg0 ; done