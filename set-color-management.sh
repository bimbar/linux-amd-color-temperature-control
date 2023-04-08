#!/bin/bash

set -e


# this is strictly necessary, thanks to https://bbs.archlinux.org/viewtopic.php?id=275921 for the information
xrandr -v

HDMI_STATUS=$(</sys/class/drm/card0/card0-HDMI-A-1/status )
DP0_STATUS=$(</sys/class/drm/card0/card0-DP-1/status )
DP1_STATUS=$(</sys/class/drm/card0/card0-DP-2/status )
DP2_STATUS=$(</sys/class/drm/card0/card0-DP-3/status )


if [ "connected" == "$DP0_STATUS" ]; then
  xrandr --verbose --output DisplayPort-0 --set CTM '-598257770,0,561864587,0,10554227,0,160761477,0,-185955614,0,31903097,0,46902368,0,64628669,0,-100560476,0'
fi

if [ "connected" == "$DP1_STATUS" ]; then
  xrandr --verbose --output DisplayPort-1 --set CTM '-857173740,0,839257518,0,5553092,0,140602800,0,-139549692,0,5821178,0,72016672,0,231606616,0,-293032401,0'
fi



