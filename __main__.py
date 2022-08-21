from turtle import Turtle,Terminator
try:
    import PyWireframe.engine as engine
except ImportError:
    import engine
try:
    import PyWireframe.render as render
except ImportError:
    import render

render.test1()
try:Turtle().hideturtle()
except Terminator:pass # 避免关闭窗口后调用test2引发Terminator异常
engine.clearObjects()
print("Running test 2")
render.test2()