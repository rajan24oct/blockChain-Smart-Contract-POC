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


print("SHIPMENT DATA")
print(shipment_data)
print("==============================END====================================")
