#!/bin/bash

set -e


# this is strictly necessary, thanks to https://bbs.archlinux.org/viewtopic.php?id=275921 for the information
xrandr -v

HDMI_STATUS=$(</sys/class/drm/card0/card0-HDMI-A-1/status )
DP0_STATUS=$(</sys/class/drm/card0/card0-DP-1/status )
DP1_STATUS=$(</sys/class/drm/card0/card0-DP-2/status )
DP2_STATUS=$(</sys/class/drm/card0/card0-DP-3/status )


if [ "connected" == "$DP0_STATUS" ]; then
  /usr/local/bin/cmdemo -o DisplayPort-0 -d srgb -r srgb -c 0.8607072584788248:0.1308192935107282:0.002457347614982036:0.03743019834381469:0.9567038347644772:0.007428018830419113:0.010920308603581723:0.015047534786493504:0.9765864397737002
fi

if [ "connected" == "$DP1_STATUS" ]; then
  /usr/local/bin/cmdemo -o DisplayPort-1 -d srgb -r srgb -c 0.8004236866104514:0.19540486818956676:-0.0012929300057034504:0.03273664054967407:0.9675085554051026:0.0013553486503847998:0.01676768832134682:0.053925117588655556:0.9317730775838571
fi



