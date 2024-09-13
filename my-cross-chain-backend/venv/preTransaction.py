from web3 import Web3
import json
import utils as util

#https://zetachain-athens.blockpi.network/lcd/v1/public/zeta-chain/observer/supportedChains
#https://zetachain-athens.blockpi.network/lcd/v1/public/zeta-chain/fungible/foreign_coins
network_token = {
    "zeta_testnet": "0x5F0b1a82749cb4E2278EC87F8BF6B618dC71a8bf",
    "bsc_testnet": "0xd97B1de3619ed2c6BEb3860147E30cA8A7dC9891",
    "sepolia_testnet":"0x05BA149A7bd6dC1F937fA9046A9e05C05f3b18b0"
}

# Load ZRC20 ABI (Assuming ZRC20 ABI is in a JSON file)
with open('ZRC20.json') as f:
    ZRC20_ABI = json.load(f)

# Load UniswapV2Router02 ABI (Assuming ABI is in a JSON file)
with open('IUniswapV2Router02.json') as f:
    UNISWAP_V2_ROUTER_ABI = json.load(f)

# Set up the Web3 provider
def get_web3_provider():
    rpc_url = 'https://zetachain-athens.g.allthatnode.com/archive/evm'
    return Web3(Web3.HTTPProvider(rpc_url))

def get_zeta_token():
    return '0x5F0b1a82749cb4E2278EC87F8BF6B618dC71a8bf'

def get_uniswap_router(provider):
    uniswap_router_address = '0x2ca7d64A7EFE2D62A725E2B35Cf7230D6677FfEe'
    return provider.eth.contract(address=uniswap_router_address, abi=UNISWAP_V2_ROUTER_ABI)

# Get withdraw fee in input token
def get_withdraw_fee_in_input_token(input_zrc20, output_zrc20):
    provider = get_web3_provider()
    zeta_token = get_zeta_token()

    input_contract = provider.eth.contract(address=input_zrc20, abi=ZRC20_ABI)
    output_contract = provider.eth.contract(address=output_zrc20, abi=ZRC20_ABI)

    input_decimals = input_contract.functions.decimals().call()
    
    # Fetch withdraw gas fee from the output contract
    gas_zrc20, gas_fee = output_contract.functions.withdrawGasFee().call()

    print(gas_zrc20,gas_fee)
    
    withdraw_fee_in_zeta = get_amounts('in', provider, gas_fee, zeta_token, gas_zrc20)
    withdraw_fee_in_input_token = get_amounts('in', provider, withdraw_fee_in_zeta[0], input_zrc20, zeta_token)

    return {
        'amount': withdraw_fee_in_input_token[0],
        'decimals': input_decimals
    }

# Get quote for swapping input ZRC20 token to output ZRC20 token
def get_quote(input_amount, input_token, output_token):
    provider = get_web3_provider()
    zeta_token = get_zeta_token()

    input_contract = provider.eth.contract(address=input_token, abi=ZRC20_ABI)
    output_contract = provider.eth.contract(address=output_token, abi=ZRC20_ABI)

    input_decimals = input_contract.functions.decimals().call()
    print(input_decimals)
    amount_in = Web3.to_wei(input_amount, 'ether')

    output_decimals = output_contract.functions.decimals().call()

    if input_token == zeta_token or output_token == zeta_token:
        out = get_amounts('out', provider, amount_in, input_token, output_token)
    else:
        out_in_zeta = get_amounts('out', provider, amount_in, input_token, zeta_token)
        out = get_amounts('out', provider, out_in_zeta[1], zeta_token, output_token)

    return {
        'amount': out[1],
        'decimals': output_decimals
    }

# Get amounts for token swapping
def get_amounts(direction, provider, amount, token_a, token_b):
    uniswap_router = get_uniswap_router(provider)
    path = [token_a, token_b]

    if direction == 'in':
        amounts = uniswap_router.functions.getAmountsIn(amount, path).call()
    else:
        amounts = uniswap_router.functions.getAmountsOut(amount, path).call()

    return amounts

# print(get_withdraw_fee_in_input_token('0x05BA149A7bd6dC1F937fA9046A9e05C05f3b18b0','0xd97B1de3619ed2c6BEb3860147E30cA8A7dC9891'))


def get_trans_fee(input_network, dest_network):
    source_tok_addr = network_token[input_network]
    dest_tok_addr = network_token[dest_network]
    fee = get_withdraw_fee_in_input_token(source_tok_addr, dest_tok_addr)
    formatted_fee = util.format_fixed(fee['amount'], fee['decimals']) #HardCoded to 18 , will change later
    return formatted_fee


def get_equivalent_dest_token(amount, trans_fee, input_network, dest_network):
    source_tok_addr = network_token[input_network]
    dest_tok_addr = network_token[dest_network]
    formatted_amount = util.parse_fixed(amount, 18)
    formatted_fee = util.parse_fixed(trans_fee, 18)
    diff_amt = int(formatted_amount) - int(formatted_fee)
    formatted_diff_amt = util.format_fixed(diff_amt, 18)
    eqv_amt = get_quote(formatted_diff_amt, source_tok_addr, dest_tok_addr)
    formatted_eqv_amt = util.format_fixed(eqv_amt['amount'], eqv_amt['decimals'])
    return formatted_eqv_amt