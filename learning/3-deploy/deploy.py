import json

from solc import compile_files, link_code
from web3 import Web3

ETH_URL = 'http://127.0.0.1:7545'


def separate_main_n_link(sols, contracts):
    # separate out main file and link files
    # assuming first file is main file.
    main = {}
    link = {}

    all_keys = list(contracts.keys())
    for key in all_keys:
        if sols[0] in key:
            main = contracts[key]
        else:
            link[key] = contracts[key]
    return main, link


def deploy_contract(contract_interface):
    # Instantiate and deploy contract
    contract = w3.eth.contract(
        abi=contract_interface['abi'], bytecode=contract_interface['bin'])

    # Get transaction hash from deployed contract
    tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[1]})

    # Get tx receipt to get contract address
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

    return tx_receipt['contractAddress']


w3 = Web3(Web3.HTTPProvider(ETH_URL))
sols = ['sols/shipment.sol', 'sols/stringUtils.sol']

contracts = compile_files(sols)

contract_interface, links = separate_main_n_link(sols, contracts)

link_add = {}
for link in links:
    link_add[link] = deploy_contract(links[link])

if link_add:
    contract_interface['bin'] = link_code(contract_interface['bin'], link_add)

contract_address, abi = deploy_contract(contract_interface), contract_interface['abi']

with open('build/data.json', 'w') as outfile:
    data = {
        "abi": abi,
        "contract_address": contract_address
    }
    json.dump(data, outfile, indent=4, sort_keys=True)

print("Informationn saved at build/data.json:")
print("MAIN contract_address:")
print(contract_address)
print("==============================END====================================")
print("abi")
print(abi)
print("==============================END====================================")
