from bmatrix.geometry import Vec2

from math import sqrt, floor
from string import digits, ascii_letters, punctuation
from random import sample, randint
from collections import deque


TRACE_COLOR_CLASSIC = 0x37, 0x71, 0x37
KATAKANA = 'ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ'
ALPHABET = punctuation + digits + ascii_letters + KATAKANA


def trace_color(random=False):
    if random:
        return randint(0, 0xff), randint(0, 0xff), randint(0, 0xff)
    
    return TRACE_COLOR_CLASSIC


class Particle:
    def __init__(self, x, y, dx, dy, m=1, radius=0.505, trace_limit=10, 
                 trace_color=trace_color(), allow_go_away=False, 
                 head_color=(0xff, 0xff, 0xff)):
        self._pos = Vec2(x, y)
        self._vel = Vec2(dx, dy)
        self._m = m
        self._radius = radius
        self._time = 0
        self.__char = 0
        self.__alphabet = sample(ALPHABET, len(ALPHABET))
        self.__trace_limit = randint(5, trace_limit)
        self.__trace = deque()
        self.__trace_color = trace_color
        self.__remove_me = False
        self.__allow_go_away = allow_go_away
        self.__head_color = head_color


    def char(self):
        return self.__alphabet[self.__char]


    def position(self):
        return self._pos


    def velocity(self):
        return self._vel


    def mass(self):
        return self._m


    def radius(self):
        return self._radius


    def remove_me(self, val=None):
        if val is None:
            return self.__remove_me
        
        self.__remove_me = val


    def trace_color(self, val):
        self.__trace_color = val


    def trace_limit(self):
        return self.__trace_limit

    
    def allow_go_away(self, val):
        self.__allow_go_away = val


    def head_color(self, val):
        self.__head_color = val


    def collide(self, other):
        dist = self._radius + other.radius()
        pos = self._pos.sub(other.position())
        return pos.dot(pos) <= dist ** 2


    def align(self, other, stage):
        dist = self._radius + other._radius
        delta_pos = self._pos.sub(other._pos)
        delta_vel = self._vel.sub(other._vel)
        a = delta_vel.dot(delta_vel)
        b = delta_pos.dot(delta_vel) * 2
        c = delta_pos.dot(delta_pos) - dist * dist
        time = (-b - sqrt(b * b - 4 * a * c)) / (2 * a)

        self._append_trace(self._pos, stage)
        self._append_trace(other._pos, stage)

        self._pos = self._pos.add(self._vel.scale(time))
        other._pos = other._pos.add(other._vel.scale(time))
        self._time = other._time = -time


    def bounce(self, other):
        dist = self._radius + other._radius
        delta_pos = self._pos.sub(other._pos)
        delta_vel = self._vel.sub(other._vel)
        factor = 2 * delta_vel.dot(delta_pos) / (dist * dist * (self._m + other._m))

        self._vel = self._vel.sub(delta_pos.scale(factor * other._m))
        other._vel = other._vel.add(delta_pos.scale(factor * self._m))

        other._pos = other._pos.add(other._vel.scale(other._time))
        self._pos = self._pos.add(self._vel.scale(self._time))


    def update(self, stage):
        width, height = stage.width(), stage.height()
        pos, vel, radius = self._pos, self._vel, self._radius

        if (pos.x <= radius and vel.x < 0) or (pos.x >= width and vel.x > 0):
            if not self.__allow_go_away:
                vel.x = -vel.x

        if (pos.y <= radius and vel.y < 0) or (pos.y >= height and vel.y > 0):
            if not self.__allow_go_away:
                vel.y = -vel.y

        tmp = pos.clone()
        self._pos = pos.add(vel)

        if int(tmp.x) != int(self._pos.x) or int(tmp.y) != int(self._pos.y):
            self._append_trace(tmp, stage)
            self.__char += 1
            if self.__char >= len(self.__alphabet):
                self.__char = 0


    def _append_trace(self, pos, stage):
        trace = self.__trace
        trace.appendleft((self.char(), pos, self.__trace_color))
        if len(trace) > self.__trace_limit:
            _, pos, _ = trace.pop()
            term = stage.terminal()
            pos = pos.ensure_int()
            with term.location(pos.x, pos.y):
                print(' ', end='')


    def __draw_trace(self, stage):
        trace = self.__trace
        for item in trace:
            stage.put_pixel(*item)


    def draw(self, stage):
        self.__draw_trace(stage)
        stage.put_pixel(self.char(), self._pos, self.__head_color)


    def __str__(self):
        return f'pos = {self._pos}, vel = {self._vel}'


    def __repr__(self):
        return f'Particle({self._pos.x}, {self._pos.y}, {self._vel.x}, {self._vel.y})'
