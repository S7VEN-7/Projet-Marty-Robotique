#!/bin/bash
# this is a completely horrible hack to get the LED device - I have no idea how to get the
# actual device name from /sys/class/leds 
ledPattern="[0-9A-F]{4}:[0-9A-F]{4}:[0-9A-F]{4}\.[0-9A-F]{4}:"
deviceName=`ls -1 /sys/class/leds | grep -E $ledPattern | sed -r "s/:\w+$//" | head -n 1`
function setLED {
echo $1 > /sys/class/leds/$deviceName:$2/brightness
}
# we're going to abuse sin() with a bit of shifting to get a nice colour spectrum
red=0
green=2
blue=4
function getColorVal {
echo "(s($1 * 0.3 + $2) * 127 + 128)/1" | bc -l | sed -r 's/^([0-9]{1,3})(\..+)$/\1/'
}
for i in {0..256}; do
    r=$(getColorVal $i $red)
    g=$(getColorVal $i $green)
    b=$(getColorVal $i $blue)
    setLED $r "red"
    setLED $g "green"
    setLED $b "blue"
    sleep 0.1
done