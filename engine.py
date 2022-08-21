import sys
import math
import turtle

FocalLength = 100
CameraX = 0
CameraY = 0
CameraZ = 0
Objects = []
_Dict={}
cfg = {"doPrint":True,"fast":True,"autoPrintPos":False}
drawing=False
_curPos=(0,0,0)
_points=set()

def start():
    if cfg["doPrint"]:
        print("Starting PyWireframe")

    if cfg["doPrint"]:
        print("Defining render")

    #Define render
    global render

    render=turtle.Turtle()
    render.speed(0)
    render.hideturtle()
    render.penup()
    render.screen.title("PyWireframe")
    if cfg["doPrint"]:
        print("PyWireframe has started succesfully!")

#Redraw all predefined objects
def refresh():
    render.clear()

    for a in Objects:
        try:
            render.pencolor(a[1])
            exec(a[0],_Dict)
        except TypeError: # a is a dynamic object (function)
            a()
    _points.clear()
    render.pencolor('black')

def exit():
    render.bye()

def __formatkw(kw):
    return ''.join("{}={},".format(key,repr(kw[key])) for key in kw.keys())
def addObject(shape, *args, color='black', **kw):
    # 为所有物体设置统一的color参数
    Objects.append(["{}({}{})".format(shape.__name__,
                                       ','.join(repr(a) for a in args),
                                       ','+__formatkw(kw) if kw else ''),
                    color])
    if cfg["doPrint"]:
        print("Added object {} as object # {} color: {}" \
              .format(Objects[-1][0], str(len(Objects)),color))
    _Dict[shape.__name__]=shape

def addDynamicObject(function):
    if cfg["doPrint"]:
        print("Added '" + function + "' object as object #" + str(len(Objects)))
    Objects.append(function)

def deleteObject(value):
    Objects.pop(value)
    if cfg["doPrint"]:
        print("Deleted object #" + value)

def printObject(value):
    if cfg["doPrint"]:
        print(str(value) + ": " + str(Objects[value]))
    else:
        raise Exception("Cannot print object as printing is disabled.")
def printObjects():
    for i in range(len(Objects)):printObject(i)
def clearObjects():
    Objects.clear()

# 最关键的函数, 相对相机的三维坐标转二维坐标
# x,y,z: 点与相机的x,y,z坐标差
def convert_3d_to_2d(x,y,z):
    # focallength: 缩放比为1时, 点与相机的Z距离
    try:
        ScaleFactor = FocalLength/(z + FocalLength) # FocalLength/z
    except ZeroDivisionError:
        ScaleFactor = -1

    if ScaleFactor < 0:
        max_scr = 1e4 # 最大边界
        try:x_ = abs(max_scr / x)
        except ZeroDivisionError:x_ = math.inf
        try:y_ = abs(max_scr / y)
        except ZeroDivisionError:y_ = math.inf
        ScaleFactor = min(x_, y_)
        if ScaleFactor == math.inf:ScaleFactor = 0

    X = x * ScaleFactor
    Y = y * ScaleFactor
    return X, Y

#Renders a line in 3d space
def line(x1, y1, z1, x2, y2, z2, pos=False):
    global drawing, _curPos
    if z1 <= CameraZ - FocalLength and z2 <= CameraZ - FocalLength: return  # 不绘制镜头后的线
    if drawing:return
    drawing=True  # 避免多个同时进行的画图冲突 (可用线程锁替代)

    X, Y = convert_3d_to_2d(
        x1 - CameraX, y1 - CameraY, z1 - CameraZ)
    render.goto(X, Y)
    render.pendown()
    _curPos = (x1, y1, z1)
    if pos or cfg["autoPrintPos"]: printPos()

    X, Y = convert_3d_to_2d(
        x2 - CameraX, y2 - CameraY, z2 - CameraZ)
    render.goto(X, Y)
    _curPos = (x2, y2, z2)
    if pos or cfg["autoPrintPos"]: printPos()

    render.penup()

    drawing=False

