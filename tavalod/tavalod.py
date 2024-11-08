import turtle
import random
import time
import math

firework_turtles = [turtle.Turtle() for _ in range(15)]  






for t in firework_turtles:
    t.speed(0)
    t.hideturtle()


turtle.tracer(0, 0)  

# gayide shodim kiram to python.
def draw_firework(t, x, y):
    colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'white']
    t.penup()
    t.goto(x, y)
    t.pendown()

  
    for explosion_size in range(2, 21, 2):
        t.color(random.choice(colors))
        for i in range(36):  
            t.forward(explosion_size * 5)
            t.backward(explosion_size * 5)
            t.right(10)
        t.penup()  
        t.goto(x, y)
        t.pendown()

# would you please fukcing run???
def simultaneous_fireworks():
    for t in firework_turtles:
        x = random.randint(-300, 300)
        y = random.randint(-200, 200)
        t.hideturtle()
        t.clear()
        t.showturtle()
        draw_firework(t, x, y)
        turtle.update()  
        time.sleep(0.5)  

# ameye man ghazie ameye to razie ya baraks bood? yadam nemiad
def clear_fireworks():
    for t in firework_turtles:
        t.clear()


def draw_flower(t, x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(random.choice(['red', 'pink', 'yellow', 'blue', 'purple']))
    
    
    for _ in range(36):  
        t.circle(50)
        t.left(10)


def flower_show():
    num_sides = 8 
    radius = 200 













#be ghole asatid yadetoon nare test benevisid.
    angle = 360 / num_sides
    for i in range(num_sides):
        x = radius * math.cos(math.radians(i * angle))
        y = radius * math.sin(math.radians(i * angle))
        t = firework_turtles[i % len(firework_turtles)] 
        t.clear()
        t.speed(3) 
        t.hideturtle()
        draw_flower(t, x, y)
        t.hideturtle()
    turtle.update() 

#
def show_tavalod_m():
    turtle.penup()
    turtle.goto(0, 0)
    turtle.color('white')
    turtle.write("Happy Birthday, Asal!", align="center", font=("Arial", 40, "bold"))
    turtle.hideturtle()
    time.sleep(3)


def main():
    turtle.bgcolor('black')
    simultaneous_fireworks()
    time.sleep(1)  

    
    clear_fireworks() 
    
    flower_show()
    time.sleep(2)  
    show_tavalod_m()
    turtle.done()

if __name__ == "__main__":
    main()
