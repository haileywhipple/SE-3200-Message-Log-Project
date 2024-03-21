from random import shuffle, randrange

def make_maze(w, h):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["█ "] * w + ['█'] for _ in range(h)] + [[]]
    hor = [["██"] * w + ['█'] for _ in range(h + 1)]

    def walk(x, y):
        vis[y][x] = 1
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "█ "
            if yy == y: ver[y][max(x, xx)] = "  "
            walk(xx, yy)

    walk(randrange(w), randrange(h))
    s_row = randrange(1, h-2)
    e_row = randrange(1, h-2)
    
    while "█" in hor[s_row][1][1]:
        if s_row > 0:
            s_row -= 1
        elif s_row < h:
            s_row += 1
        
    hor[s_row][0] = "  "

    while "█" in hor[e_row][w-1][1]:
        if e_row > 0:
            e_row -= 1
        elif e_row < h:
            e_row += 1
    
    hor[e_row][w] = " "
        

    s = ""

    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])

    return s