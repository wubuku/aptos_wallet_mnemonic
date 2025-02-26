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



## 项目打包与分发

本项目可以通过多种方式打包分发，以便在不同环境中使用。

### 打包方式比较

| 方式 | 目标机器需要Python | 包含依赖 | 离线运行 | 文件大小 | 启动速度 | 适用场景 |
|-----|----------------|----------|---------|--------|---------|---------|
| Wheel包 | ✅ 需要 | ❌ 不包含 | ❌ 需联网 | 小 | 快 | 开发环境、有网络连接 |
| Shiv | ✅ 需要 | ✅ 包含 | ✅ 支持 | 中等 | 快 | 有Python的离线环境 |
| PyInstaller | ❌ 不需要 | ✅ 包含 | ✅ 支持 | 大 | 慢 | 完全独立的可执行文件 |
| Nuitka | ❌ 不需要 | ✅ 包含 | ✅ 支持 | 大 | 快 | 追求性能的场景 |

### 1. 创建Wheel包

生成标准Python包，适合在有网络连接的环境中使用：

```bash
# 构建wheel包
poetry build

# 构建结果位于dist/目录下
# 例如：dist/aptos_wallet_mnemonic-0.2.0-py3-none-any.whl
```

目标机器上安装方法：

```bash
pip install aptos_wallet_mnemonic-0.2.0-py3-none-any.whl
```

**注意**：安装wheel包时，pip会自动从PyPI下载并安装所有依赖项。wheel包**不包含**依赖代码。

### 2. 使用Shiv打包（推荐用于离线环境）

如果目标机器已安装Python但不希望联网下载依赖，Shiv是理想选择：

```bash
# 安装shiv
poetry add shiv --dev

# 打包应用及其所有依赖到单个.pyz文件
poetry run shiv -c aptos_wallet_mnemonic -o aptos_wallet.pyz .
```

目标机器上使用方法：

```bash
# 直接运行（如果有执行权限）
./aptos_wallet.pyz

# 或通过Python解释器运行
python aptos_wallet.pyz
```

**优势**：包含所有依赖，无需联网安装，文件大小适中，启动快速。

### 3. 使用PyInstaller创建独立可执行文件

生成完全独立的可执行文件，目标机器无需安装Python：

```bash
# 安装PyInstaller
poetry add pyinstaller --dev

# 打包应用
poetry run pyinstaller --onefile aptos_wallet_mnemonic.py
```

打包结果位于`dist/`目录下，可以直接在目标机器上运行，无需任何依赖。

**注意**：生成的文件体积较大，包含完整的Python运行环境。

### 4. 使用Nuitka编译为本地代码

将Python代码编译为C并生成本地可执行文件，性能更好：

```bash
# 安装Nuitka
poetry add nuitka --dev

# 编译应用
poetry run python -m nuitka --follow-imports aptos_wallet_mnemonic.py
```

**优势**：运行速度快，保护源代码，无需Python环境。

### 5. 导出依赖列表

如果只需要导出项目依赖：

```bash
# 导出为requirements.txt
poetry export -f requirements.txt > requirements.txt
```

目标机器上安装依赖：

```bash
pip install -r requirements.txt
```

### 推荐分发方案

1. **开发环境**：使用`poetry build`创建wheel包
2. **有Python的离线环境**：使用`shiv`创建独立的`.pyz`文件（最佳平衡方案）
3. **完全独立部署**：使用`PyInstaller`或`Nuitka`创建独立可执行文件

根据目标环境选择合适的打包方式，可以大大简化部署和使用过程。


## 使用 Docker 构建和运行

### 构建 Docker 镜像
docker build -t aptos-wallet-env .

### 运行容器
```bash
# 交互式 shell
docker run -it --rm aptos-wallet-env

# 运行特定 Python 脚本
docker run -it --rm aptos-wallet-env python3 aptos_wallet_mnemonic.py

# 端口映射（未来 Node.js 服务）
docker run -it --rm -p 3000:3000 aptos-wallet-env
```


## AI 生成的 Go 版本（待验证）

可以通过以下方式测试验证：
1. 使用相同助记词分别用 Python 和 Go 版本生成账户
2. 比较两者生成的地址和私钥是否匹配
3. 使用生成的配置文件尝试与 Aptos 网络交互

```go
package main

import (
	"crypto/ed25519"
	"crypto/hmac"
	"crypto/sha512"
	"encoding/binary"
	"encoding/hex"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/tyler-smith/go-bip39"
)

const (
	BIP39_SALT_MODIFIER = "mnemonic"
	BIP39_PBKDF2_ROUNDS = 2048
	BIP32_PRIVDEV       = 0x80000000
	ACCOUNTS_DIR        = "aptos_accounts"

	CONFIG_TEMPLATE = `---
profiles:
  default:
    network: Testnet
    private_key: "0x%s"
    public_key: "0x%s"
    account: %s
    rest_url: "https://fullnode.testnet.aptoslabs.com"
    faucet_url: "https://faucet.testnet.aptoslabs.com"
