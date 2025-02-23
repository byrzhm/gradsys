import pytest
from app.utils import parse_result
from app.utils import docker_client
import os
from docker.models.containers import Container


def test_parse_result():
    """测试评分结果解析"""
    results = [
        "Score: 100/100",
        "Score: 0/100",
        "Score: 60/100",
        "Score: 99/100",
    ]
    expected = [100, 0, 60, 99]

    for result, expect in zip(results, expected):
        assert parse_result(result) == expect

    # test raise exception
    with pytest.raises(ValueError, match="invalid result"):
        parse_result("invalid result")


# Docker Tests


@pytest.fixture
def test_docker_image():
    docker_client.images.build(path=os.path.dirname(__file__), tag="test-image")
    yield
    docker_client.images.remove("test-image", force=True)


class TestDocker:

    def test_run_attach(self):
        result = docker_client.containers.run(
            image="alpine",
            command="echo hello world",
            detach=False,  # make return type to bytes
        )
        assert isinstance(result, bytes)
        assert result == b"hello world\n"

    def test_run_detach(self):
        container = docker_client.containers.run(
            image="alpine",
            command=["sh", "-c", "sleep 5 && echo hello world"],
            detach=True,  # make return type to container
        )
        assert isinstance(container, Container)
        container.wait()
        assert container.logs().decode("utf-8") == "hello world\n"  # remove "b" prefix
        container.remove()

    def test_fixture_image(self, test_docker_image):
        """测试容器运行"""
        container = docker_client.containers.run(
            image="test-image",
            volumes={os.path.dirname(__file__): {"bind": "/code", "mode": "ro"}},
            mem_limit="100m",
            network_mode="none",
            user="nobody",
            detach=True,
            # auto_remove=True,
            # !!! Don't use auto_remove
        )
        container.wait()
        assert container.logs().decode("utf-8").strip() == "score 90/100"
        container.remove()
