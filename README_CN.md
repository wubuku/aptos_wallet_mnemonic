# 如何运行这个 Aptos Wallet Mnemonic 项目

## 问题背景
需要运行一个基于 Python 的 Aptos 钱包助记词生成工具，项目使用 Poetry 进行依赖管理。

## 环境准备
1. 确保已安装 Python (3.7+)
2. 安装 Poetry（如果尚未安装）：
```bash
pip install poetry
```

## 运行步骤

### 1. 检查项目依赖
查看项目依赖的两个主要来源：
- `pyproject.toml` 文件中的依赖声明
- Python 代码中的 import 语句

### 2. 确保 pyproject.toml 配置正确
确保项目名称不会与依赖包冲突：
```toml
[tool.poetry]
name = "aptos-wallet-mnemonic"  # 不要使用 "aptos-sdk"
version = "0.1.0"
description = "Python project about generate mnemonic to aptos hd-wallet"
authors = ["Your Name"]

[tool.poetry.dependencies]
python = ">=3.7,<4.0"
httpx = "^0.23.0"
PyNaCl = "^1.5.0"
aiohttp = "^3.8.0"
mnemonic = "^0.20"
aptos-sdk = "^0.2.0"
ecdsa = "^0.18.0"
```

### 3. 安装依赖
在项目目录下执行：
```bash
poetry install
```

### 4. 处理依赖冲突
如果遇到 "lock file is not consistent" 警告，执行：
```bash
poetry lock --no-update
```

### 5. 运行项目
使用 Poetry 运行 Python 脚本：
```bash
poetry run python aptos_wallet_mnemonic.py
```

## 常见问题处理

### ModuleNotFoundError
如果遇到模块未找到错误：
1. 检查 `pyproject.toml` 是否包含该依赖
2. 添加缺失的依赖后执行 `poetry install`

### 依赖版本冲突
如果遇到版本解析失败：
1. 尝试 `poetry lock --no-update`
2. 如果还是失败，可以在 `pyproject.toml` 中调整版本要求
3. 最后手段：删除 `poetry.lock` 文件并重新生成

## 注意事项
1. 不要直接使用 `pip install`，应该通过 Poetry 管理依赖
2. 确保所有依赖都在 `pyproject.toml` 中正确声明
3. 代码中的 import 语句应该与 `pyproject.toml` 中的依赖保持一致

