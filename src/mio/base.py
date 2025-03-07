class MioObject:
    """
    描述 Mio 的基本对象
    """
    def __init__(self):
        self.x: int = 0  # x 坐标
        self.y: int = 0  # y 坐标
        self.width: int = 0  # 宽度
        self.height: int = 0  # 高度

    def reset(self):
        """
        重置对象
        :return: self
        """
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        return self

    def get_position(self):
        """
        获取位置坐标
        :return: x, y
        """
        return self.x, self.y

    def set_position(self, x: int, y: int):
        """
        设置位置坐标
        :param x: x 坐标
        :param y: y 坐标
        :return: self
        """
        self.x = x
        self.y = y
        return self

    def get_size(self):
        """
        获取尺寸
        :return: width, height
        """
        return self.width, self.height

    def set_size(self, width: int, height: int):
        """
        设置尺寸
        :param width: 宽度
        :param height: 高度
        :return: self
        """
        self.width = width
        self.height = height
        return self

    def get_area(self):
        """
        获取面积
        :return: 面积大小（单位：平方像素）
        """
        return self.width * self.height

    def get_center(self):
        """
        获取中心坐标
        :return: x, y
        """
        return self.x + self.width / 2, self.y + self.height / 2

    def get_center_int(self):
        """
        获取中心坐标（整数）
        :return: x, y
        """
        return int(self.x + self.width / 2), int(self.y + self.height / 2)

    def get_box(self):
        """
        获取包围盒坐标，以左上、右上、左下、右下四个点的坐标表示
        :return: (x1, y1), (x2, y1), (x1, y2), (x2, y2)
        """
        return self.left_top(), self.right_top(), self.left_bottom(), self.right_bottom()

    def left_top(self):
        """
        获取左上角坐标
        :return: x, y
        """
        return self.x, self.y

    def right_top(self):
        """
        获取右上角坐标
        :return: x, y
        """
        return self.x + self.width, self.y

    def left_bottom(self):
        """
        获取左下角坐标
        :return: x, y
        """
        return self.x, self.y + self.height

    def right_bottom(self):
        """
        获取右下角坐标
        :return: x, y
        """
        return self.x + self.width, self.y + self.height

    def move(self, delta_x: int, delta_y: int):
        """
        移动对象
        :param delta_x: x 坐标偏移量
        :param delta_y: y 坐标偏移量
        :return: self
        """
        self.x += delta_x
        self.y += delta_y
        return self

