import bpy

import sys
sys.path.append("C:\\Users\\mikewesthad\\Documents\\Git Projects\\LitWithinBlender")

import imp
import NeuralNetwork
imp.reload(NeuralNetwork)
from NeuralNetwork import Network

import Vector
imp.reload(Vector)
from Vector import Vector


numberCells             = 1
micronsPerBlenderUnit   = 1000.0
lightBoxDimensions      = Vector(1, 1, 1) * micronsPerBlenderUnit


n = Network(lightBoxDimensions, micronsPerBlenderUnit, numberCells)
n.buildNetwork()
