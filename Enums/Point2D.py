class Point2D:
    # Integer 2D coordinates
    # The (0,0) of the coordinates is top-left corner

    def __init__(self, h=0, w=0):
        self._h = h
        self._w = w

    def __str__(self): return f"({self._h},{self._w})"

    __repr__ = __str__

    @property
    def h(self): return self._h

    @property
    def w(self): return self._w

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self._h == other.h and self._w == other.w
        return NotImplemented

    def __pos__(self): return Point2D(self._h, self._w)

    def __neg__(self): return Point2D(-self._h, -self._w)

    def __add__(self, other):
        if isinstance(self, other.__class__):
            return Point2D(self._h + other.h, self._w + other.w)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(self, other.__class__):
            return self + (-other)
        return NotImplemented

    def __hash__(self): return hash((self._h, self._w))

    def __mul__(self, other):
        if (isinstance(other, int)):
            return Point2D(other * self._h, other*self._w)
        return NotImplemented

    def __rmul__(self, other): return self * other

    def __imul__(self, other):
        if (isinstance(other, int)):
            return self * other  # self *= other
        return NotImplemented
