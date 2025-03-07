from typing import Any

import numpy as np

from mio.color import MioColor
from mio.exceptions import ImageSizeNotMatchError
from numpy import ndarray, dtype
import cv2 as cv


def alpha_mix(pic1: ndarray[Any, dtype], pic2: ndarray[Any, dtype]) -> ndarray[Any, dtype]:
    """
    直接叠加两个图像（包含alpha通道），返回一个新的ndarray对象

    叠加的两个图像必须大小一样，且都是BGRA格式（四通道）
    :param pic1:
    :param pic2:
    :return: 新的图像对象
    """
    # 以防万一，强制转换BGR为BGRA格式
    if len(pic1.shape) == 3 and pic1.shape[2] == 3:
        pic1 = cv.cvtColor(pic1, cv.COLOR_BGR2BGRA)
    if len(pic2.shape) == 3 and pic2.shape[2] == 3:
        pic2 = cv.cvtColor(pic2, cv.COLOR_BGR2BGRA)

    print(pic1.shape)
    print(pic2.shape)

    # 比较图像形状
    if pic1.shape[:2] != pic2.shape[:2]:
        raise ImageSizeNotMatchError("Size of two images are not match.")

    # 提取各通道
    b1, g1, r1, a1 = cv.split(pic1)
    b2, g2, r2, a2 = cv.split(pic2)

    # 归一化alpha通道
    alpha1 = a1 / 255.0
    alpha2 = a2 / 255.0

    # 计算混合后的alpha
    alpha_out = alpha2 + alpha1 * (1.0 - alpha2)
    alpha_out_normalized = alpha_out * 255.0

    # 计算颜色通道，考虑各自的透明度
    b_out = (b2 * alpha2 + b1 * alpha1 * (1.0 - alpha2)) / alpha_out
    g_out = (g2 * alpha2 + g1 * alpha1 * (1.0 - alpha2)) / alpha_out
    r_out = (r2 * alpha2 + r1 * alpha1 * (1.0 - alpha2)) / alpha_out

    # 合并通道
    pic = cv.merge([b_out.astype(np.uint8),
                    g_out.astype(np.uint8),
                    r_out.astype(np.uint8),
                    alpha_out_normalized.astype(np.uint8)])
    return pic

def alpha_mix_np(pic1: ndarray[Any, dtype], pic2: ndarray[Any, dtype]) -> ndarray[Any, dtype]:
    """
    直接叠加两个图像（包含alpha通道），返回一个新的ndarray对象，使用numpy实现的版本，暂时不用，似乎慢一倍

    叠加的两个图像必须大小一样，且都是BGRA格式（四通道）
    :param pic1:
    :param pic2:
    :return: 新的图像对象
    """
    # 以防万一，强制转换BGR为BGRA格式
    if len(pic1.shape) == 3 and pic1.shape[2] == 3:
        pic1 = cv.cvtColor(pic1, cv.COLOR_BGR2BGRA)
    if len(pic2.shape) == 3 and pic2.shape[2] == 3:
        pic2 = cv.cvtColor(pic2, cv.COLOR_BGR2BGRA)

    # 将图像转换为浮点数以提高精度
    pic1 = pic1.astype(np.float32) / 255.0
    pic2 = pic2.astype(np.float32) / 255.0

    # 提取alpha通道
    a1 = pic1[..., 3:4]  # 保持维度
    a2 = pic2[..., 3:4]  # 保持维度

    # 计算混合后的alpha
    alpha_out = a2 + a1 * (1.0 - a2)

    # 避免除以零
    mask = alpha_out > 0.001
    # 创建结果数组
    result = np.zeros_like(pic1)

    # 在alpha有效区域进行混合
    # 计算颜色通道，考虑各自的透明度
    result[mask[..., 0], :3] = (pic2[mask[..., 0], :3] * a2[mask[..., 0]] +
                                pic1[mask[..., 0], :3] * a1[mask[..., 0]] * (1.0 - a2[mask[..., 0]])) / alpha_out[mask[..., 0]]

    # 设置alpha通道
    result[..., 3:4] = alpha_out

    # 转回uint8
    return (result * 255.0).astype(np.uint8)

def background(width: int, height: int, color: MioColor):
    pass