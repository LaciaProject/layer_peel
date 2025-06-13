# 贡献指南

感谢您对 Layer Peel 项目的关注！我们欢迎各种形式的贡献，包括但不限于：

- 🐛 报告 Bug
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 提交代码修复或新功能
- 🧪 添加测试用例
- 🌐 翻译文档

## 🚀 快速开始

### 环境准备

1. **Fork 仓库**
   ```bash
   # 在 GitHub 上 fork 仓库，然后克隆到本地
   git clone https://github.com/yourusername/layer-peel.git
   cd layer-peel
   ```

2. **设置开发环境**
   ```bash
   # 创建虚拟环境
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或者 venv\Scripts\activate  # Windows

   # 安装开发依赖
   pip install -e ".[dev,test,docs]"

   # 安装 pre-commit 钩子
   pre-commit install
   ```

3. **验证环境**
   ```bash
   # 运行测试确保环境正常
   pytest

   # 检查代码格式和质量
   ruff check src/ tests/
   ruff format --check src/ tests/

   # 类型检查
   mypy src/
   ```

## 📋 开发流程

### 1. 创建分支

```bash
# 从 main 分支创建新的功能分支
git checkout -b feature/your-feature-name

# 或者修复 bug
git checkout -b fix/bug-description
```

### 2. 开发代码

- 遵循现有的代码风格和约定
- 添加必要的测试用例
- 更新相关文档
- 确保所有测试通过

### 3. 提交代码

```bash
# 添加更改
git add .

# 提交更改（使用有意义的提交信息）
git commit -m "feat: add support for new archive format"

# 推送到你的 fork
git push origin feature/your-feature-name
```

### 4. 创建 Pull Request

1. 在 GitHub 上创建 Pull Request
2. 填写 PR 模板中的信息
3. 等待代码审查
4. 根据反馈进行修改

## 📝 代码规范

### Python 代码风格

我们使用以下工具来保持代码质量：

- **Ruff**: 代码格式化、导入排序和代码检查（替代 Black、isort、flake8）
- **MyPy**: 类型检查

```bash
# 检查代码质量和格式
ruff check src/ tests/

# 自动修复可修复的问题
ruff check --fix src/ tests/

# 格式化代码
ruff format src/ tests/

# 类型检查
mypy src/
```

### 提交信息规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**类型 (type):**
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式修改
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

**示例:**
```
feat: add support for RAR5 format
fix: handle corrupted ZIP files gracefully
docs: update API documentation
test: add unit tests for encoding detection
```

## 🧪 测试

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_extract.py

# 运行特定测试函数
pytest tests/test_extract.py::test_zip_extraction

# 生成覆盖率报告
pytest --cov=layer_peel --cov-report=html
```

### 编写测试

- 为新功能添加测试用例
- 确保测试覆盖率不降低
- 使用有意义的测试名称
- 包含正常情况和边界情况的测试

```python
def test_extract_nested_zip():
    """测试嵌套 ZIP 文件的解压缩"""
    # 测试实现...
    pass

def test_extract_corrupted_archive():
    """测试处理损坏的压缩文件"""
    # 测试实现...
    pass
```

## 📚 文档

### 文档类型

1. **API 文档**: 在代码中使用 docstring
2. **用户指南**: 更新 README.md
3. **开发文档**: 更新相关的 .md 文件

### 文档风格

- 使用清晰、简洁的语言
- 提供实际的代码示例
- 包含参数说明和返回值描述
- 添加适当的类型注解

```python
def extract(
    data: Union[Iterator[bytes], RawIOBase],
    source_path: str,
    chunk_size: int = 65536,
    depth: int = 5,
) -> Generator[tuple[Iterator[bytes], str, Optional[str]], Any, None]:
    """
    递归解压缩多层嵌套的压缩文件

    Args:
        data: 输入数据，可以是字节流迭代器或文件对象
        source_path: 源文件路径，用于标识和日志记录
        chunk_size: 读取数据的块大小，默认64KB
        depth: 最大递归深度，防止无限递归，默认5层

    Yields:
        tuple[Iterator[bytes], str, Optional[str]]:
            文件数据流、路径和MIME类型

    Raises:
        MaxDepthExceededError: 超过最大递归深度
        ExtractionError: 解压缩过程中发生错误
    """
```

## 🐛 报告 Bug

### Bug 报告模板

请使用以下模板报告 Bug：

```markdown
## Bug 描述
简要描述遇到的问题

## 重现步骤
1. 执行 '...'
2. 点击 '....'
3. 滚动到 '....'
4. 看到错误

## 期望行为
描述你期望发生的情况

## 实际行为
描述实际发生的情况

## 环境信息
- OS: [e.g. Ubuntu 20.04]
- Python 版本: [e.g. 3.10.0]
- Layer Peel 版本: [e.g. 0.1.0]

## 附加信息
添加任何其他有助于解决问题的信息
```

## 💡 功能建议

### 功能请求模板

```markdown
## 功能描述
简要描述建议的功能

## 问题背景
描述这个功能要解决的问题

## 建议的解决方案
描述你希望如何实现这个功能

## 替代方案
描述你考虑过的其他解决方案

## 附加信息
添加任何其他相关信息或截图
```

## 🔍 代码审查

### 审查清单

在提交 PR 之前，请确保：

- [ ] 代码遵循项目的编码规范
- [ ] 所有测试都通过
- [ ] 添加了必要的测试用例
- [ ] 更新了相关文档
- [ ] 提交信息符合规范
- [ ] 没有引入新的依赖（如有必要，请在 PR 中说明）

### 审查过程

1. 自动化检查（CI/CD）
2. 代码审查（至少一个维护者）
3. 测试验证
4. 合并到主分支

## 🏷️ 发布流程

版本发布由维护者负责：

1. 更新版本号
2. 更新 CHANGELOG.md
3. 创建 Git 标签
4. 发布到 PyPI
5. 创建 GitHub Release

## 📞 获取帮助

如果你在贡献过程中遇到问题：

- 📋 [查看现有 Issues](https://github.com/yourusername/layer-peel/issues)
- 💬 [参与讨论](https://github.com/yourusername/layer-peel/discussions)
- 📧 发送邮件到 contributors@layer-peel.dev

## 🙏 致谢

感谢所有为 Layer Peel 项目做出贡献的开发者！

---

再次感谢您的贡献！每一个贡献都让 Layer Peel 变得更好。
