from flask import Flask, request, jsonify
import qrcode
import io
import base64
import addWallet as wallet
import showBalances as balanceCheck
import preTransaction as preTrans
import swap
from datetime import datetime


app = Flask(__name__)

# Sample in-memory data store
users = {
    "user1": {"name": "Alice", "evmAddress": "0x1234", "qrCode": None}
}

# transactions = [
#         {"dateTime": "2024-09-12T12:34:56Z", "status": "Success", "sentAmount": "1 ETH", "sentToken": "ETH", "destinationToken": "BTC", "recipientAddress": "0x5678", "txnHash":"0x68758585678ff66xx7768y8686868gfygfghg6fvDRR588"},
#         {"dateTime": "2024-09-12T13:45:67Z", "status": "Failed", "sentAmount": "0.5 BTC", "sentToken": "BTC", "destinationToken": "ETH", "recipientAddress": "0x9876", "txnHash":"0x68758585678ff66xx7768y8686868gfyghbhbfvDRR588"}
#     ]

transactions =[
    {"dateTime":"2024-09-12T14:14:56Z","destinationToken":"BNB","recipientAddress":"0xB09e387D683CDAe6Dca5B76Ed89B8F4b5Bb88D13","sentAmount":"0.031 ETH","sentToken":"ETH","status":"Success","txnHash":"0x762b922b74b75c3b243f605fe7429cd910f65e70c60f53f38c3568a05b480537"},
    {"dateTime":"2024-09-12T15:10:55Z","destinationToken":"ETH","recipientAddress":"0xB09e387D683CRAe6Dca5B76Ed89B8F4b5Bb99E44","sentAmount":"0.5 BTC","sentToken":"BTC","status":"Failed","txnHash":"0x762b922b74b75c3b243f605fe7429cd910f65e78030f53f38c3568a05b480537"},
    {"dateTime":"2024-09-13 03:51:42","destinationToken":"sETH Sepolia","recipientAddress":"0xB09e387D683CDAe6Dca5B76Ed89B8F4b5Bb88D13","sentAmount":"0.0001 BNB","sentToken":"BNB","status":"Success","txnHash":"0x4dc642a6c98f14b27630ff0bde115fcb93d1851cef3eb98f4b7c3a01332f908f"},
    {"dateTime":"2024-09-13 04:15:42","destinationToken":"BNB","recipientAddress":"0xB09e387D683CDAe6Dca5B76Ed89B8F4b5Bb88D13","sentAmount":"0.031 sETH Sepolia","sentToken":"sETH Sepolia","status":"Success","txnHash":"0xcf018cfd7f287f09a5ea0a8ba377964dbe3a1d135a071665f014e7fa0315336b"}
    ]

token_dict = {
    "zeta_testnet": "ZETA",
    "bsc_testnet": "BNB",
    "sepolia_testnet":"sETH Sepolia"
}

@app.route('/api/show-profile', methods=['GET'])
def show_profile():
    user_info = users.get('user1', {})
    qr = qrcode.make(user_info.get('evmAddress', ''))
    qr_img = io.BytesIO()
    qr.save(qr_img, format='PNG')
    qr_img.seek(0)
    qr_base64 = base64.b64encode(qr_img.getvalue()).decode('utf-8')
    user_info['qrCode'] = f"data:image/png;base64,{qr_base64}"
    return jsonify(user_info)

@app.route('/api/add-wallet', methods=['POST'])
def add_wallet():
    data = request.json
    evm_address = data.get('evmAddress')
    private_key = data.get('privateKey')
    # Here you would typically validate and save the wallet details
    if not private_key or not evm_address:
        return jsonify({"error": "Missing private_key or evmAddress"}), 400
    
    if evm_address not in users:
        is_valid_address = wallet.validate_address(evm_address)
        is_valid_key, derived_address = wallet.validate_private_key(private_key)
        if not is_valid_address or not is_valid_key:
            return jsonify({"error": "Wallet details incorrect"}), 400
        users[evm_address] = {"name": data.get("name", "Unknown"), "evmAddress": evm_address, "qrCode": None, "privateKey": private_key}
        users['user1'] = {"name": data.get("name", "Unknown"), "evmAddress": evm_address, "qrCode": None, "privateKey": private_key}
    else:
        return jsonify({"error": "Wallet already added"}), 400
    
    return jsonify({"success": True, "message": "Wallet added successfully."})

