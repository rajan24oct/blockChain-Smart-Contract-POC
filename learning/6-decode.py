import json
from datetime import datetime
from solc import compile_files
from web3 import Web3

sols = ['1-shipment.sol']

compliled_contract = compile_files(sols)

abi = compliled_contract['1-shipment.sol:shipmentRecords']['abi']
bytecode = compliled_contract['1-shipment.sol:shipmentRecords']['bin']

# w3 = Web3(Web3.HTTPProvider('http://35.240.174.241:8545'))
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
contract = w3.eth.contract(abi=abi, bytecode=bytecode)

tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[1]})
tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

contract_address = tx_receipt['contractAddress']

with open('data.json', 'w') as outfile:
    data = {
        "abi": abi,
        "contract_address": contract_address
    }
    json.dump(data, outfile, indent=4, sort_keys=True)


w3.eth.defaultAccount = w3.eth.accounts[1]
user = w3.eth.contract(address=contract_address, abi=abi)


tx = user.functions.setShipment('99999999', str(datetime.now()), 'CBJ', 'TRANSIT', 'NOTES')
tx = tx.transact()
w3.eth.waitForTransactionReceipt(tx)
shipment_data = user.functions.getShipment().call()

data = []

for i in range(w3.eth.blockNumber+1):
    block = w3.eth.getBlock(i, full_transactions=True)
    # print("-----------{}---------------".format(i))

    for tx in block.transactions:
        tx_from = tx.get('from', '') if tx.get('from', '') else ''
        tx_to = tx.get('to', '') if tx.get('to', '') else ''

        if tx_from.lower() == contract_address.lower() or tx_to.lower() == contract_address.lower():
            ret = {
                'to': tx['to'],
                'from': tx['from'],
                'value': tx['value'],
                'gas': tx['gas'],
                'gas_price': tx['gasPrice'],
                'input': tx['input'],
                'hash': tx['hash'].hex(),
                'nonce': tx['nonce'],
                'block': tx['blockHash'].hex(),
                'block_number': tx['blockNumber'],
                'transaction_index': tx['transactionIndex'],
            }
            data.append(ret)

for row in data:
    x = user.functions.getShipment().call(block_identifier=row['block_number'])
    print(x)
