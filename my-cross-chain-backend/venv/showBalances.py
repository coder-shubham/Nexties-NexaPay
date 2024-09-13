from web3 import Web3

# Define RPC endpoints for each chain
rpc_endpoints = {
    "zeta_testnet": "https://zetachain-athens-evm.blockpi.network/v1/rpc/public",
    "bsc_testnet": "https://bsc-testnet.blockpi.network/v1/rpc/public",
    "sepolia_testnet":"https://ethereum-sepolia.blockpi.network/v1/rpc/public"
    # Add other chains and their RPC URLs as needed
}

# Function to get balance for a specific address
def get_balance(address, chain_name, rpc_url):
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if web3.is_connected():
        # Get balance in Wei (smallest unit of Ether)
        balance_wei = web3.eth.get_balance(address)
        # Convert Wei to Ether (or other native token depending on the chain)
        balance_eth = web3.from_wei(balance_wei, 'ether')
        return balance_eth
    else:
        return None

def get_balance_multipleChain(address):
    balances = [{}]
    for chain, rpc_url in rpc_endpoints.items():
        balance = get_balance(address, chain, rpc_url)
        balance_dict = {}
        balance_dict["network"]=chain
        balance_dict["amount"]=balance
        balances.append(balance_dict)
        if balance is not None:
            print(f"{chain} balance: {balance} ETH")
        else:
            print(f"Could not connect to {chain} RPC")
    return balances