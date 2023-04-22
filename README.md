# linux-amd-color-temperature-control

Many thanks to https://mina86.com/2019/srgb-xyz-matrix/ and https://arjun.lol/notes/clamping-wcg-displays-to-srgb-in-linux/, I basically reimplemented his C# code in python.
NB: In contrast to this article, cmdemo is not needed, this can also directly be set via xrandr.

This python script uses the color primaries of a monitor (to be found in EDID data or possibly in some sort of monitor profile you measured using, possibly, argyllcms) and generates a xrandr call to clamp this wide color gamut monitor to sRGB.
This can then be used in udev hotplug scripts (see examples).

Example:

```
$ python3 srgb-xyz-matrix.py -r 0.6777,0.3144 -g 0.2714,0.6328 -b 0.1484,0.0556 -w 0.3134,0.3291 -o DisplayPort-1
xrandr --verbose --output DisplayPort-1 --set CTM '-598257770,0,561864587,0,10554227,0,160761477,0,-185955614,0,31903097,0,46902368,0,64628669,0,-100560476,0'
```

After you have this command, use the scripts / udev integrations in the repo. Also call set-color-management.sh from your .profile or .xprofile or .bashrc or whatever is called when you log into X.
