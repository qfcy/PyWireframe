*This is an extended version of package PyWireframe, aiming at using fewer code to render 3D scenes. Some bugs from the old version have been fixed.*

*Besides, we added some new features such as drawing polygon and FPS displaying.*

PyWireframe是一个使用Python turtle绘制3D图形的库, 使用简单的代码实现复杂的3D场景。

这是PyWireframe包的扩展版本。旧版本中的一些错误已经被修复。

此外，我们还添加了一些新功能，如绘制多边形和FPS显示等。

运行效果:

.. image:: https://img-blog.csdnimg.cn/6fe4d0db8676481ea0876e2414114ef7.gif
	:alt: Preview1

.. image:: https://img-blog.csdnimg.cn/928af47729d247bb8c63b4f637a33a5f.gif
	:alt: Preview2

以下为PyWireframe原版的部分英文说明: 

PyWireframe-extended V0.5
=========================

PyWireframe is a Python library for creating 3D wireframe graphics. 
It's highly inefficient (it uses turtle graphics) and doesn't support rotation.

Installation
------------

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install
PyWireframe.

# `pip install PyWireframe`

Usage
-----
PyWireframe has three different ways of rendering - [Objects](https://github.com/HyperHamster535/PyWireframe/wiki/Objects), [Shapes](https://pywireframe.readthedocs.io/en/latest/Usage/Objects.html), and [Dyanmic Objects](https://pywireframe.readthedocs.io/en/latest/Usage/Dynamic-Objects.html). For info on the syntax for using these, [see the doc](https://github.com/HyperHamster535/PyWireframe/wiki/).

To start PyWireframe, use `start()`.

To add objects use function `addObject`.

To render all existing objects, use `refresh()`.

To exit PyWireframe, use `exit()`.

You can also stop PyWireframe from printing to the console with `printMode(mode)`. More info can be found on the [readthedocs.io](https://pywireframe.readthedocs.io/en/latest/).

上传者 Uploader:

* 七分诚意 qq:3076711200 百度贴吧账号:qfcy\_ *

* CSDN主页: https://blog.csdn.net/qfcy\_ *