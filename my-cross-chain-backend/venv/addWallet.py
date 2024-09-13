from web3 import Web3
import re

# Initialize web3 instance (dummy RPC URL, replace with actual if needed)
web3 = Web3(Web3.HTTPProvider("https://zetachain-athens-evm.blockpi.network/v1/rpc/public"))

# Function to validate Ethereum address
def validate_address(address):
    return web3.is_address(address)

# Function to validate Ethereum private key
def validate_private_key(private_key):
    # Check if it's a 64-character hex string (no "0x" prefix)
    if re.match(r'^[0-9a-fA-F]{64}$', private_key):
        try:
            # Derive the public address from the private key
            account = web3.eth.account.from_key(private_key)
            return True, account.address  # Return True and the derived address
        except ValueError:
            return False, None  # Invalid private key
    else:
        return False, None

# Test with valid inputs

