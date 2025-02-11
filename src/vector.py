

class Vec:

    def __init__(self, x, y, z) :
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other) :
        return Vec(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other) :
        return Vec(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self,  scalar ) :
        return Vec(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __rmul__(self, scalar) :
        return self.__mul__(scalar)

    def dot(self, other) :
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def __str__(self) :
        return f"({self.x}, {self.y}, {self.z})"
    
    def __repr__(self) :
        return f"Vec({self.x}, {self.y}, {self.z})"
    


def make_vecs( obj ) :
    "find vector-like objects are replace them with Vec objects"

    if type(obj) in ( str, int, float ) :
        return
    
    if type(obj) in ( list, tuple ) :
        for item in obj : make_vecs(item)
        return
    
    try : 
        D = obj.__dict__
    except AttributeError :
        return
    
    # replace n_x, n_y, n_z with a Vec(n_x, n_y, n_z)

    xs = [ n for n in D if n.endswith("_x") ]

    for xname in xs :
        name = xname[:-2]
        if hasattr(obj, name + "_y") and hasattr(obj, name + "_z") :
           
            v = Vec(getattr(obj, name + "_x"), 
                    getattr(obj, name + "_y"), 
                    getattr(obj, name + "_z"))
            setattr(obj, name, v)
            delattr(obj, name + "_x")
            delattr(obj, name + "_y")
            delattr(obj, name + "_z")

    # recurse into the object's attributes
    for key in D :
        make_vecs(D[key])

if __name__ == "__main__" :
        a = Vec(1, 2, 3)
        b = Vec(4, 5, 6)
        print(a + b)
        print(a - b)
        print(a * 2)
        print(2 * a )
        print(a.dot(b))
        print(a)
        print(repr(a))