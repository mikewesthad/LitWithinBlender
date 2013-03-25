import bpy

import sys
sys.path.append("C:\\Users\\mikewesthad\\Documents\\Git Projects\\LitWithinBlender")

import imp
import NeuralNetwork
imp.reload(NeuralNetwork)
import NeuralNetwork


numberCells = 1

micronsPerBlenderUnit = 1000.0

boxWidth    = 1000.0
boxHeight   = 1000.0
boxDepth    = 1000.0

n = NeuralNetwork.Network(boxWidth, boxHeight, boxDepth, micronsPerBlenderUnit, numberCells)
n.buildNetwork()
