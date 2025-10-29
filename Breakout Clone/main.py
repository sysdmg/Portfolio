import turtle
import time
import random

# Create custom Ball class
class Ball(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.speed(0)
        self.shape("circle")
        self.color("white")
        self.penup()
        self.goto(0, 0)
        self.dx = 1.4
        self.dy = 1.4

# Set up the screen
screen = turtle.Screen()
screen.title("Breakout")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)

# Create the paddle
paddle = turtle.Turtle()
paddle.speed(0)
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=1, stretch_len=5)
paddle.penup()
paddle.goto(0, -250)

# Create the ball
ball = Ball()

# Create score display
score = 0
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))

# Create bricks
bricks = []
colors = ["red", "orange", "yellow", "green", "blue"]
for i in range(5):  # 5 rows
    for j in range(8):  # 8 bricks per row
        brick = turtle.Turtle()
        brick.speed(0)
        brick.shape("square")
        brick.color(colors[i])
        brick.shapesize(stretch_wid=1, stretch_len=3)
        brick.penup()
        brick.goto(-350 + j * 100, 200 - i * 30)
        bricks.append(brick)

# Paddle movement functions
def paddle_right():
    x = paddle.xcor()
    if x < 350:
        paddle.setx(x + 20)

def paddle_left():
    x = paddle.xcor()
    if x > -350:
        paddle.setx(x - 20)

# Keyboard bindings
screen.listen()
screen.onkeypress(paddle_right, "Right")
screen.onkeypress(paddle_left, "Left")

# Main game loop
game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(0.01)  # Add a small delay to control game speed
    
    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)
    
    # Ball collision with walls
    if ball.xcor() > 390 or ball.xcor() < -390:
        ball.dx *= -1
    
    if ball.ycor() > 290:
        ball.dy *= -1
    
    # Ball collision with paddle
    if (ball.ycor() < -240 and ball.ycor() > -250) and \
       (ball.xcor() < paddle.xcor() + 50 and ball.xcor() > paddle.xcor() - 50):
        ball.dy *= -1
    
    # Ball collision with bricks
    for brick in bricks[:]:
        if (brick.ycor() - 20 < ball.ycor() < brick.ycor() + 20) and \
           (brick.xcor() - 30 < ball.xcor() < brick.xcor() + 30):
            brick.hideturtle()
            bricks.remove(brick)
            ball.dy *= -1
            score += 10
            score_display.clear()
            score_display.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))
    
    # Check for game over
    if ball.ycor() < -290:  # Ball goes below paddle
        game_is_on = False
        score_display.goto(0, 0)
        score_display.write("GAME OVER", align="center", font=("Courier", 36, "normal"))
    
    # Check for win
    if len(bricks) == 0:
        game_is_on = False
        score_display.goto(0, 0)
        score_display.write("YOU WIN!", align="center", font=("Courier", 36, "normal"))

screen.mainloop()