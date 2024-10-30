import turtle
import random
import time

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Bouncing Ball Simulator")
wn.tracer(0)

balls = []

for _ in range(25):
    balls.append(turtle.Turtle())

colors = ["red", "orange", "yellow", "green", "blue", "violet"]
shapes = ["circle", "square", "triangle"]

for ball in balls:
    ball.shape(random.choice(shapes))
    ball.color(random.choice(colors))
    ball.penup()
    ball.speed(0)
    x = random.randint(-290, 290)
    y = random.randint(200, 400)
    ball.goto(x, y)
    ball.dy = 0
    ball.dx = random.randint(-1, 1)
    ball.da = random.randint(-1, 1)

gravity = 0.01

while True:
    wn.update()

    for ball in balls:
        ball.rt(ball.da)
        ball.dy -= gravity
        ball.sety(ball.ycor() + ball.dy)

        ball.setx(ball.xcor() + ball.dx)

        #Check for a wall collision
        if ball.xcor() > 300:
            ball.dx *= -1
            ball.da *= -1

        if ball.xcor() < -300:
            ball.dx *= -1
            ball.da *= -1

        #Check for a bounce
        if ball.ycor() < -300:
            ball.sety(-300)
            ball.dy *= -1
            ball.da *= -1

    #Check for collisions between balls
    for i in range(0, len(balls)):
        for j in range(i+1, len(balls)):
            #Check for a collision
            if balls[i].distance(balls[j]) < 20:
                balls[i].dx, balls[j].dx = balls[j].dx, balls[i].dx
                balls[i].dy, balls[j].dy = balls[j].dy, balls[i].dy

        # # Add a small delay to slow down the entire simulation
        # time.sleep(0.000001)