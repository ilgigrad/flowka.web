from django.template import Library
from core.utils import toInt, hex_to_rgb,rgb_to_hex
register = Library()

@register.filter(name='mkrange')
def mkrange(args):
    min=toInt(args.get('min',0))
    max=toInt(args.get('max',min))
    step=toInt(args.get('step',1))
    return range(min, max+step, step)

@register.filter(name='mksize')
def mksize(args,area):
    min=toInt(args.get('min',0))
    max=toInt(args.get('max',min))
    step=toInt(args.get('step',1))
    area=toInt(area)-3000
    nb=area/toInt((max-min)/step)
    from math import sqrt
    return int(10 * round(float(sqrt(nb))/10))


@register.filter(name='mkcolorrange')
def mkcolorrange(args,colors):
    x=0
    colorList=[]
    while True:
        if x>=len(colors):
            break
        colorList.append(colors[x:x+7])
        x+=7
    import random
    color0=colorList.pop(int(random.random()*len(colorList)))
    color1=colorList.pop(int(random.random()*len(colorList)))
    if isinstance(args,str):
        args=args.split(',')
        min=toInt(args[0])
        max=toInt(args[1])
        step=toInt(args[2])
    else:
        min=toInt(args.get('min',0))
        max=toInt(args.get('max',min))
        step=toInt(args.get('step',1))
    nb=toInt((max-min)/step)+1
    rgb0=hex_to_rgb(color0)
    rgb1=hex_to_rgb(color1)
    ri=(rgb1[0]-rgb0[0])/nb
    gi=(rgb1[1]-rgb0[1])/nb
    bi=(rgb1[2]-rgb0[2])/nb
    colorrange=[]
    for i in range(nb+1):
        colorrange.append(rgb_to_hex((int(rgb0[0]+(i*ri)),int(rgb0[1]+(i*gi)),int(rgb0[2]+(i*bi)))))
    return colorrange
