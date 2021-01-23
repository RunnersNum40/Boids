import numpy as np
import math

def is_iterable(A):
    """Check whether object A is interable"""
    try:
        A[0]
        return True
    except:
        return False

class Vector:
    """A variable dimension vector class"""
    @classmethod
    def from_dir(cls, direction, magnitude):
        """Create a Vector inctance from an angle and magnitude"""
        return cls(np.cos(direction)*magnitude, np.sin(direction)*magnitude)

    def __init__(self, components,*args):
        if is_iterable(components):
            self.vec = np.array(components, dtype=np.float32)
        else:
            self.vec = np.array([components, *args], dtype=np.float32)

        self.ndims = self.vec.shape[0]

    @property
    def x(self):
        return self.vec[0]

    @property
    def y(self):
        return self.vec[1]

    @property
    def z(self):
        return self.vec[2]

    @property
    def angle(self):
        if self.ndims != 2: raise Exception(f"Error Vector with {self.ndims} dimensions cannot have angle")
        return np.arctan2(self.vec[1], self.vec[0])%(2*math.pi)

    @angle.setter
    def angle(self, angle):
        if self.ndims != 2: raise Exception(f"Error Vector with {self.ndims} dimensions cannot have angle")
        return self.from_dir(angle, abs(self))

    @property
    def magnitude(self):
        return abs(self)

    @magnitude.setter
    def magnitude(self, new):
        if abs(self) == 0:
            raise Exception("Cannot scale a vector (0, 0)")
        self /= abs(self)*new

    def __add__(self, other):
        if type(other) == type(self):
            return Vector(self.vec+other.vec)
        else:
            raise Exception("Error: Cannot add or subtract non-vector with vector")

    def __mul__(self, factor):
        if type(factor) == type(self):
            return sum(np.multiply(self.vec, factor.vec))
        else:
            return Vector(self.vec*factor)

    def __truediv__(self, divisor):
        return self*(1/divisor)

    def __sub__(self, other):
        return self+(-other)

    def __neg__(self):
        return Vector(-self.vec)

    def __abs__(self):
        """Return the magnitude of the self"""
        return math.sqrt(np.sum(self.vec**2))

    def __index__(self, index):
        return self.vec[index]

    def __iter__(self):
        return self.vec.__iter__()

    def __str__(self):
        return "Vector({})".format(", ".join(map(str, self.vec)))

if __name__ == '__main__':
    v1 = Vector(0, 1)
    v2 = Vector(1, 0)
    print(v1, v2)
    print(v1+v2)
    print((v1+v2)/2)