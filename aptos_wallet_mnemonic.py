#!/usr/bin/env python3
import sys
import os
import argparse
from mnemonic import Mnemonic
from utils import PublicKeyUtils
from aptos_sdk.account import Account

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Aptos Wallet Mnemonic Generator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Required arguments
    parser.add_argument(
        '--dir', '-d', 
        dest='accounts_dir', 
        required=True,
        help='Root directory for storing account information (supports absolute or relative paths)'
    )
    
    # Network selection (required)
    parser.add_argument(
        '--network', '-n', 
        choices=['devnet', 'testnet', 'mainnet', 'local', 'custom'],
        required=True,
        help='Network type [devnet, testnet, mainnet, local, custom]'
    )
    
    # Optional arguments
    parser.add_argument(
        '--node-url', 
        default='',  # Changed to empty default to use network-specific URL
        help='Override default Node URL for the selected network'
    )
    
    parser.add_argument(
        '--faucet-url', 
        default='',
        help='Override default Faucet URL for the selected network'
    )
    
    parser.add_argument(
        '--count', '-c',
        type=int,
        default=10,
        help='Number of wallets to generate'
    )
    
    parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='Force overwrite existing mnemonic file'
    )
    
    # Parameters for configuration files and directories
    parser.add_argument(
        '--config-dir',
        default='.aptos',
        help='Name of the configuration directory (default: .aptos)'
    )
    
    parser.add_argument(
        '--config-file',
        default='config.yaml',
        help='Name of the configuration file (default: config.yaml)'
    )
    
    # New parameter for mnemonic file name
    parser.add_argument(
        '--mnemonic-file',
        default='aptos_mnemonic.txt',
        help='Name of the mnemonic file (default: aptos_mnemonic.txt)'
    )
    
    return parser.parse_args()

def get_network_urls(network):
    """Return default URL configuration based on network type"""
    urls = {
        'devnet': {
            'rest': 'https://fullnode.devnet.aptoslabs.com/v1',
            'faucet': 'https://faucet.devnet.aptoslabs.com'
        },
        'testnet': {
            'rest': 'https://fullnode.testnet.aptoslabs.com/v1',
            'faucet': 'https://faucet.testnet.aptoslabs.com'
        },
        'mainnet': {
            'rest': 'https://fullnode.mainnet.aptoslabs.com/v1',
            'faucet': ''
        },
        'local': {
            'rest': 'http://localhost:8080/v1',
            'faucet': 'http://localhost:8081'
        },
        'custom': {
            'rest': '',
            'faucet': ''
        }
    }
    return urls.get(network, urls['devnet'])

def main():
    """Main function"""
    args = parse_arguments()
    
    # Process account directory path (support absolute and relative paths)
    accounts_dir = os.path.abspath(args.accounts_dir)
    
    # Get network-related URLs
    network_urls = get_network_urls(args.network)
    
    # Use network-specific URLs if not overridden by command line
    node_url = args.node_url if args.node_url else network_urls['rest']
    faucet_url = args.faucet_url if args.faucet_url else network_urls['faucet']
    
    # Create config file template
    config_template = """---
profiles:
  default:
    network: {NETWORK}
    private_key: "{PRIVATE_KEY}"
    public_key: "{PUBLIC_KEY}"
    account: {ACCOUNT}
    rest_url: "{REST_URL}"
"""

    # Only add faucet_url to config if it exists
    if faucet_url:
        config_template += '    faucet_url: "{FAUCET_URL}"\n'
    
    # Create root directory
    os.makedirs(accounts_dir, exist_ok=True)
    
    # Check if mnemonic file already exists
    mnemonic_file = os.path.join(accounts_dir, args.mnemonic_file)
    if os.path.exists(mnemonic_file) and not args.force:
        print(f"Error: Mnemonic file '{mnemonic_file}' already exists. Use --force to overwrite or specify a different directory.")
        sys.exit(1)
    
    # Generate new mnemonic
    words = Mnemonic('english').generate()
    print(words)
    
    # Save mnemonic to file
    with open(mnemonic_file, 'w') as f:
        f.write(words)
    
    # Generate account information
    for address_index in range(args.count):
        # Use BIP44 derivation path
        path = f"m/44'/637'/{address_index}'/0'/0'"
        pt = PublicKeyUtils(words, path)
        apt_account = Account.load_key(pt.private_key.hex())
        
        # Ensure private key format is correct (includes 0x prefix)
        private_key = f"0x{pt.private_key.hex()}"
        
        # Get public key and ensure format is correct
        public_key = str(apt_account.public_key())
        if not public_key.startswith("0x"):
            public_key = f"0x{public_key}"
        
        # Get account address and ensure format is correct (remove 0x prefix)
        account_address = str(apt_account.address())
        account_address = account_address.replace("0x", "")
        
        print(f"({address_index}) {path} {apt_account.address()} {private_key}")
        
        # Create account directory structure
        account_dir = os.path.join(accounts_dir, str(apt_account.address()))
        aptos_config_dir = os.path.join(account_dir, args.config_dir)  # Use the config dir from args
        config_file = os.path.join(aptos_config_dir, args.config_file)  # Use the config file from args
        
        # Skip if config file already exists
        if os.path.exists(config_file):
            print(f"Note: Config file for account {apt_account.address()} already exists at '{config_file}', skipping this account.")
            continue
        
        # Create necessary directories
        os.makedirs(aptos_config_dir, exist_ok=True)
        
        # Prepare config file content
        config_content = config_template.format(
            NETWORK=args.network.capitalize(),
            PRIVATE_KEY=private_key,
            PUBLIC_KEY=public_key,
            ACCOUNT=account_address,
            REST_URL=node_url,
            FAUCET_URL=faucet_url
        )
        
        # Write config file
        with open(config_file, 'w') as f:
            f.write(config_content)
        
        print(f"Created config file: {config_file}")

if __name__ == "__main__":
    main()
    
