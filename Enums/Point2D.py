class Point2D:
    # Integer 2D coordinates
    # The (0,0) of the coordinates is top-left corner

    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    def __str__(self):
        return f"({self._x},{self._y})"

    __repr__ = __str__

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self._x == other.x and self._y == other.y
        return NotImplemented

    def __pos__(self):
        return Point2D(self._x, self._y)

    def __neg__(self):
        return Point2D(-self._x, -self._y)

    def __add__(self, other):
        if isinstance(self, other.__class__):
            return Point2D(self._x + other.x, self._y + other.y)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(self, other.__class__):
            return self + (-other)
        return NotImplemented

    def __hash__(self):
        return hash((self.x, self.y))
