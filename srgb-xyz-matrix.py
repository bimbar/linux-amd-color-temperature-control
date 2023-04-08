# Many thanks to https://arjun.lol/notes/clamping-wcg-displays-to-srgb-in-linux/
# and https://mina86.com/2019/srgb-xyz-matrix/

import numpy as np

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

sRGB = ColorSpace(Point(0.64, 0.33), Point(0.3, 0.6), Point(0.15, 0.06), D65)
P3Display = ColorSpace(Point(0.68, 0.32), Point(0.265, 0.69), Point(0.15, 0.06), D65)

# Gigabyte M28u
#    Red  : 0.6777, 0.3144
#    Green: 0.2714, 0.6328
#    Blue : 0.1484, 0.0556
#    White: 0.3134, 0.3291
M28u = ColorSpace(Point(0.6777, 0.3144), Point(0.2714, 0.6328), Point(0.1484, 0.0556), Point(0.3134, 0.3291))

# Samsung LS27A70
#    Red  : 0.6796, 0.3203
#    Green: 0.2548, 0.6796
#    Blue : 0.1503, 0.0595
#    White: 0.3134, 0.3291
LS27A70 = ColorSpace(Point(0.6796, 0.3203), Point(0.2548, 0.6796), Point(0.1503, 0.0595), Point(0.3134, 0.3291))

matrix = RGBtoRGB(sRGB, M28u)
print("xrandr --verbose --output DisplayPort-0 --set CTM '" + MatrixForXRandR(matrix) + "'")
print("cmdemo -o DisplayPort-0 -d srgb -r srgb -c '" + MatrixForCMDemo(matrix) + "'")

matrix = RGBtoRGB(sRGB, LS27A70)
print("xrandr --verbose --output DisplayPort-1 --set CTM '" + MatrixForXRandR(matrix) + "'")
print("cmdemo -o DisplayPort-1 -d srgb -r srgb -c '" + MatrixForCMDemo(matrix) + "'")
