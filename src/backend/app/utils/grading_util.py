import docker
import logging
import re
import os

# 初始化 Docker 客户端
docker_client = docker.from_env()


def run_grading(
    submission_code_dir: str,
    grading_image: str,
    # TODO: Add timeout parameter
) -> str:
    run_command = f"cp -rf /code/* . && sh /scripts/grading.sh"
    run_commands = ["sh", "-c", run_command]

    try:
        # 配置容器启动参数
        logging.info("Running grading container...")
        container = docker_client.containers.run(
            image=grading_image,  # 评分镜像
            volumes={
                submission_code_dir: {"bind": "/code", "mode": "ro"}
            },  # 挂载代码目录
            mem_limit="100m",  # 内存限制
            network_mode="none",  # 不使用网络
            # user="nobody",  # 使用非特权用户
            detach=True,  # 异步运行
            command=run_commands,  # 执行评分脚本
        )

        # 等待容器执行完成并获取输出
        container.wait()  # 等待容器停止
        logs = container.logs()  # 获取容器输出日志
        container.remove()  # 删除容器

        logging.info("container logs: %s", logs.decode("utf-8"))

        # 返回评分脚本的输出
        return logs.decode("utf-8")

    except docker.errors.DockerException as e:
        logging.error(f"Error while running grading container: {e}")
        return f"Error: {e}"
    except Exception as e:
        logging.error(f"Unknown error: {e}")
        return f"Error: {e}"


def parse_result(result: str) -> int:
    """e.g., 'Score: 90/100' -> 90"""
    try:
        score = int(re.search(r"Score: (\d+)", result).group(1))
    except AttributeError as e:
        raise ValueError(f"{result}")
    return score
