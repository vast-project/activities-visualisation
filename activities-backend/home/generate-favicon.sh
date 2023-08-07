#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $SCRIPT_DIR/static/img
convert -density 300 -define icon:auto-resize=256,128,96,64,48,32,16 -background none vast-no-text-500x500.svg vast.ico
inkscape -w 32 -h 32 vast-no-text-500x500.svg -o vast-apple-icon.png
