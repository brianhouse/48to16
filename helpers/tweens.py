def linear(pos):
    return pos

def ease_in(pos):
    return pos**3
    
def ease_out(pos):
    return (pos - 1)**3 + 1

def ease_in_out(pos):
    pos *= 2
    if pos < 1:
         return 0.5 * pos**3
    pos -= 2
    return 0.5 * (pos**3 + 2)

def ease_out_in(pos):
    pos *= 2    
    pos = pos - 1    
    if pos < 2:
        return 0.5 * pos**3 + 0.5
    else:
        return 1.0 - (0.5 * pos**3 + 0.5)
        


if __name__ == "__main__":
    from housepy import drawing
    ctx = drawing.Context(400, 400, relative=True, flip=True)
    for n in range(1000):
        x = float(n) / 1000.0
        y = ease_in_out(x)
        ctx.arc(x, y, 1.0/ctx.width, 1.0/ctx.height, thickness=0, fill=(0., 0., 0.))
    ctx.show()
    exit()
