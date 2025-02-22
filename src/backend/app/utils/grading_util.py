import docker
import logging
import re

# 初始化 Docker 客户端
docker_client = docker.from_env()


def run_grading(
    submission_code_path: str,
    grading_script_path: str,
    grading_image: str,
    # TODO: Add timeout parameter
) -> str:
    # 读取评分脚本内容
    with open(grading_script_path, "r") as f:
        grading_script_content = f.read()

    cp_command = f"cp -rf /code/* ."
    run_command = f"{cp_command} && bash -c '{grading_script_content}'"

    try:
        # 配置容器启动参数
        container = docker_client.containers.run(
            image=grading_image,  # 评分镜像
            volumes={
                submission_code_path: {"bind": "/code", "mode": "ro"}
            },  # 挂载代码目录
            mem_limit="100m",  # 内存限制
            network_mode="none",  # 不使用网络
            user="nobody",  # 使用非特权用户
            detach=True,  # 异步运行
            auto_remove=True,  # 容器结束后自动删除
            command=run_command,  # 执行评分脚本
        )

        # 等待容器执行完成并获取输出
        container.wait()  # 等待容器停止
        logs = container.logs()  # 获取容器输出日志

        # 返回评分脚本的输出
        return logs.decode("utf-8")

    except docker.errors.DockerException as e:
        logging.error(f"Error while running grading container: {e}")
        return f"Error: {e}"
    except Exception as e:
        logging.error(f"Unknown error: {e}")
        return f"Error: {e}"


def parse_result(result: str) -> int:
    """e.g., 'score: 90/100' -> 90"""
    return int(re.search(r"score: (\d+)", result).group(1))
