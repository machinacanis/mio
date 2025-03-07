class ImageSizeNotMatchError(Exception):
    """
    图像大小不匹配错误
    """
    def __init__(self, message):
        super().__init__(message)