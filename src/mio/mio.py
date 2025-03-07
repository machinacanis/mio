from io import BytesIO
from os import PathLike
from pathlib import Path
from typing import Any

import numpy as np
from numpy import ndarray, dtype
import cv2 as cv

from .image import MioImage


class Mio(MioImage):
    """
    基于 opencv-python 的图像绘制工具
    """
    def __init__(self):
        super().__init__()  # 调用父类的初始化方法
