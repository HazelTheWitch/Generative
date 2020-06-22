from PIL import Image, ImageDraw
from hvector import Vector

import math
import random

class Line:
    def __init__(self, theta0, theta1, lines):
        self.startPoint = Line.thetaToPoint(theta0)
        self.endPoint = Line.thetaToPoint(theta1)

        for line in lines:
            self.updateEndPoint(line)
        
    def updateEndPoint(self, line):
        intersect = self.intersection(line)

        if intersect:
            self.endPoint = intersect

    def pointAt(self, t):
        return self.startPoint + (self.endPoint - self.startPoint) * t
    
    def intersection(self, other):
        x00, y00 = self.startPoint
        x01, y01 = self.endPoint
        x10, y10 = other.startPoint
        x11, y11 = other.endPoint
        
        A = y00-y10
        B = y01-y00
        C = y11-y10
        D = x00-x10
        E = x01-x00
        F = x11-x10

        T0 = -(F*A-D*C)/(F*B-E*C)

        T1 = (A + B*T0) / C

        if 0 <= T0 <= 1 and 0 <= T1 <= 1:
            return self.pointAt(T0)
        
        return None

    @staticmethod
    def thetaToPoint(theta):
        return Vector.fromNSpherical(1, theta)

    @classmethod
    def randomLine(cls, lines, deadzone=0):
        TWOPI = 2 * math.pi
        t0 = random.uniform(0, TWOPI)
        t1 = random.uniform(0, TWOPI)

        while Line.angleDifference(t0, t1) < deadzone:
            t1 = random.uniform(0, TWOPI)

        return cls(t0, t1, lines)

    @staticmethod
    def angleDifference(t0, t1):
        if t0 > t1:
            t0, t1 = t1, t0
        return min(t1 - t0, t0 + 2 * math.pi - t1)

    

def generate(fp, width, height, lineCount, background=(0, 0, 0, 0), lineColor=(255, 255, 255, 255), circleColor=None, circleFill=None, lineWidth=1):
    if not circleColor:
        circleColor = lineColor

    if not circleFill:
        circleFill = background

    def pti(p):
        half = Vector(width, height) / 2
        return tuple(half + half.componentMul(p))

    image = Image.new('RGBA', (width, height))

    draw = ImageDraw.Draw(image)

    draw.ellipse(
        (pti(Vector(-1, -1)), pti(Vector(1, 1))),
        outline=circleColor,
        fill=circleFill,
        width=lineWidth
    )

    lines = []

    for i in range(lineCount):
        line = Line.randomLine(lines, math.pi / 3)
        lines.append(line)

        draw.line(
            (pti(line.startPoint), pti(line.endPoint)),
            fill=lineColor,
            width=lineWidth
        )

    image.save(fp)

for i in range(5):
    generate(f'test{i}.png', 400, 400, 5, lineWidth=4)
