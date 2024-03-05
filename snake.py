import minescript
import keyboard
import sys
from math import *
import time
from random import randint

def direction(yaw,pitch):
    yaw = radians(yaw)
    pitch = radians(pitch)
    return [-cos(pitch) * sin(yaw),-sin(pitch), cos(pitch) * cos(yaw)]

def rcolor():
    return []

def particle(pos,color):
    x,y,z = pos
    r,g,b = [i/255 for i in color]
    minescript.execute(f"/particle minecraft:dust {r} {g} {b} 1 {x} {y} {z}")

def cross_product(u, v):
    return [ u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]

class Player:
    def __init__(self):
        self.pos = [0,0,0]
        self.direction = [0,0,0]
        self.h = 1.5
        self.r = 8
    def update(self):
        self.pos = minescript.player_position()
        self.pos[1] += self.h
        self.direction = direction(*minescript.player_orientation())
    def get_gridpos(self):
        return [self.pos[i] + self.r*self.direction[i] for i in range(3)]
    
def add(a,b,p=True):
    return [a[i] + b[i] for i in range(3)] if p else [a[i] - b[i] for i in range(3)]

def scale(a,n):
    return [n*i for i in a]
    
class Game:
    def __init__(self):
        self.fail = [
            [0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0],
            [0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0],
            [0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0]
        ]
        self.array = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        self.ydim = len(self.array)
        self.xdim = len(self.array[0])
        self.x_offset = self.xdim // 2
        self.y_offset = self.ydim // 2
        self.snake = [[self.y_offset,self.x_offset]]
        self.heading = "down"
        self.running = True
        self.colors= {
            1:[255,255,255],
            2:[0,255,0],
            3:[255,0,0]
        }
        self.apples = 0
        self.spawn_apple()
    def insert_head(self,n=1):
        if self.heading == "right":
            self.snake.insert(0,[self.snake[0][0],self.snake[0][1]+n])
        elif self.heading == "left":
            self.snake.insert(0,[self.snake[0][0],self.snake[0][1]-n])
        elif self.heading == "up":
            self.snake.insert(0,[self.snake[0][0]+n,self.snake[0][1]])
        elif self.heading == "down":
            self.snake.insert(0,[self.snake[0][0]-n,self.snake[0][1]])    

    def spawn_apple(self):
        empty = False
        while not empty:
            y, x = randint(2, self.ydim-3), randint(2, self.xdim-3)
            if self.array[y][x] == 0:  
                self.array[y][x] = 3
                empty = True

    def update(self):
        self.insert_head()
        if self.array[self.snake[0][0]][self.snake[0][1]] == 3:
            self.apples += 1
            self.spawn_apple()
        else:
            ey, ex = self.snake.pop()
            self.array[ey][ex] = 0
        head_y, head_x = self.snake[0]
        if self.array[head_y][head_x] in [1, 2]:
            self.array = self.fail
            self.running = False
        else:
            self.array[head_y][head_x] = 2  

def norm(v):
    return sqrt(sum([i**2 for i in v]))

def draw(ply,G):
    gridpos = ply.get_gridpos()
    right = cross_product(ply.direction,[0,1,0])
    for y in range(G.ydim):
        for x in range(G.xdim):
            index = G.array[y][x]
            if index != 0:
                particle_pos = add(gridpos, add(scale(right, x - G.x_offset), [0, y - G.y_offset, 0]))
                particle(particle_pos,G.colors[index]) 
            

def on_key_press(event):
    key = event.name
    if key == "flecha arriba":
        game.heading = "up"
    elif key == "flecha abajo":
        game.heading = "down"
    elif key == "flecha izquierda":
        game.heading = "left"
    elif key == "flecha derecha":
        game.heading = "right"
    elif key == "k":
        sys.exit()

def main():
    global game  
    ply = Player()
    game = Game()
    keyboard.on_press(on_key_press)
    
    try:
        while game.running:
            time.sleep(0.2)  
            ply.update()
            game.update()
            draw(ply, game)
    finally:
        keyboard.unhook_all()

if __name__ == "__main__":
    main()

