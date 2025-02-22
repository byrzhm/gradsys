from app.utils.security import is_safe_path, safe_extract
import zipfile
import pytest


def test_safe_path_detection():
    """测试危险路径检测"""
    assert is_safe_path("normal_dir/file.txt") is True
    assert is_safe_path("../hack.sh") is False
    assert is_safe_path("/absolute/path") is False


def test_malicious_zip_handling(tmp_path):
    """测试恶意ZIP文件处理"""
    malicious_zip = tmp_path / "bad.zip"

    # 创建包含危险路径的ZIP
    with zipfile.ZipFile(malicious_zip, "w") as z:
        z.writestr("../../etc/passwd", "hack")

    # 测试安全解压
    with pytest.raises(ValueError) as excinfo:
        safe_extract(malicious_zip, tmp_path)

    assert "危险文件路径" in str(excinfo.value)