@app.route('/api/show-balances', methods=['GET'])
def show_balances():
    # Example response
    balances = [
        {"network":"network1","amount": "10 ETH"},
        {"network":"network2","amount": "5 BTC"}
    ]
    if users['user1']['name'] == 'Alice':
        return jsonify({"balances": []})

    balances = balanceCheck.get_balance_multipleChain(users["user1"]["evmAddress"])
    return jsonify({"balances": balances})

@app.route('/api/get-destination-tokens', methods=['GET'])
def get_destination_tokens():
    recipient_address = request.args.get('recipientAddress')

    if not recipient_address:
        return jsonify({"error": "Recipient address is required"}), 400

    # Fetch balance data based on the recipient address
    # In a real application, you would query a database or another data source
    balances = balanceCheck.get_balance_multipleChain(recipient_address)
    return jsonify({"balances": balances})


@app.route('/api/get-trans-eqv-fee', methods=['POST'])
def get_trans_eqv_fee():
    data = request.json
    destTokenNetwork = data.get('selectedChain')
    sourceTokenNetwork = data.get('selectedToken')
    amount = data.get('amount')

    if not amount or not sourceTokenNetwork or not destTokenNetwork:
        print("Not all info")
        return jsonify({"error": "Amount,SourceTokenNetwork and DestTokenNetwork is required"}), 400

    # Fetch balance data based on the recipient address
    # In a real application, you would query a database or another data source
    trans_fee = preTrans.get_trans_fee(sourceTokenNetwork, destTokenNetwork)
    print("TransFee: " + str(trans_fee))

    if trans_fee is None:
         print("TransFee is None")
         return jsonify({"error": "Trans Fee cannot be calculated"}), 400
    
    if(amount < trans_fee):
        print("Amount is less than transFee")
        return jsonify({"error": "Amount is less than transFee"}), 400

    eqv_fee = preTrans.get_equivalent_dest_token(str(amount), str(trans_fee), sourceTokenNetwork, destTokenNetwork)

    fee = {}
    fee["transFee"] = trans_fee
    fee["eqvFee"] = eqv_fee

    return jsonify({"fees": fee})

@app.route('/api/show-transactions', methods=['GET'])
def show_transactions():
    # Example transactions
    return jsonify({"transactions": transactions})

@app.route('/api/pay', methods=['POST'])
def pay():
    data = request.json
    recipient_address = data.get('recipientAddress')
    selected_chain = data.get('selectedChain')
    selected_token = data.get('selectedToken')
    amount = data.get('amount')

    if users['user1']['name'] == 'Alice':
        return jsonify({"error": "User wallet is not added properly"}), 400
    

    senderAddr = users["user1"]["evmAddress"]
    senderKey = users["user1"]["privateKey"]

    transaction = {}
    now = datetime.now()

    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
    transaction["dateTime"] = formatted_now
    transaction["sentAmount"] = amount + " " + token_dict[selected_token]
    transaction["sentToken"] = token_dict[selected_token]
    transaction["destinationToken"] = token_dict[selected_chain]
    transaction["recipientAddress"] = recipient_address
    transaction["status"] = "Failed"

    try:
        txnHash = swap.swap_token(amount,senderAddr,senderKey,recipient_address,selected_token,selected_chain)
        if(txnHash is None):
            raise Exception("Gas fee is more than given amount")
        transaction["status"] = "Success"
        transaction["txnHash"] = txnHash
        transactions.append(transaction)
        return jsonify({"success": True, "transactionHash": txnHash})
    except Exception as e:
        print('Got exception as: ' + e)
        transactions.append(transaction)
        return jsonify({"errorReason ": e}), 400
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)
