<p align="center">
    <img src="mio.png" alt="mio" width="200" height="200">
</p>
<div align="center">

#  Mio

_😎 基于 [opencv-python](https://github.com/opencv/opencv-python) 封装的文本图像绘制/排版工具，让编写自动化图片生成的过程更不那么折磨一些（大概）_

</div>

## 安装

> 暂时还没上传到pypi，可以直接下载源码打包使用
>
> 好吧其实没法用，因为才写了一点

```shell
pip install pymio
```

# 简单使用

```python

from mio import MioImage

img1 = MioImage("image1.png")
img2 = MioImage("image2.png").resize(300, 500)

result = img1 + img2
result.write("result.png")

```