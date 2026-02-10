import turtle; 

# t.speed(0)

# size = 100

def draw_square(t, size = 100):
    #Draw a square with the given size.
    for _ in range(4):
        t.forward(size); t.left(90)

#for i in range(100):
#    t.forward(100);t.left(89)

def main():
    t = turtle.Turtle()
    t.speed(0)
    draw_spiral(t)
    t.mainloop()

def draw_spiral(t):
    for i in range(36):
        draw_square(t, 50)
        t.left(10)