def ball(x,y,z,size,pos=False):
    # size: radius of the ball
    global _curPos,drawing
    _curPos = (x, y, z)
    if z <= CameraZ - FocalLength: return  # 不绘制镜头后的物体
    if drawing:return
    drawing=True

    try:
        ScaleFactor = FocalLength / (z - CameraZ + FocalLength)
    except ZeroDivisionError:
        ScaleFactor = 1e4
    if ScaleFactor < 0:
        ScaleFactor = 1e4

    X = (x-CameraX) * ScaleFactor
    Y = (y-CameraY) * ScaleFactor
    size *= ScaleFactor

    #render.penup()
    render.setheading(0)
    render.goto(X, Y - size)
    render.pendown()
    render.circle(size)
    render.penup()
    if pos or cfg["autoPrintPos"]:
        render.goto(X, Y)
        # center
        render.dot(3)
        printPos()
    drawing = False

def polygon(points,fillcolor=None,draw_edge=True,pos=False):
    # pencolor已包含在color参数中
    global _curPos, drawing
    # 不绘制镜头后的物体
    flag=False
    for point in points:
        if point[2] > CameraZ - FocalLength: flag=True
    if not flag:return # 所有点都在镜头的后面
    if drawing:return
    drawing=True

    if draw_edge:render.pendown()
    if fillcolor:
        render.fillcolor(fillcolor)
        render.begin_fill()
    for point in points + [points[0]]:# 形成闭环
        _curPos = point
        if pos or cfg["autoPrintPos"]: printPos()
        x,y,z = point
        X, Y = convert_3d_to_2d(
            x - CameraX, y - CameraY, z - CameraZ)
        render.goto(X, Y)

    render.penup()
    if fillcolor:
        render.end_fill()
    drawing = False

def text(arg,align='left',font=('Arial', 8, 'normal')):
    render.write(str(arg),align=align,font=font)

def printPos():
    # don't write down position repeatly
    if _curPos not in _points:
        text(_curPos)
        _points.add(_curPos)

def getPos():
    return _curPos

def moveCamera(axis, amount, _refresh=False):
    global CameraX
    global CameraY
    global CameraZ

    if axis == "X":
        CameraX += amount
    elif axis == "Y":
        CameraY += amount
    elif axis == "Z":
        CameraZ += amount
    else:
        raise Exception(axis +" is not a valid axis")

    if _refresh:refresh()

def setCameraPos(x=None,y=None,z=None, _refresh=False):
    global CameraX,CameraY,CameraZ
    if x:CameraX=x
    if y:CameraY=y
    if z:CameraZ=z
    if _refresh:refresh()

def setFocalLen(newFocalLen=None,amount=None,_refresh=False):
    global FocalLength
    if newFocalLen:FocalLength=newFocalLen
    elif amount:FocalLength+=amount
    if _refresh:refresh()

def reset():
    global CameraX, CameraY, CameraZ, FocalLength
    CameraX=CameraY=CameraZ=0
    FocalLength=0

def debug():
    print("CameraX = " + str(CameraX))
    print("CameraY = " + str(CameraY))
    print("CameraZ = " + str(CameraZ))
    print("FocalLength = " + str(FocalLength))
    print("objects: ")
    print(Objects)

def mode(*posarg, doPrint = None, fast=None,
         autoPrintPos=None):
    if posarg:raise TypeError("Keyword arguments only")
    if doPrint is not None:cfg["doPrint"]=doPrint
    if fast is not None:cfg["fast"]=fast
    if autoPrintPos is not None:cfg["autoPrintPos"]=autoPrintPos
def printMode(mode): # Only for compatibility
    if mode == "on":
        cfg["doPrint"] = True
    elif mode == "off":
        cfg["doPrint"] = False
    else:
        print("'" + mode + "' is not a valid printMode value.")

def getCanvas():
    return render.screen.getcanvas()
def getRender():
    return render