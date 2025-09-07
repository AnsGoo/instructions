import hashlib
from pathlib import Path

from django.settings import STORE_PATH


def get_file_md5(chunk):
    # 创建一个md5哈希对象
    md5_hash = hashlib.md5()
    # 打开文件并读取内容
    md5_hash.update(chunk)
    # 返回文件的MD5值，以十六进制表示
    return md5_hash.hexdigest()


def store_file(filename, hexcode, chunk):
    file_path = Path(STORE_PATH).joinpath(hexcode).joinpath(filename)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'wb') as f:
        f.write(chunk)
    return file_path.absolute(), hexcode
