import coordinates
from belt import Belt
from pen import Pen

import concurrent.futures

class Board:
    def __init__(self):
        self.w = 400 # mm
        self.h = 300 # mm
        self.belt0 = Belt(step=14, dir=15)
        self.belt1 = Belt(step=18, dir=23)

        self.pen = Pen(pin=24, lifted=0, pressed=0);

        self.belt0.pos, self.belt1.pos = coordinates.cartesian_to_polar(self.w/2, self.h/2, self.w, self.h)

    def lift_pen(self):
        self.pen.lift()

    def press_pen(self):
        self.pen.press()

    def go_to(self, x, y):
        x0, y0 = coordinates.polar_to_cartesian(self.belt0.pos, self.belt1.pos, self.w, self.h)
        N = 100
        dx = (x-x0) / N
        dy = (y-y0) / N

        for i in range(N):
            xi = x0 + (i+1)*dx
            yi = y0 + (i+1)*dy
            r0, r1 = coordinates.cartesian_to_polar(xi, yi, self.w, self.h)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                f1 = executor.submit(self.belt0.go_to, r0)
                f2 = executor.submit(self.belt1.go_to, r1)
