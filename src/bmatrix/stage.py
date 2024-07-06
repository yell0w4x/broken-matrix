class TerminalStage:
    def __init__(self, terminal, objects_limit=150):
        self.__term = terminal
        self.__objects_limit = objects_limit
        self.__objects = list()


    def objects(self):
        return self.__objects


    def terminal(self):
        return self.__term


    def width(self):
        return self.__term.width


    def height(self):
        return self.__term.height


    def objects_limit(self, val=None):
        if val is None:
            return self.__objects_limit

        self.__objects_limit = val

    
    def put_pixel(self, char, pos, color):
        term = self.__term
        pos = pos.clone().ensure_int()
        if not (pos.x < self.width() and pos.y < self.height()):
            return

        with term.location(pos.x, pos.y):
            color = term.color_rgb(*color)
            print(f'{color}{char}{term.normal}', end='')


    def clear(self):
        print(self.__term.home + self.__term.clear)


    def add_particle(self, particle):
        self.__objects.append(particle)


    def run(self):
        objects_limit = self.__objects_limit
        objects = self.__objects
        width, height = self.width(), self.height()
        red_color = 0xff, 0, 0
        white_color = 0xff, 0xff, 0xff

        for obj in objects:
            obj.update(self)

            obj.allow_go_away(len(objects) > objects_limit)

            pos, vel, radius = obj.position(), obj.velocity(), obj.radius()
            if (pos.x <= -obj.trace_limit() and vel.x < 0) or (pos.x >= width + obj.trace_limit() and vel.x > 0):
                obj.remove_me(True)

            if (pos.y <= -obj.trace_limit() and vel.y < 0) or (pos.y >= height + obj.trace_limit() and vel.y > 0):
                obj.remove_me(True)

        self.__objects = objects = [obj for obj in objects if not obj.remove_me()]

        obj_len = len(objects)
        for i in range(obj_len - 1):
            obj1 = objects[i]
            j = i + 1
            while j < obj_len:
                obj2 = objects[j]
                if obj1.collide(obj2):
                    obj1.align(obj2, self)
                    obj1.bounce(obj2)
                j += 1

        for obj in objects:
            obj.draw(self)
