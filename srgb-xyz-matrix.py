# Copyright 2023 Markus Peter mpeter at mpeter dot name
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Many thanks to https://arjun.lol/notes/clamping-wcg-displays-to-srgb-in-linux/
# and https://mina86.com/2019/srgb-xyz-matrix/


import numpy as np
import argparse as ap


class Point:
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y

class ColorSpace:
	def __init__(self, r = Point(), g = Point(), b = Point(), w = Point()):
		self.r = r
		self.g = g
		self.b = b
		self.w = w

def RGBtoXYZ(colorSpace):
	whiteXYZ = np.array([colorSpace.w.x / colorSpace.w.y, 1, (1 - colorSpace.w.x - colorSpace.w.y) / colorSpace.w.y])
	mPrime = np.array([[colorSpace.r.x / colorSpace.r.y, colorSpace.g.x / colorSpace.g.y, colorSpace.b.x / colorSpace.b.y],
		[1, 1, 1],
		[(1 - colorSpace.r.x - colorSpace.r.y) / colorSpace.r.y, (1 - colorSpace.g.x - colorSpace.g.y) / colorSpace.g.y, (1 - colorSpace.b.x - colorSpace.b.y) / colorSpace.b.y]])
	diagonalVector = np.dot( np.linalg.inv(mPrime), whiteXYZ)
	diagonalMatrix = np.array( [[diagonalVector[0], 0, 0],
								[0, diagonalVector[1], 0],
								[0, 0, diagonalVector[2]]])
	ret = np.dot(mPrime, diagonalMatrix)
	return ret

def XYZtoRGB(colorSpace):
	return np.linalg.inv(RGBtoXYZ(colorSpace))

def RGBtoRGB(cFrom, cTo):
	return np.dot(XYZtoRGB(cTo), RGBtoXYZ(cFrom))

def MatrixForCMDemo(matrix):
	ret = ""
	for row in matrix:
		for column in row:
			if (len(ret) > 0):
				ret = ret + ":"
			ret = ret + str(column)
	return ret

def MatrixForXRandR(matrix):
	ret = ""
	for row in matrix:
		for column in row:
			if (len(ret) > 0):
				ret = ret + ","
			if (column > 0):
				val = int(column * 2**32)
			else:
				val = -int(column * 2**32)
			if (val > 2**31):
				val = val - 2**32
			ret = ret + str(val) + ",0"
	return ret



D65 = Point(0.312713, 0.329016)

monitorType = {}

# sRGB
monitorType["srgb"] = ColorSpace(Point(0.64, 0.33), Point(0.3, 0.6), Point(0.15, 0.06), D65)
# DisplayP3
monitorType["displayp3"] = ColorSpace(Point(0.68, 0.32), Point(0.265, 0.69), Point(0.15, 0.06), D65)
# Gigabyte M28u
monitorType["m28u"] = ColorSpace(Point(0.6777, 0.3144), Point(0.2714, 0.6328), Point(0.1484, 0.0556), Point(0.3134, 0.3291))
# Samsung LS27A70
monitorType["ls27a70"] = ColorSpace(Point(0.6796, 0.3203), Point(0.2548, 0.6796), Point(0.1503, 0.0595), Point(0.3134, 0.3291))


parser = ap.ArgumentParser(description="Generate a CTM matrix to map your monitor's colorspace to sRGB",
                                 formatter_class=ap.ArgumentDefaultsHelpFormatter)
parser.add_argument("-t", help="preconfigured monitor type, for a list use -t help")
parser.add_argument("-r", help="red primary, for example -r 0.6777,0.3144", default="0.64,0.33")
parser.add_argument("-g", help="green primary, for example -g 0.2714,0.6328", default="0.3,0.6")
parser.add_argument("-b", help="blue primary, for example -b 0.1484,0.0556", default="0.15,0.06")
parser.add_argument("-w", help="white point, for example -w 0.312713,0.329016, defaults to D65", default="0.312713,0.329016")
parser.add_argument("-o", help="the xrandr name for the output to be configured", default="DisplayPort-0")
args = parser.parse_args()
config = vars(args)

c = ColorSpace()
c.w = D65

if (config["r"]):
	x,y = config["r"].split(",")
	c.r=Point(float(x), float(y))
if (config["g"]):
	x,y = config["g"].split(",")
	c.g=Point(float(x), float(y))
if (config["b"]):
	x,y = config["b"].split(",")
	c.b=Point(float(x), float(y))
if (config["w"]):
	x,y = config["w"].split(",")
	c.w=Point(float(x), float(y))
if (config["t"] and config["t"] in monitorType.keys()):
	c = monitorType[config["t"]]
elif (config["t"] == "help"):
	for type in monitorType:
		print(type)
	exit()

matrix = RGBtoRGB(monitorType["srgb"], c)

print("xrandr --verbose --output " + config["output"] + " --set CTM '" + MatrixForXRandR(matrix) + "'")
