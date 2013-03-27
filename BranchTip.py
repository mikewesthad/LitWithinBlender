import math as m
import random as r

import imp

import Vector
imp.reload(Vector)
from Vector import Vector


    # Don't forget to force heading into [0, 360]

class DendriteTip:
    def __init__(heading, headingRange, stepSize, resources, maxResources,
                 startThickness, endThickness, startPosition,
                 cellCenter, neuron):

        self.heading        = heading
        self.headingRange   = headingRange
        self.stepSize       = stepSize
        self.resources      = resources
        self.maxResources   = maxResources
        self.startThickness = startThickness
        self.endThickness   = endThickness
        self.cellCenter     = cellCenter
        self.neuron         = neuron

        self.p1 = startPosition
        self.p2 = None
        self.v1 = None
        self.v2 = None
        self.v3 = None
        self.v4 = None

        self.growing = True

        self.points     = []
        self.vertices   = []

    def isGrowing(self):
        return self.growing

    def grow(self, stepSize=None, heading=None, headingRange=None):
        if self.growing:
            if heading==None:       heading         = self.heading
            if headingRange==None:  headingRange    = self.headingRange
            if stepSize==None:      stepSize        = self.stepSize

            if self.p2 == None:
                initializeGrowth(stepSize, heading, headingRange)
            else:
                regularGrowth(stepSize, heading, headingRange)

    def initializeGrowth(self, stepSize, heading, headingRange):        
        self.p2     = Vector()
        self.p2.x   = m.cos(m.radians(heading)) * stepSize + self.p1.x
        self.p2.y   = m.sin(m.radians(heading)) * stepSize + self.p1.y
        
        thickness = (self.resources/self.maxResources) * (self.startThickness - self.endThickness) + self.endThickness
        halfThickness = thickness / 2.0

        t           = self.p1 - self.cellCenter
        leftPerp    = t.leftXYPerpendicular().normalize()
        rightPerp   = t.rightXYPerpendicular().normalize()
        self.v1     = leftPerp * halfThickness + self.p1
        self.v4     = rightPerp * halfThickness + self.p1

        t           = self.p2 - self.p1
        leftPerp    = t.leftXYPerpendicular().normalize()
        rightPerp   = t.rightXYPerpendicular().normalize()
        self.v2     = leftPerp * halfThickness + self.p2
        self.v3     = rightPerp * halfThickness + self.p2

        self.vertices   = self.vertices + [self.v1] + [self.v2] + [self.v3] + [self.v4]
        self.points     = self.points + [self.p1] + [self.p2]
        
        self.resources -= stepSize
        if self.resources <= 0: self.growing = False


    def regularGrowth(self, stepSize=None, heading=None, headingRange=None):
        # Start growing from the last dendrite points (deep copies)
        self.p1 = self.p2.copyVector()
        self.v1 = self.v2.copyVector()
        self.v4 = self.v3.copyVector()

        # Unlink any references that exist
        self.p2 = Vector()
        self.v2 = Vector()
        self.v3 = Vector()
        
        # Map the resources remaining into the range of thickness values to obtain the current thickness
        thickness       = remap(self.resources, 0.0, self.maxResources, self.startThickness, self.endThickness)
        halfThickness   = thickness / 2.0

        # Generate a random heading
        heading += r.uniform(-self.headingRange, self.headingRange)

        # Find p2 by moving in the heading direction
        self.p2.x = self.p1.x + m.cos(m.radians(heading)) * stepSize
        self.p2.y = self.p1.y + m.sin(m.radians(heading)) * stepSize

        # Calculate the new vertices of the quad (adding thickness relative to p2)
        t           = self.p2 - self.p1
        leftPerp    = t.leftXYPerpendicular().normalize()
        rightPerp   = t.rightXYPerpendicular().normalize()
        self.v2     = leftPerp * halfThickness + self.p2
        self.v3     = rightPerp * halfThickness + self.p2

        # Store the new vertices and the new point
        self.vertices   = self.vertices + [self.v2] + [self.v3]
        self.points     = self.points + [self.p2]
        
        # Update the resources based on distance traveled            
        self.resources -= stepSize        
        if self.resources <= 0: self.growing = False


    def split(self, numberChildren=2, heading=None, headingRange=None, stepSize=None):
        if heading==None:       heading         = self.heading
        if headingRange==None:  headingRange    = self.headingRange
        if stepSize==None:      stepSize        = self.stepSize

        if self.resources < stepSize * numberChildren: return
        
        self.growing    = False
        childResources  = self.resources/numberChildren
        startAngle      = heading - headingRange
        endAngle        = heading + headingRange
        children        = []
                
        for childNumber in range(numberChildren):
            childHeading    = remap(childNumber, 0.0, numberChildren, startAngle, endAngle)
            childPosition   = self.p2.copyVector()  # Create a fresh copy for each child
            
            childBranch = BranchTip(childHeaing, headingRange, stepSize,
                                    childResorces, self.maxResources,
                                    self.startThickness, self.endThickness,
                                    childPosition, self.cellCenter, self.neuron)
            
            childBranch.v1 = self.v2.copyVector()
            childBranch.v4 = self.v3.copyVector()
            childBranch.grow()
            
            children.append(childBranch)
        
        return children
    
            
        
    # Take a value (a) that has range [aMin, aMax] and remap it to the range [bMin, bMax]
    def remap(a, aMin, aMax, bMin, bMax):        
        percent = float(a - aMin) / float(aMax - aMin)
        b       = percent * (bMax - bMin) + bMin
        return b
        
