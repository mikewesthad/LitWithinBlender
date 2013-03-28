import imp
import Neuron
imp.reload(Neuron)
from Neuron import Neuron
import Vector
imp.reload(Vector)
from Vector import Vector

n = Neuron(Vector(100,200,0), 1)
n.growDendrites()
n.buildNeuronMesh()
