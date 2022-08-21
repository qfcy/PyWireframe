import sys,turtle
from PyWireframe.engine import *
from time import perf_counter
from tkinter import TclError

#Define some shapes
def cube(x, y, z, size):
    line(x, y, z, size, y, z)
    line(size, y, z, size, size, z)
    line(size, size, z, y, size, z)
    line(x, size, z, x, y, z)

    line(x, y, size, size, y, size)
    line(size, y, size, size, size, size)
    line(size, size, size, x, size, size)
    line(x, size, size, x, y, size)

    line(x, y, z, x, y, size)
    line(size, y, z, size, y, size)
    line(size, size, z, size, size, size)
    line(x, size, z, x, size, size)

def pyramid3 (x, y, z, size):
    line(x, y, z, size, y, z)
    line(x, y, z, size / 2, size, z)
    line(x, y, z, size / 2, y, size)

    line(size, y, z, size / 2, size, z)
    line(size, y, z, size / 2, y, size)

    line(size / 2, y, size, size / 2, size, z)

def pyramid4 (x, y, z, size):
    line(x, y, z, size, y, z)
    line(x, y, z, x, y, size)

    line(size, y, size, size, y, z)
    line(size, y, size, x, y, size)

    line(x, y, z, size / 2, size, size / 2)
    line(size, y, z, size / 2, size, size / 2)
    line(x, y, size, size / 2, size, size / 2)
    line(size, y, size, size / 2, size, size / 2)

def horizon(distance=3000,length=80000):
    line(-length/2,0,distance,length/2,0,distance)

def __move(event,axis,amount):
    __unbind()
    name="<Key-%s>"%event.keysym
    #print(name,event)
    #cv.unbind_all(name)
    moveCamera(axis,amount)
    #refresh()
    #debug()
    __bind()

_delta = 5
def __bind():
    cv=getCanvas()
    cv.bind_all("<Key-Up>",lambda event:__move(event,'Z',_delta))
    cv.bind_all("<Key-Down>",lambda event:__move(event,'Z',-_delta))
    cv.bind_all("<Control-Key-Down>",lambda event:__move(event,'Y',-_delta))
    cv.bind_all("<Control-Key-Up>",lambda event:__move(event,'Y',_delta))
    cv.bind_all("<Key-Left>",lambda event:__move(event,'X',-_delta))
    cv.bind_all("<Key-Right>",lambda event:__move(event,'X',_delta))
    cv.bind_all("<Key-equal>",lambda event:setFocalLen(amount=5))
    cv.bind_all("<Key-minus>",lambda event:setFocalLen(amount=-5))
def __unbind(): # 用于渲染时暂时不接受新的键盘事件
    cv=getCanvas()
    cv.unbind_all("<Key-Up>") # unbind_all与bind_all对应, unbind也与bind对应
    cv.unbind_all("<Key-Down>")
    cv.unbind_all("<Control-Key-Down>")
    cv.unbind_all("<Control-Key-Up>")
    cv.unbind_all("<Key-Left>")
    cv.unbind_all("<Key-Right>")
    cv.unbind_all("<Key-equal>")
    cv.unbind_all("<Key-minus>")

def mainloop():
    show_fps = True
    last_time = perf_counter()
    writer = turtle.Turtle()
    writer.hideturtle();
    writer.penup()
    writer.screen.tracer(False)
    # Python turtle的bug: 调用write()方法后画布会自动刷新, 与tracer(False)无关
    update = writer.screen.cv.update
    writer.screen.cv.update=lambda:None
    try:
        while True:
            refresh()
            update()
            fps = 1 / (perf_counter() - last_time)
            last_time = perf_counter()
            if show_fps:
                writer.clear()
                writer.goto(
                    writer.screen.window_width() // 2 - 80,
                    writer.screen.window_height() // 2 - 25
                )
                writer.write(
                    "fps: %d" % fps,
                    font=(None, 12)
                )
    except (turtle.Terminator, TclError):
        pass

# 相机初始位置为0,0,0
def test1():
    mode(autoPrintPos=True)
    start()
    __bind()
    addObject(horizon,color='#bbbbbb')
    addObject(cube,0,0,0,100)
    addObject(pyramid4,100,100,100,160,color='green')
    addObject(ball,50,50,0,50,color='purple')

    mainloop()

def test2():
    mode(autoPrintPos=False)
    mode(doPrint=False)
    mode(fast=True)
    start()
    turtle.colormode(255)
    __bind()

    length = 2000
    step = 40
    addObject(polygon, [(80, -80, 0), (80, -80, length - step),
                        (-80, -80, length - step), (-80, -80, 0)],
              fillcolor="#d0d0d0", draw_edge=False) # 地面
    addObject(line,-80,80,0,-80,80,length-step)
    addObject(line,-80,-80,0,-80,-80,length-step)
    for z in range(0,length,step):
        r,g,b = int(z * 0.1), int(z * 0.1), int(z * 0.1) # 淡出效果
        addObject(line,-80,80,z,-80,-80,z, color=(r,g,b))

    addObject(line,80,-80,0,80,-80,length-step)
    addObject(line,80,80,0,80,80,length-step)
    for z in range(0,length,step):
        r,g,b = int(z * 0.1), int(z * 0.1), int(z * 0.1)
        addObject(line,80,80,z,80,-80,z, color=(r,g,b))

    mainloop()

if __name__=="__main__":test1()