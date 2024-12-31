import sys
import os
from aiohttp import Payload
from mnemonic import Mnemonic
from utils import PublicKeyUtils
from aptos_sdk.account import Account
from aptos_sdk.client import FaucetClient, RestClient

FAUCET_URL = 'https://faucet.devnet.aptoslabs.com' #'https://faucet.testnet.aptoslabs.com'
NODE_URL = 'https://fullnode.devnet.aptoslabs.com/v1' #'https://fullnode.testnet.aptoslabs.com/v1'


# mnemonic_alice = Mnemonic('english').generate()
# mnemonic_bob = Mnemonic('english').generate()

# print(f'mnemonic_alice is: {mnemonic_alice}')
# print(f'mnemonic_bob is: {mnemonic_bob}')

# pt_alice = PublicKeyUtils(mnemonic_alice)
# pt_bob = PublicKeyUtils(mnemonic_bob)


# alice = Account.load_key(pt_alice.private_key.hex())
# bob = Account.load_key(pt_bob.private_key.hex())



# print("\n=== Addresses ===")
# print(f"Alice addresss: {alice.address()}")
# print(f"Alice public_key: {alice.public_key()}")
# print(f"Alice private_key: 0x{pt_alice.private_key.hex()}")

# print(f"Bob addresss: {bob.address()}")
# print(f"Bob public_key: {bob.public_key()}")
# print(f"Bob private_key: 0x{bob.private_key.hex()}")

# rest_client = RestClient(NODE_URL)
# faucet_client = FaucetClient(FAUCET_URL, rest_client)  # <:!:section_1


# #:!:>section_3
# faucet_client.fund_account(alice.address(), 1_000_000_0)
# faucet_client.fund_account(bob.address(), 0)  # <:!:section_3

# print("\n=== Initial Balances ===")
# #:!:>section_4
# print(f"Alice: {rest_client.account_balance(alice.address())}")
# print(f"Bob: {rest_client.account_balance(bob.address())}")  # <:!:section_4

# # Have Alice give Bob 1_000 coins
# #:!:>section_5
# txn_hash = rest_client.transfer(alice, bob.address(), 1_000_000_0)  # <:!:section_5
# #:!:>section_6
# rest_client.wait_for_transaction(txn_hash)  # <:!:section_6

# print("\n=== Intermediate Balances ===")
# print(f"Alice: {rest_client.account_balance(alice.address())}")
# print(f"Bob: {rest_client.account_balance(bob.address())}")

# # Have Alice give Bob another 1_000 coins using BCS
# txn_hash = rest_client.bcs_transfer(alice, bob.address(), 1_000_000_0)
# rest_client.wait_for_transaction(txn_hash)

# print("\n=== Final Balances ===")
# print(f"Alice: {rest_client.account_balance(alice.address())}")
# print(f"Bob: {rest_client.account_balance(bob.address())}")

# rest_client.close()


# Define the root directory for storing account information
ACCOUNTS_DIR = "aptos_accounts"

# Define YAML config file template - this is just a text template
CONFIG_TEMPLATE = """---
profiles:
  default:
    network: Testnet
    private_key: "0x{PRIVATE_KEY}"
    public_key: "0x{PUBLIC_KEY}"
    account: {ACCOUNT}
    rest_url: "https://fullnode.testnet.aptoslabs.com"
    faucet_url: "https://faucet.testnet.aptoslabs.com"
"""

# Create root directory
os.makedirs(ACCOUNTS_DIR, exist_ok=True)

# Generate mnemonic words
words = Mnemonic('english').generate()
print(words)

# Save mnemonic to file
mnemonic_file = os.path.join(ACCOUNTS_DIR, 'aptos_mnemonic.txt')
with open(mnemonic_file, 'w') as f:
    f.write(words)

for address_index in range(10):
    # Derivation from BIP44 derivation path
    path = f"m/44'/637'/{address_index}'/0'/0'"
    pt = PublicKeyUtils(words, path)
    apt_account = Account.load_key(pt.private_key.hex())
    print(f"({address_index}) {path} {apt_account.address()} 0x{pt.private_key.hex()}")
    
    # Create account directory structure
    account_dir = os.path.join(ACCOUNTS_DIR, str(apt_account.address()))
    aptos_config_dir = os.path.join(account_dir, '.aptos')
    config_file = os.path.join(aptos_config_dir, 'config.yaml')
    
    # Skip if config file already exists
    if os.path.exists(config_file):
        continue
        
    # Create necessary directories
    os.makedirs(aptos_config_dir, exist_ok=True)
    
    # Prepare config file content
    config_content = CONFIG_TEMPLATE.format(
        PRIVATE_KEY=pt.private_key.hex(),
        PUBLIC_KEY=str(apt_account.public_key()).replace('0x', ''),
        ACCOUNT=str(apt_account.address()).replace('0x', '')
    )
    
    # Write config file
    with open(config_file, 'w') as f:
        f.write(config_content)
    
