import colorsys


class MioColor:
    """
    Mio 中的颜色对象封装，用于一致化色彩处理

    可以直接传入BGRA颜色值或HEX字符串来初始化颜色对象
    """
    def __init__(self, b: int = 0, g: int = 0, r: int = 0, a: int = 255, hex_str: str = ""):
        self.B = 0  # 蓝色通道
        self.G = 0  # 绿色通道
        self.R = 0  # 红色通道
        self.A = 255  # 透明度通道

        if b:
            self.B = b
        if g:
            self.G = g
        if r:
            self.R = r
        if a:
            self.A = a
        if hex_str:
            if len(hex_str) == 6:
                self.from_hex_rgb(hex_str)
            elif len(hex_str) == 8:
                self.from_hex_rgba(hex_str)
            else:
                raise ValueError("Invalid hex string.")

    @staticmethod
    def _check_value_int(value: int):
        """
        检查颜色通道值是否合法
        :param value: 颜色通道值
        :return: 合法的颜色通道值
        """
        if value < 0:
            return 0
        if value > 255:
            return 255
        return value

    def from_rgb(self, r: int, g: int, b: int):
        """
        从 RGB 通道设置颜色
        :param r: 红色通道
        :param g: 绿色通道
        :param b: 蓝色通道
        :return: self
        """
        self.R = self._check_value_int(r)
        self.G = self._check_value_int(g)
        self.B = self._check_value_int(b)
        return self

    def from_rgba(self, r: int, g: int, b: int, a: int):
        """
        从 RGBA 通道设置颜色
        :param r: 红色通道
        :param g: 绿色通道
        :param b: 蓝色通道
        :param a: 透明度通道
        :return: self
        """
        self.R = self._check_value_int(r)
        self.G = self._check_value_int(g)
        self.B = self._check_value_int(b)
        self.A = self._check_value_int(a)
        return self

    def from_bgra(self, b: int, g: int, r: int, a: int):
        """
        从 BGRA 通道设置颜色
        :param b: 蓝色通道
        :param g: 绿色通道
        :param r: 红色通道
        :param a: 透明度通道
        :return: self
        """
        self.B = self._check_value_int(b)
        self.G = self._check_value_int(g)
        self.R = self._check_value_int(r)
        self.A = self._check_value_int(a)
        return self

    def from_bgr(self, b: int, g: int, r: int):
        """
        从 BGR 通道设置颜色
        :param b: 蓝色通道
        :param g: 绿色通道
        :param r: 红色通道
        :return: self
        """
        self.B = self._check_value_int(b)
        self.G = self._check_value_int(g)
        self.R = self._check_value_int(r)
        return self

    def from_hex_rgb(self, hex_str: str):
        # 如果传入的是十六进制字符串
        # 检测是否以#开头，如果是则去掉
        if hex_str.startswith("#"):
            hex_str = hex_str[1:]
        # 如果字符串长度不是6，则抛出异常
        if len(hex_str) != 6:
            raise ValueError("Invalid hex string.")
        # 将字符串转换为整数
        hex_value = int(hex_str, 16)
        # 分别获取RGB通道的值
        self.R = (hex_value >> 16) & 0xFF
        self.G = (hex_value >> 8) & 0xFF
        self.B = hex_value & 0xFF
        return self

    def from_hex_rgba(self, hex_str: str):
        # 如果传入的是十六进制字符串
        # 检测是否以#开头，如果是则去掉
        if hex_str.startswith("#"):
            hex_str = hex_str[1:]
        # 如果字符串长度不是8，则抛出异常
        if len(hex_str) != 8:
            raise ValueError("Invalid hex string.")
        # 将字符串转换为整数
        hex_value = int(hex_str, 16)
        # 分别获取RGBA通道的值
        self.R = (hex_value >> 24) & 0xFF
        self.G = (hex_value >> 16) & 0xFF
        self.B = (hex_value >> 8) & 0xFF
        self.A = hex_value & 0xFF
        return self

    def from_hsl(self, h: int, s: int, l: int):
        """
        从 HSL 通道设置颜色
        :param h: 色相
        :param s: 饱和度
        :param l: 亮度
        :return: self
        """
        # 转换 HSL 到 RGB
        r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
        # 乘以255并转换为整数
        self.R = int(r * 255)
        self.G = int(g * 255)
        self.B = int(b * 255)
        return self

    def from_cmyk(self, c: int, m: int, y: int, k: int):
        """
        从 CMYK 通道设置颜色
        :param c: 青色通道
        :param m: 洋红色通道
        :param y: 黄色通道
        :param k: 黑色通道
        :return: self
        """
        # 转换 CMYK 到 RGB
        r = 255 * (1 - c) * (1 - k)
        g = 255 * (1 - m) * (1 - k)
        b = 255 * (1 - y) * (1 - k)
        self.R = int(r)
        self.G = int(g)
        self.B = int(b)
        return self

    def to_rgb(self):
        """
        转换为 RGB 通道
        :return: r, g, b
        """
        return self.R, self.G, self.B

    def to_rgba(self):
        """
        转换为 RGBA 通道
        :return: r, g, b, a
        """
        return self.R, self.G, self.B, self.A

    def to_bgr(self):
        """
        转换为 BGR 通道
        :return: b, g, r
        """
        return self.B, self.G, self.R

    def to_bgra(self):
        """
        转换为 BGRA 通道
        :return: b, g, r, a
        """
        return self.B, self.G, self.R, self.A

    def to_hex_rgb(self):
        """
        转换为 RGB 十六进制字符串
        :return: 十六进制字符串
        """
        return "#{:02X}{:02X}{:02X}".format(self.R, self.G, self.B)

    def to_hex_rgba(self):
        """
        转换为 RGBA 十六进制字符串
        :return: 十六进制字符串
        """
        return "#{:02X}{:02X}{:02X}{:02X}".format(self.R, self.G, self.B, self.A)

    def to_hsl(self):
        """
        转换为 HSL 通道
        :return: h, s, l
        """
        r = self.R / 255
        g = self.G / 255
        b = self.B / 255
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return int(h * 360), int(s * 100), int(l * 100)

    def to_cmyk(self):
        """
        转换为 CMYK 通道
        :return: c, m, y, k
        """
        r = self.R / 255
        g = self.G / 255
        b = self.B / 255
        k = 1 - max(r, g, b)
        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)
        return int(c * 100), int(m * 100), int(y * 100), int(k * 100)