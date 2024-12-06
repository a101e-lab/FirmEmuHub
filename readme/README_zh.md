# IoT 基准测试模拟器

[English](../README.md) | [中文](README_zh.md)

此脚本旨在使用 Docker 容器模拟 IoT 固件。它根据指定的基准测试配置构建并运行 Docker 镜像，并尝试在容器内启动服务。

## 前置要求

- Python 3.x
- Docker

## 安装

1. **克隆仓库：**

   ```bash
   git clone git@github.com:a101e-lab/iot-benchmark.git
   cd iot-benchmark
   ```

2. **安装所需的 Python 包：**

   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

1. **准备基准测试配置：**

   确保在基准测试目录中有 `benchmark.yml` 文件。该文件应包含构建和运行 Docker 容器所需的配置。

2. **运行脚本（必要时使用 `sudo`）：**

   ```bash
   sudo python3 iot-benchmark/emulation.py -b <path-to-benchmark-directory>
   ```

   将 `<path-to-benchmark-directory>` 替换为包含 `benchmark.yml` 文件的基准测试目录路径。

   **注意：** 由于 Docker 命令可能需要提升权限，因此可能需要使用 `sudo`。

## 故障排除

- 确保 Docker 正在运行且可以从命令行访问
- 验证 `benchmark.yml` 文件格式正确且包含所有必要字段
- 检查 Docker 日志以排查容器启动问题

## 许可证

本项目采用 Apache 2.0 许可证 - 详见 [LICENSE](../LICENSE) 文件。