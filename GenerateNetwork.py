import bpy

import sys
sys.path.append("C:\\Users\\mikewesthad\\Documents\\Git Projects\\LitWithinBlender")

import imp
import NeuralNetwork
imp.reload(NeuralNetwork)
import NeuralNetwork

n = NeuralNetwork.Network(1, 1, 1, 1)
n.buildNetwork()
