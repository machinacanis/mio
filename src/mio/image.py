from io import BytesIO
from os import PathLike
from pathlib import Path
from typing import Any

import cv2 as cv
import numpy as np
from numpy import ndarray, dtype

from .base import MioObject
from .color import MioColor
from .utils import alpha_mix


class MioImage(MioObject):
    """
    用于在 Mio 中使用的图像对象封装
    """
    def __init__(self, image: str | PathLike | ndarray[Any, dtype] | bytes | BytesIO | None = None):

        super().__init__()
        self.data: ndarray[Any, dtype] | None = None
        self.nametag: str = ""

        if image is not None:
            self.read(image)

    def __add__(self, other: 'MioImage') -> 'MioImage':
        """
        MioImage 对象的运算符重载，当两个 MioImage 对象相加时，会将后一个对象叠加到前一个对象上（相对位置不变）

        这个方法会返回一个新的 MioImage 对象，不会修改原有对象

        当另一个对象被加到当前对象上时，会继承第一个对象的属性

        注意，累计后的结果会退化到一个普通的 MioImage 对象，不会保留两个源对象的其他子类属性
        :param other:
        :return:
        """
        # TODO: 实现图像加法中的类型检查
        # 这里需要一个类型检查，如果传入的不是MioImage支持的类型，则抛出异常
        # 暂时没写
        # 将两个源对象的数据复制到新对象
        first_image = self.rasterisation()
        second_image = other.rasterisation()
        # 如果第二个对象的大小超出第一个对象，则裁剪到第一个对象的大小
        second_image.resize_without_scale(first_image.width, first_image.height)
        # 将两个图像叠加
        new_data = alpha_mix(first_image.data, second_image.data)
        # 创建新的 MioImage 对象
        new_image = MioImage()
        new_image.read(new_data)
        return new_image


    def _caculate_size(self):
        if self.data is not None:
            self.height, self.width = self.data.shape[:2]

    def copy(self):
        """
        复制当前对象，返回一个新的 MioImage 对象
        :return: MioImage
        """
        new_image = self
        return new_image


    def clear(self):
        """
        清除数据
        :return: self
        """
        self.data = None
        self.reset()  # 重置对象基本数据
        return self

    def rasterisation(self) -> 'MioImage':
        """
        栅格化，返回一个 MioImage 对象，不包含子类的额外属性和方法
        """
        # 这个方法用作一个接口，其他继承了 MioImage 的类可以通过这个方法返回一个降级成 MioImage 的对象
        # 根据背景色、背景透明度、自身透明度，将图像转换为带有背景色和透明度的图像
        if self.data is None:
            raise ValueError("No image data to rasterisation.")
        return self.copy()


    def read(self, image: str | PathLike | ndarray[Any, dtype] | bytes | BytesIO | None = None):
        # 首先判断传入的参数类型
        if image is None:
            self.data = None  # 如果没有传入参数，则将 data 设置为 None
        elif isinstance(image, str):
            # 传入的是一个字符串，尝试将其转换为Path对象
            image_path = Path(image)
            # 判断文件是否存在
            if not image_path.exists():
                raise FileNotFoundError(f"File {image_path} is not found.")
            # 尝试读取文件
            try:
                cv2_img = cv.imread(cv.samples.findFile(image_path.__str__()), cv.IMREAD_UNCHANGED)
                if cv2_img is None:
                    raise FileNotFoundError(f"File {image_path} is not found or is not an available file.")
                self.data = cv2_img
            except cv.error:
                raise FileNotFoundError(f"File {image_path} is not found or is not an available file.")
        elif isinstance(image, PathLike):
            # 传入的是一个文件路径，转换为Path对象
            image_path = Path(image)
            # 判断文件是否存在
            if not image_path.exists():
                raise FileNotFoundError(f"File {image_path} is not found.")
            # 尝试读取文件
            try:
                cv2_img = cv.imread(cv.samples.findFile(image_path.__str__()), cv.IMREAD_UNCHANGED)
                if cv2_img is None:
                    raise FileNotFoundError(f"File {image_path} is not found or is not an available file.")
                self.data = cv2_img
            except cv.error:
                raise FileNotFoundError(f"File {image_path} is not found or is not an available file.")
        elif isinstance(image, ndarray):
            # TODO: 如果传入的参数是ndarray类型，检测是否是所需类型的图像
            self.data = image
        elif isinstance(image, bytes):
            # 如果传入的参数是bytes类型，则直接读取
            try:
                nparr = np.frombuffer(image, np.uint8)
                cv2_img = cv.imdecode(nparr, cv.IMREAD_UNCHANGED)
                self.data = cv2_img
            except cv.error:
                raise ValueError("Invalid image bytes.")
        elif isinstance(image, BytesIO):
            # 如果传入的参数是BytesIO类型，则直接读取
            try:
                nparr = np.frombuffer(image.read(), np.uint8)
                cv2_img = cv.imdecode(nparr, cv.IMREAD_UNCHANGED)
                self.data = cv2_img
            except cv.error:
                raise ValueError("Invalid image bytes.")
        self._caculate_size()  # 计算图像的尺寸
        return self  # 返回自身，以支持链式调用


    def write(self, image: str | PathLike):
        """
        将图像写入进文件
        :param image: 文件路径
        :return:
        """
        if self.data is None:
            raise ValueError("No image data to write.")
        path = Path(image)
        # 判断文件是否存在
        if path.exists():
            raise FileExistsError(f"File {path} is already existed.")
        # 尝试写入文件
        try:
            cv.imwrite(path.__str__(), self.data)
        except cv.error:
            raise ValueError(f"Failed to write image to {path}.")

    def show(self):
        """
        显示图像，使用OpenCV的imshow方法，仅供调试使用，会导致程序阻塞
        :return:
        """
        if self.data is None:
            raise ValueError("No image data to show.")
        cv.imshow(self.nametag, self.data)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def resize(self, width: int, height: int, interpolation: int = cv.INTER_LINEAR):
        """
        调整图像尺寸，使用OpenCV的resize方法，支持多种插值方法，可以通过InterpolationMethods枚举类选择，也有对应的快捷方式，也可以直接传入OpenCV的插值方法枚举

        根据OpenCV的文档，对于放大图像，推荐使用INTER_LINEAR（线性）或INTER_CUBIC（三次），对于缩小图像，推荐使用INTER_AREA（区域）
        :param interpolation: 插值方法
        :param width: 宽度
        :param height: 高度
        :return: None
        """
        if self.data is None:
            raise ValueError("No image data to resize.")
        self.data = cv.resize(self.data, (width, height), interpolation=interpolation)
        self._caculate_size()  # 重新计算图像的尺寸
        return self

    def resize_by_ratio(self, ratio: float, interpolation: int = cv.INTER_LINEAR, x_ratio:float = 1.0, y_ratio: float = 1.0):
        """
        按照比例调整图像尺寸，可以通过x_ratio和y_ratio分别设置横向和纵向的比例，也可以通过ratio直接设置比例，如果设置了x_ratio和y_ratio，则对应方向上的ratio参数会被覆盖
        :param x_ratio: 横向比例
        :param y_ratio: 纵向比例
        :param ratio: 比例
        :param interpolation: 插值方法
        :return: None
        """
        if self.data is None:
            raise ValueError("No image data to resize.")
        # 如果传入的比例为0或1，则不进行任何操作
        if ratio == 0 or ratio == 1:
            return
        # 通过resize的fx和fy参数进行调整
        self.data = cv.resize(
            self.data,
            (0, 0),
            fx=x_ratio if x_ratio != 1.0 else ratio,  # 如果x_ratio不为1.0，则使用x_ratio，否则使用ratio
            fy=y_ratio if y_ratio != 1.0 else ratio,  # 如果y_ratio不为1.0，则使用y_ratio，否则使用ratio
            interpolation=interpolation
        )
        self._caculate_size()  # 重新计算图像的尺寸
        return self

    def cut(self, width: int, height: int):
        """
        裁剪图像，以左上角为基准，将图像裁剪为指定尺寸
        :param width: 宽度
        :param height: 高度
        :return: None
        """
        if self.data is None:
            raise ValueError("No image data to cut.")
        self.data = self.data[:height, :width]
        self._caculate_size()  # 重新计算图像的尺寸
        return self

    def cut_by_ratio(self, ratio: float, x_ratio: float = 1.0, y_ratio: float = 1.0):
        """
        按照比例裁剪图像，可以通过x_ratio和y_ratio分别设置横向和纵向的比例，也可以通过ratio直接设置比例，如果设置了x_ratio和y_ratio，则对应方向上的ratio参数会被覆盖
        :param x_ratio: 横向比例
        :param y_ratio: 纵向比例
        :param ratio: 比例
        :return: None
        """
        if self.data is None:
            raise ValueError("No image data to cut.")
        # 如果传入的比例为0或1，则不进行任何操作
        if ratio == 0 or ratio == 1:
            return
        # 通过切片进行裁剪
        self.data = self.data[:int(self.height * y_ratio if y_ratio != 1.0 else self.height * ratio), :int(self.width * x_ratio if x_ratio != 1.0 else self.width * ratio)]
        self._caculate_size()

    def free_cut(self, first_point: tuple[int, int], second_point: tuple[int, int]):
        """
        自由裁剪图像，根据指定的两个点坐标裁剪图像
        :param first_point: 第一个点的坐标
        :param second_point: 第二个点的坐标
        :return: None
        """
        if self.data is None:
            raise ValueError("No image data to cut.")
        self.data = self.data[first_point[1]:second_point[1], first_point[0]:second_point[0]]
        self._caculate_size()
        return self

    def expand(self, width: int, height: int):
        """
        扩展图像，以左上角为基准，将图像扩展为指定尺寸
        :param width: 宽度
        :param height: 高度
        :return: None
        """
        if self.data is None:
            raise ValueError("No image data to expand.")
        # 计算要扩展的尺寸
        expand_width = width - self.width
        expand_height = height - self.height
        # 向外扩展图像，填充背景
        self.data = cv.copyMakeBorder(
            self.data, 0, expand_height, 0, expand_width, cv.BORDER_CONSTANT, value=[0]
        )
        self._caculate_size()
        return self

    def expand_by_ratio(self, ratio: float, x_ratio: float = 1.0, y_ratio: float = 1.0):
        """
        按照比例扩展图像，可以通过x_ratio和y_ratio分别设置横向和纵向的比例，也可以通过ratio直接设置比例，如果设置了x_ratio和y_ratio，则对应方向上的ratio参数会被覆盖
        :param x_ratio: 横向比例
        :param y_ratio: 纵向比例
        :param ratio: 比例
        :return: None
        """
        if self.data is None:
            raise ValueError("No image data to expand.")
        # 如果传入的比例为0或1，则不进行任何操作
        if ratio == 0 or ratio == 1:
            return
        # 计算要扩展的尺寸
        expand_width = int(self.width * x_ratio if x_ratio != 1.0 else self.width * ratio) - self.width
        expand_height = int(self.height * y_ratio if y_ratio != 1.0 else self.height * ratio) - self.height
        # 向外扩展图像，填充背景
        self.data = cv.copyMakeBorder(
            self.data, 0, expand_height, 0, expand_width, cv.BORDER_CONSTANT, value=[0]
        )
        self._caculate_size()
        return self

    def resize_without_scale(self, width: int, height: int):
        """
        将图像调整为指定尺寸，不缩放图像，只是调整大小
        :param width: 宽度
        :param height: 高度
        :return: self
        """
        # 获取图像当前的尺寸
        current_width, current_height = self.get_size()
        # 计算尺寸差
        width_diff = width - current_width
        height_diff = height - current_height
        # 如果水平方向的差值大于0，则在右侧填充
        if width_diff > 0:
            self.expand(width, current_height)
            current_width = width
        # 如果水平方向的差值小于0，则在右侧裁剪
        elif width_diff < 0:
            self.cut(width, current_height)
            current_width = width
        # 如果垂直方向的差值大于0，则在底部填充
        if height_diff > 0:
            self.expand(current_width, height)
        # 如果垂直方向的差值小于0，则在底部裁剪
        elif height_diff < 0:
            self.cut(current_width, height)
        self._caculate_size()  # 重新计算图像的尺寸
        return self




    def border_radius(self):
        pass
