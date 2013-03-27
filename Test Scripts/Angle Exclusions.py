import random

def exludeRange(allowableRanges, exludeRange):
    eStart  = exludeRange[0]
    eEnd    = exludeRange[1]

    newAllowableRanges = []

    for allowableRange in allowableRanges:
        aStart  = allowableRange[0]
        aEnd    = allowableRange[1]

        # The exclusion range is contained within the allowable range
        if aStart < eStart and aEnd > eEnd:
            newAllowableRanges.append([aStart, eStart])
            newAllowableRanges.append([eEnd, aEnd])

        # The exlusion range does not overlap with the allowable range
        elif aStart > eEnd or aEnd < eStart:
            newAllowableRanges.append([aStart, aEnd])
        
        # The allowable range is contained within the exlusion range
        elif aStart >= eStart and aEnd <= eEnd:
            pass

        # There is a partial overlap between the allowable range and the exclusion range
        else:
            if aStart >= eStart:
                newAllowableRanges.append([eEnd, aEnd])
            elif aEnd <= eEnd:
                newAllowableRanges.append([aStart, eStart])

    return newAllowableRanges


def generateRandomInAllowableRanges(allowableRanges):
    totalAngle = 0.0
    for i in allowableAngles:
        totalAngle += i[1] - i[0]

    rand = random.uniform(0, totalAngle)
    totalAngle = 0.0
    for i in allowableAngles:
        if totalAngle < rand < totalAngle + i[1] - i[0]:
            return i[0]+rand-totalAngle
        totalAngle += i[1] - i[0]



allowableAngles = [[0.0, 360.0]]

excludeAngles = []
for i in range(10):
    sAngle = random.uniform(-40, 400)
    eAngle = sAngle + random.uniform(0, 45)
    excludeAngles.append([sAngle, eAngle])

for e in excludeAngles:
    allowableAngles = exludeRange(allowableAngles, e)
print allowableAngles

for i in range(10000000):
    rand = generateRandomInAllowableRanges(allowableAngles)
    
    isInsideAllowable = False
    for aRange in allowableAngles:
        if aRange[0] <= rand and rand <= aRange[1]:
            isInsideAllowable = True

    isInsideExcluded = False
    for eRange in excludeAngles:
        if eRange[0] <= rand and rand <= eRange[1]:
            isInsideExcluded = True

    if not(isInsideAllowable) or isInsideExcluded:
        print "Shiiiit", rand
    
