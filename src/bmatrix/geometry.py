from math import sqrt


class Vec3:
    def __init__(self, *coords):
        if isinstance(coords[0], Vec3):
            coords = coords[0].to_tuple()

        self.x = coords[0]
        self.y = coords[1]
        self.z = coords[2] if len(coords) > 2 else 0


    def clone(self):
        return Vec3(self)


    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z


    def cross(self, other):
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )


    def magnitude(self):
        return sqrt(self.dot(self))


    def sub(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)


    def add(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)


    def normalize(self):
        try:
            return self.scale(1 / sqrt(self.dot(self)))
        except ZeroDivisionError:
            return self


    def scale(self, scalar):
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)


    def translate(self, scalar):
        return Vec3(self.x + scalar, self.y + scalar, self.z + scalar)


    def transpose_xy(self):
        self.x, self.y = self.y, self.x


    def to_tuple(self):
        return self.x, self.y, self.z


    def ensure_int(self):
        self.x = int(self.x)
        self.y = int(self.y)
        self.z = int(self.z)

        return self


    def __mul__(self, other):
        if isinstance(other, Vec3):
            return self.dot(other)
        elif isinstance(other, (int, float)):
            return self.scale(other)
        else:
            raise ValueError('Should be Vec3, int or float')


    def __sub__(self, other):
        if isinstance(other, Vec3):
            return self.sub(other)
        elif isinstance(other, (int, float)):
            return self.translate(-other)
        else:
            raise ValueError('Should be Vec3, int or float')


    def __add__(self, other):
        if isinstance(other, Vec3):
            return self.add(other)
        elif isinstance(other, (int, float)):
            return self.translate(other)
        else:
            raise ValueError('Should be Vec3, int or float')


    def __xor__(self, other):
        return self.cross(other)


    def __getitem__(self, i):
        items = self.x, self.y, self.z
        return items[i]

    
    def __repr__(self):
        return f'Vec3({self.x}, {self.y}, {self.z})'


class Matrix:
    def __init__(self, *items, size=3):
        if items:
            self.__m = [list(items[i: i + size]) for i in range(0, size * size, size)]
        else:
            self.__m = [[0 for _ in range(size)] for _ in range(size)]


    def __getitem__(self, item):
        if isinstance(item, (int, float)):
            return self.__m[int(item)]
        elif isinstance(item, tuple) and len(item) == 2:
            i, j = item
            return self.__m[i][j]
        else:
            raise IndexError(f'Can\'t use specified object for subscript {item}')


    def __setitem__(self, key, value):
        if isinstance(key, (int, float)):
            self.__m[int(key)] = value[:]
        elif isinstance(key, tuple) and len(key) == 2:
            i, j = key
            self.__m[i][j] = value
        else:
            raise IndexError(f'Can\'t use specified object for subscript {item}')


    def __eq__(self, other):
        return self.__m == other.m()


    def __ne__(self, other):
        return self.__m != other.m()


    def m(self):
        return self.__m


    def multiply(self, other):
        if isinstance(other, Matrix):
            m = Matrix()
            for i, row in enumerate(self.__m):
                for j, val in enumerate(row):
                    m[i, j] = self[i, 0] * other[0, j] + self[i, 1] * other[1, j] + self[i, 2] * other[2, j]

            return m
        elif isinstance(other, Vec3):
            v = []
            for row in self.__m:
                a, b, c = row
                v.append(a * other.x + b * other.y + c * other.z)

            return Vec3(*v)
        else:
            raise TypeError('Invalid object type')


    def __mul__(self, other):
        return self.multiply(other)


    def __rmul__(self, other):
        return self.multiply(other)


    def __matmul__(self, other):
        return self.multiply(other)


Vec2 = Vec3
