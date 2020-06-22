from PIL import Image, ImageDraw, ImageFont

import random
import math

def thetaToXY(theta, d):
    return d * math.cos(theta % (2 * math.pi)), d * math.sin(theta % (2 * math.pi))

def trace(x0, y0, theta, dtheta, ddtheta, length, stepSize, splitPerUnit, splitsPossible, maxDtheta):
    distance = 0

    while distance < length:
        yield x0, y0
        theta += dtheta
        dx, dy = thetaToXY(theta, stepSize)
        distance += stepSize
        x0 += dx
        y0 += dy

        dtheta *= ddtheta

        if abs(dtheta) > maxDtheta:
            yield None\

        if random.random() < splitPerUnit * stepSize and splitsPossible > 0:
            yield from trace(x0, y0, theta, dtheta, ddtheta + random.uniform(-0.001, 0.001), length - distance, stepSize, splitPerUnit, splitsPossible - 1, maxDtheta)
            yield from trace(x0, y0, theta, -dtheta, ddtheta + random.uniform(-0.001, 0.001), length - distance, stepSize, splitPerUnit, splitsPossible - 1, maxDtheta)
            break
    
    yield None


def generate(size, background, traceColor, traces, length, width, scale=1, seed=None, text=None, doText=True, textLocation=(0.5, 0.8), textSize=36, font='FiraCode-Regular.ttf', traceOrigin=(0.5, 0.5), variation=None, textVariation=None, drawChance=0.8):
    img = Image.new('RGBA', (size[0] * scale, size[1] * scale), color=background)

    draw = ImageDraw.Draw(img)

    if seed is not None:
        if variation:
            random.seed(f'{seed}{variation}')
        else:
            random.seed(seed)

        if text is None:
            text = str(seed)

    if doText and text is not None:
        font = ImageFont.truetype(font=font, size=textSize)
        if textVariation:
            font.set_variation_by_name(textVariation)
        w, h = draw.textsize(seed, font=font)
        x = int(size[0] * scale * textLocation[0] - w / 2)
        y = int(size[1] * scale * textLocation[1] - h / 2)

        draw.text((x, y), text, fill=traceColor, font=font)

    for t in range(traces // 2):
        x, y = None, None

        theta = math.pi / 4 + random.uniform(-math.pi / 8, math.pi / 8)

        for XY in trace(size[0] * traceOrigin[0], size[1] * traceOrigin[1], theta, random.uniform(-0.01, 0.01), random.uniform(1.0001,
                                                                                                     1.005), length, 1, 1 / 500, 4, math.pi / 20):
            if XY is None:
                x, y = None, None
            else:
                X, Y = XY

                if x is not None and y is not None and random.random() < drawChance:
                    draw.line([x * scale, y * scale, X * scale, Y * scale],
                              fill=traceColor, width=width)

                x = X
                y = Y

        
        for XY in trace(size[0] * traceOrigin[0], size[1] * traceOrigin[1], (theta + math.pi) % (2 * math.pi), random.uniform(-0.01, 0.01), random.uniform(1.0001,
                                                                                                                                 1.005), length, 1, 1 / 500, 4, math.pi / 20):
            if XY is None:
                x, y = None, None
            else:
                X, Y = XY

                if x is not None and y is not None and random.random() < drawChance:
                    draw.line([x * scale, y * scale, X * scale, Y * scale],
                              fill=traceColor, width=width)

                x = X
                y = Y
    
    return img


# generate((1024, 1024), (0, 0, 0, 255), (241, 167, 190, 255), 10, 1000, 1).save('displate0.png')
seed = 'love'

var = 0
while True:
    generate((4060 // 4, 2900 // 4), (0, 0, 0, 255), (255, 255, 255, 255),
             10, 3000, 1, scale=4, traceOrigin=(0.5, 0.5), seed=seed, doText=True, textSize=160, font='Raleway-VariableFont_wght.ttf', textLocation=(0.5, 0.9), textVariation='Regular', variation=var).convert('RGB').save(f'displate{seed}.jpg', quality=95)
        
    if input():
        break
    
    var += 1

# Image.open('displate1.png').convert('RGB').save('displate1.jpg')
