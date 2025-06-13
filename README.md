# Layer Peel

[![PyPI version](https://badge.fury.io/py/layer-peel.svg)](https://badge.fury.io/py/layer-peel)
[![Python Support](https://img.shields.io/pypi/pyversions/layer-peel.svg)](https://pypi.org/project/layer-peel/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

一个用于递归解压缩多层嵌套压缩文件的Python库。

## ✨ 特性

- 🔄 **递归解压缩**: 自动处理嵌套的压缩文件
- 📦 **多格式支持**: 支持 ZIP、TAR、TGZ、7Z、RAR 等格式
- 🚀 **流式处理**: 内存友好的流式解压缩
- 🎯 **自动检测**: 智能识别压缩文件格式
- 🛡️ **异常处理**: 完善的错误处理和日志记录
- 🔧 **命令行工具**: 提供易用的CLI接口
- 📝 **完整文档**: 详细的API文档和使用示例
- ⚡ **现代开发**: 使用 uv 进行极速依赖管理和构建

## 🚀 快速开始

### 安装

#### 使用 pip 安装

```bash
pip install layer-peel
```

#### 使用 uv 安装（推荐）

```bash
# 安装 uv（如果尚未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 使用 uv 安装 layer-peel
uv add layer-peel

# 或者在临时环境中运行
uvx layer-peel --help
```

### 基本使用

#### 作为Python库使用

```python
from layer_peel import extract

# 解压缩嵌套的压缩文件
with open('nested_archive.zip', 'rb') as f:
    for file_data, file_path, mime_type in extract(f, 'nested_archive.zip'):
        print(f"提取文件: {file_path}")

        # 保存文件
        with open(file_path.replace('!', '_'), 'wb') as output:
            for chunk in file_data:
                output.write(chunk)
```

#### 使用命令行工具

```bash
# 基本用法
layer-peel archive.zip

# 指定输出目录
layer-peel archive.zip -o /tmp/extracted

# 设置递归深度
layer-peel archive.zip -d 10

# 静默模式
layer-peel archive.zip --quiet

# 详细模式
layer-peel archive.zip --verbose
```

## 📖 详细文档

### API 参考

#### `extract(data, source_path, chunk_size=65536, lifespan_manager=lifespan, depth=5)`

递归解压缩多层嵌套的压缩文件。

**参数:**
- `data`: 输入数据，可以是字节流迭代器或文件对象
- `source_path`: 源文件路径，用于标识和日志记录
- `chunk_size`: 读取数据的块大小，默认64KB
- `lifespan_manager`: 生命周期管理器，用于进度跟踪
- `depth`: 最大递归深度，防止无限递归，默认5层

**返回:**
生成器，产生 `(file_data, file_path, mime_type)` 元组

**示例:**
```python
import layer_peel

with open('complex_archive.zip', 'rb') as f:
    for file_data, file_path, mime_type in layer_peel.extract(f, 'complex_archive.zip'):
        print(f"文件: {file_path}")
        print(f"类型: {mime_type}")

        # 处理文件数据
        content = b''.join(file_data)
        print(f"大小: {len(content)} 字节")
```

### 支持的格式

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| ZIP | .zip | 最常见的压缩格式 |
| TAR | .tar | Unix/Linux 归档格式 |
| TGZ/TAR.GZ | .tgz, .tar.gz | Gzip压缩的TAR |
| 7Z | .7z | 7-Zip压缩格式 |
| RAR | .rar | WinRAR压缩格式 |

### 高级用法

#### 自定义生命周期管理器

```python
from contextlib import contextmanager
from layer_peel import extract

@contextmanager
def custom_progress(path):
    print(f"🚀 开始处理: {path}")
    try:
        yield
    finally:
        print(f"✅ 完成处理: {path}")

with open('archive.zip', 'rb') as f:
    for file_data, file_path, mime_type in extract(
        f, 'archive.zip', lifespan_manager=custom_progress
    ):
        # 处理文件...
        pass
```

#### 处理编码问题

```python
from layer_peel.utils import fix_encoding

# 修复文件名编码
raw_filename = b'\xe4\xb8\xad\xe6\x96\x87.txt'
decoded_filename = fix_encoding(raw_filename)
print(decoded_filename)  # 输出: 中文.txt
```

#### 检测文件类型

```python
from layer_peel.utils import get_mime_type

with open('unknown_file', 'rb') as f:
    data = f.read(1024)  # 读取前1KB
    mime_type = get_mime_type(data)
    print(f"文件类型: {mime_type}")
```

## 🛠️ 开发

### 使用 uv 进行依赖管理

本项目使用 [uv](https://docs.astral.sh/uv/) 作为Python包和项目管理工具，提供极快的依赖解析和安装速度。

#### 安装 uv

```bash
# macOS 和 Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 或者使用 pip 安装
pip install uv
```

#### 环境设置

```bash
# 克隆仓库
git clone https://github.com/LaciaProject/layer_peel.git
cd layer-peel

# 使用 uv 创建虚拟环境（自动检测 Python 版本）
uv venv

# 激活虚拟环境
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate     # Windows

# 安装项目依赖（包括开发依赖）
uv pip install -e ".[dev,test,docs]"

# 或者使用 uv sync 同步锁定的依赖
uv sync --all-extras
```

#### 依赖管理

```bash
# 添加新的运行时依赖
uv add requests

# 添加开发依赖
uv add --dev pytest-xdist

# 添加可选依赖组
uv add --optional docs sphinx

# 移除依赖
uv remove requests

# 更新所有依赖到最新版本
uv lock --upgrade

# 更新特定依赖
uv lock --upgrade-package requests

# 查看依赖树
uv tree

# 检查依赖冲突
uv pip check
```

#### Python 版本管理

```bash
# 安装特定 Python 版本
uv python install 3.11 3.12

# 查看已安装的 Python 版本
uv python list

# 为项目固定 Python 版本
uv python pin 3.11

# 使用特定 Python 版本创建虚拟环境
uv venv --python 3.12
```

#### 运行脚本和工具

```bash
# 在虚拟环境中运行命令
uv run python -m pytest

# 运行项目脚本
uv run layer-peel --help

# 临时运行工具（无需安装）
uvx ruff check src/

# 安装全局工具
uv tool install ruff
```

#### 构建和发布

```bash
# 构建包
uv build

# 发布到 PyPI（需要配置认证）
uv publish

# 发布到测试 PyPI
uv publish --repository testpypi
```

#### 锁文件管理

项目使用 `uv.lock` 文件来锁定精确的依赖版本，确保在不同环境中的一致性：

```bash
# 生成/更新锁文件
uv lock

# 从锁文件安装依赖
uv sync

# 仅安装生产依赖
uv sync --no-dev

# 安装特定依赖组
uv sync --extra docs
```

#### 性能优势

使用 uv 相比传统工具的优势：

- **🚀 极速安装**: 比 pip 快 10-100 倍
- **🔒 可靠锁定**: 确保跨环境的一致性
- **💾 缓存优化**: 全局缓存减少重复下载
- **🛠️ 统一工具**: 替代 pip、pip-tools、virtualenv、poetry 等
- **🐍 Python 管理**: 内置 Python 版本管理

### 传统开发方式（可选）

如果您更喜欢使用传统工具：

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate

# 安装开发依赖
pip install -e ".[dev]"

# 安装pre-commit钩子
pre-commit install
```

### 运行测试

使用 uv 运行测试：

```bash
# 运行所有测试
uv run pytest

# 运行测试并生成覆盖率报告
uv run pytest --cov=layer_peel --cov-report=html

# 运行特定测试
uv run pytest tests/test_extract.py

# 并行运行测试（需要安装 pytest-xdist）
uv run pytest -n auto

# 运行测试并显示详细输出
uv run pytest -v

# 仅运行失败的测试
uv run pytest --lf
```

### 代码格式化和检查

使用 uv 进行代码质量检查：

```bash
# 检查代码质量和格式
uv run ruff check src/ tests/

# 自动修复可修复的问题
uv run ruff check --fix src/ tests/

# 格式化代码
uv run ruff format src/ tests/

# 类型检查
uv run mypy src/

# 运行所有检查（推荐在提交前运行）
uv run pre-commit run --all-files
```

### 一键开发环境设置

为了简化开发环境设置，您可以使用以下一键命令：

```bash
# 完整的开发环境设置
git clone https://github.com/LaciaProject/layer_peel.git && \
cd layer-peel && \
uv venv && \
source .venv/bin/activate && \
uv sync --all-extras && \
pre-commit install && \
echo "✅ 开发环境设置完成！"
```

## 🤝 贡献

我们欢迎各种形式的贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细信息。

### 贡献指南

1. Fork 这个仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📝 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解版本更新历史。

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [python-magic](https://github.com/ahupp/python-magic) - 文件类型检测
- [chardet](https://github.com/chardet/chardet) - 字符编码检测
- [py7zr](https://github.com/miurahr/py7zr) - 7Z格式支持
- [rarfile](https://github.com/markokr/rarfile) - RAR格式支持
- [stream-unzip](https://github.com/uktrade/stream-unzip) - 流式ZIP解压

## 📞 支持

如果你遇到问题或有疑问：

- 📋 [提交Issue](https://github.com/LaciaProject/layer_peel/issues)
- 💬 [讨论区](https://github.com/LaciaProject/layer_peel/discussions)
---

<div align="center">
Made with ❤️ by the Layer Peel Contributors
</div>
