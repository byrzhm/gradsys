import os
import zipfile


def is_safe_path(path):
    """防御路径遍历攻击"""
    return not os.path.isabs(path) and ".." not in path


def safe_extract(zip_path, target_dir):
    """安全解压ZIP文件"""
    with zipfile.ZipFile(zip_path) as z:
        for name in z.namelist():
            if not is_safe_path(name):
                raise ValueError(f"危险文件路径: {name}")
        z.extractall(target_dir)