`
)

// Key represents an Aptos account key pair
type Key struct {
	PrivateKey ed25519.PrivateKey
	PublicKey  ed25519.PublicKey
}

// Converts a derivation path string to a slice of indices
func parseDerivationPath(path string) ([]uint32, error) {
	if !strings.HasPrefix(path, "m/") {
		return nil, fmt.Errorf("invalid derivation path: %s", path)
	}

	path = strings.TrimPrefix(path, "m/")
	segments := strings.Split(path, "/")
	indices := make([]uint32, len(segments))

	for i, segment := range segments {
		var value uint32
		if strings.HasSuffix(segment, "'") {
			segment = strings.TrimSuffix(segment, "'")
			hardened := true
			_, err := fmt.Sscanf(segment, "%d", &value)
			if err != nil {
				return nil, err
			}
			if hardened {
				value += BIP32_PRIVDEV
			}
		} else {
			_, err := fmt.Sscanf(segment, "%d", &value)
			if err != nil {
				return nil, err
			}
		}
		indices[i] = value
	}

	return indices, nil
}

// Derives a child key from parent key and chain code
func deriveChildKey(parentKey, parentChainCode []byte, index uint32) ([]byte, []byte) {
	var data []byte
	if index >= BIP32_PRIVDEV {
		// Hardened derivation
		data = append([]byte{0x00}, parentKey...)
	} else {
		// Normal derivation (not used in Aptos)
		pub := ed25519.PrivateKey(parentKey).Public().(ed25519.PublicKey)
		data = pub
	}

	// Append index in big-endian form
	indexBytes := make([]byte, 4)
	binary.BigEndian.PutUint32(indexBytes, index)
	data = append(data, indexBytes...)

	// Calculate HMAC-SHA512
	hmacSha512 := hmac.New(sha512.New, parentChainCode)
	hmacSha512.Write(data)
	I := hmacSha512.Sum(nil)

	// Split into key and chain code
	childKey := I[:32]
	childChainCode := I[32:]

	return childKey, childChainCode
}

// Derives the master key from seed
func computeMasterKey(seed []byte) ([]byte, []byte) {
	hmacSha512 := hmac.New(sha512.New, []byte("ed25519 seed"))
	hmacSha512.Write(seed)
	I := hmacSha512.Sum(nil)

	// Split into master key and chain code
	masterKey := I[:32]
	chainCode := I[32:]

	return masterKey, chainCode
}

// Derives private key from mnemonic and derivation path
func derivePrivateKey(mnemonic, path string) (ed25519.PrivateKey, error) {
	// Generate seed from mnemonic
	seed := bip39.NewSeed(mnemonic, "")

	// Generate master key
	masterKey, chainCode := computeMasterKey(seed)

	// Parse derivation path
	indices, err := parseDerivationPath(path)
	if err != nil {
		return nil, err
	}

	// Derive child key
	key := masterKey
	code := chainCode
	for _, index := range indices {
		key, code = deriveChildKey(key, code, index)
	}

	// Create Ed25519 private key
	privateKey := ed25519.NewKeyFromSeed(key)
	return privateKey, nil
}

// Creates a new key from private key bytes
func newKeyFromPrivateKey(privateKey ed25519.PrivateKey) *Key {
	return &Key{
		PrivateKey: privateKey,
		PublicKey:  privateKey.Public().(ed25519.PublicKey),
	}
}

// Returns the hexadecimal representation of the private key
func (k *Key) PrivateKeyHex() string {
	return hex.EncodeToString(k.PrivateKey.Seed())
}

// Returns the hexadecimal representation of the public key
func (k *Key) PublicKeyHex() string {
	return hex.EncodeToString(k.PublicKey)
}

// Returns the Aptos account address
func (k *Key) Address() string {
	return hex.EncodeToString(k.PublicKey)
}

func main() {
	// Create root directory
	err := os.MkdirAll(ACCOUNTS_DIR, 0755)
	if err != nil {
		fmt.Printf("Error creating directory: %v\n", err)
		return
	}

	// Generate mnemonic (24 words for 256-bit entropy)
	entropy, err := bip39.NewEntropy(256)
	if err != nil {
		fmt.Printf("Error generating entropy: %v\n", err)
		return
	}
	
	mnemonic, err := bip39.NewMnemonic(entropy)
	if err != nil {
		fmt.Printf("Error generating mnemonic: %v\n", err)
		return
	}
	
	fmt.Println(mnemonic)

	// Save mnemonic to file
	mnemonicFile := filepath.Join(ACCOUNTS_DIR, "aptos_mnemonic.txt")
	err = os.WriteFile(mnemonicFile, []byte(mnemonic), 0644)
	if err != nil {
		fmt.Printf("Error saving mnemonic: %v\n", err)
		return
	}

	// Generate 10 accounts from the mnemonic
	for i := 0; i < 10; i++ {
		// Derive private key using BIP44 path
		path := fmt.Sprintf("m/44'/637'/%d'/0'/0'", i)
		
		privateKey, err := derivePrivateKey(mnemonic, path)
		if err != nil {
			fmt.Printf("Error deriving private key: %v\n", err)
			continue
		}
		
		key := newKeyFromPrivateKey(privateKey)
		
		fmt.Printf("(%d) %s %s 0x%s\n", 
			i, path, key.Address(), key.PrivateKeyHex())
		
		// Create account directory structure
		accountDir := filepath.Join(ACCOUNTS_DIR, key.Address())
		aptosConfigDir := filepath.Join(accountDir, ".aptos")
		configFile := filepath.Join(aptosConfigDir, "config.yaml")
		
		// Skip if config file already exists
		if _, err := os.Stat(configFile); err == nil {
			continue
		}
		
		// Create directories
		err = os.MkdirAll(aptosConfigDir, 0755)
		if err != nil {
			fmt.Printf("Error creating directory: %v\n", err)
			continue
		}
		
		// Prepare config file content
		configContent := fmt.Sprintf(CONFIG_TEMPLATE,
			key.PrivateKeyHex(),
			key.PublicKeyHex(),
			key.Address(),
		)
		
		// Write config file
		err = os.WriteFile(configFile, []byte(configContent), 0644)
		if err != nil {
			fmt.Printf("Error writing config file: %v\n", err)
			continue
		}
	}
}
```

