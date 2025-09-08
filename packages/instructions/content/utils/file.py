import hashlib
from pathlib import Path

from django.conf import settings
from markitdown import MarkItDown


def get_file_md5(chunk):
    # 创建一个md5哈希对象
    md5_hash = hashlib.md5()
    # 打开文件并读取内容
    md5_hash.update(chunk)
    # 返回文件的MD5值，以十六进制表示
    return md5_hash.hexdigest()


def store_file(filename, hexcode, chunk):
    root_path = Path(settings.STORE_PATH)
    file_path = root_path.joinpath(hexcode).joinpath(filename)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'wb') as f:
        f.write(chunk)
    return file_path.absolute().replace(root_path.absolute(), ''), hexcode


def convert_file(file_path):
    md = MarkItDown(enable_plugins=True)  # 设置为 True 启用插件
    file_path = Path(settings.STORE_PATH, file_path)
    md.extract_images = True
    return md.convert(file_path)
