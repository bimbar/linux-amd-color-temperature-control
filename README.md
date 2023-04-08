# linux-amd-color-temperature-control

Many thanks to https://mina86.com/2019/srgb-xyz-matrix/ and https://arjun.lol/notes/clamping-wcg-displays-to-srgb-in-linux/, I basically reimplemented his C# code in python.

This is not really coded for general usability, but it's a fair starting point for anyone who wants to do this himself and is able to do a little bit of programming.

This python script uses the color primaries of a monitor (to be found in EDID data) and generates a cmdemo call to clamp this wide color gamut monitor to sRGB. This can then be used in .xprofile or something similar so it runs at login.

Usage: insert your monitor parameters into the python script at the bottom and run it.
