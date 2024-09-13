from web3 import Web3
from decimal import Decimal
import json


rpc_endpoints = {
    "zeta_testnet": "https://zetachain-athens-evm.blockpi.network/v1/rpc/public",
    "bsc_testnet": "https://bsc-testnet.blockpi.network/v1/rpc/public",
    "sepolia_testnet":"https://ethereum-sepolia.blockpi.network/v1/rpc/public"
}

network_token = {
    "zeta_testnet": "0x5F0b1a82749cb4E2278EC87F8BF6B618dC71a8bf",
    "bsc_testnet": "0xd97B1de3619ed2c6BEb3860147E30cA8A7dC9891",
    "sepolia_testnet":"0x05BA149A7bd6dC1F937fA9046A9e05C05f3b18b0"
}


def prepare_params(web3, types, args):
    encoded_params = []
    
    # Iterate over args and types to handle specific types like bytes32
    for i in range(len(args)):
        if types[i] == "bytes32":
            # Handle bytes32 explicitly by padding the argument to 32 bytes
            padded_arg = web3.to_bytes(hexstr=args[i]).rjust(32, b'\x00')
            encoded_params.append(padded_arg)
        else:
            # Convert the argument to its corresponding ABI-encoded value
            encoded_params.append(web3.to_bytes(hexstr=args[i]))

    abi_encoded_params = web3.codec.encode(types, args)
    return abi_encoded_params

def prepare_data(web3, contract_address, types, args):
    # Prepare the params by encoding them
    encoded_params = prepare_params(web3, types, args)
    return contract_address + encoded_params.hex()

def parse_units(web3, amount, decimals):
    return web3.to_wei(amount, 'ether')
    

def swap_token(amount, senderAddress, senderKey, recipitentAddr, inputChain, destChain):
    rpc_url = rpc_endpoints[inputChain]
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if web3.is_connected():
        print('Connected to Network ' + inputChain)

    #Swap Token Address   
    contract_address = '0xa5ac0bD9CC81f776700cB4e5F93B4A0027c8e42F'
    types = ['address', 'bytes']
    args = [network_token[destChain], recipitentAddr]
    # Prepare the transaction data
    transaction_data = prepare_data(web3, contract_address, types, args)
    print(f"Prepared transaction data: {transaction_data}")
    private_key = senderKey
    value = parse_units(web3, amount, 18)
    to_address="0x8531a5aB847ff5B22D855633C25ED1DA3255247e"
    nonce = web3.eth.get_transaction_count(senderAddress)
    gas_limit = web3.eth.estimate_gas({
        'from': senderAddress,
        'to': to_address,
        'data': transaction_data,
        'value': value
    })
    gas_price = web3.eth.gas_price
    total_gas_fee = gas_limit * gas_price
    total_gas_fee_in_ether = web3.from_wei(total_gas_fee, 'ether')
    chainId = web3.eth.chain_id
    print(f"Estimated Gas: {gas_limit}")
    print(f"Gas Price: {gas_price} wei")
    print(f"Total Gas Fee: {total_gas_fee_in_ether} ETH")
    if(total_gas_fee_in_ether >= float(amount)):
        print("Gas fee is more than given amount")
        return None

    transaction = {
        'to': to_address,
        'value': value,
        'gas': gas_limit,
        'gasPrice': web3.eth.gas_price,  
        'nonce': nonce,
        'data': transaction_data,
        'chainId': chainId
    }

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print(f"Transaction hash: {web3.to_hex(txn_hash)}")
    return str(web3.to_hex(txn_hash))


