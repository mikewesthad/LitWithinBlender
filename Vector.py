class Vector:

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    """
    Vector functions:
         normalize()
         length()
         leftXYPerpendicular()
         rightXYPerpendicular()
         toList()
    """
    def normalize(v):
        return v.__div__(v.length())
        
    def length(v):
        return (v.x**2 + v.y**2 + v.z**2)**0.5

    def distance(v1, v2):
        return ((v2.x-v1.x)**2.0 + (v2.y-v1.y)**2.0 + (v2.z-v1.z)**2.0)**0.5

    def copyVector(v1):
        v2 = Vector(v1.x, v1.y, v1.z)
        return v2

    def leftXYPerpendicular(v1):
        v2 = Vector()
        v2.x = -v1.y
        v2.y = v1.x
        return v2
        
    def rightXYPerpendicular(v1):
        v2 = Vector()
        v2.x = v1.y
        v2.y = -v1.x
        return v2

    def toList(v):
        return [v.x, v.y, v.z]
            

    """
    Vector operations:
        +, - (add/sub elementwise or by scaler
        * (cross product or multiplication by scaler)
        - (negative)
        / (division by a scaler)
    """
    def __add__(v1, v2):
        if (type(v2) is int) or (type(v2) is float):
            v2 = Vector(v2, v2, v2)
        v3 = Vector()
        v3.x = v1.x + v2.x
        v3.y = v1.y + v2.y
        v3.z = v1.z + v2.z
        return v3

    def __sub__(v1, v2):
        if (type(v2) is int) or (type(v2) is float):
            v2 = Vector(v2, v2, v2)
        v3 = Vector()
        v3.x = v1.x - v2.x
        v3.y = v1.y - v2.y
        v3.z = v1.z - v2.z
        return v3
    
    def __mul__(v1, v2):
        if (type(v2) is int) or (type(v2) is float):
            v2 = Vector(v2, v2, v2)
        v3 = Vector()
        v3.x = v1.x * v2.x
        v3.y = v1.y * v2.y
        v3.z = v1.z * v2.z
        return v3

    def __div__(v1, scaler):
        v2 = Vector()
        v2.x = v1.x / scaler
        v2.y = v1.y / scaler
        v2.z = v1.z / scaler
        return v2

    def __neg__(v1):
        v2 = Vector()
        v2.x = -v1.x
        v2.y = -v1.y
        v2.z = -v1.z
        return v2

    
    """
    Conversion to string
    """
    def __str__(self):
        return "<%.4f, %.4f, %.4f>" % (self.x, self.y, self.z)
