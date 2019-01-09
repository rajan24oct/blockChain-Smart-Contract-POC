import json
from com.dl.utils.processor import BCProcessor

# Specify All the Solidity files
solsArr = ['sols/shipment.sol', 'sols/stringUtils.sol']

# compile and Transact into ETH
bcp = BCProcessor(solsArr)
contract_address, abi = bcp.deploy_n_transact()

# save contract address and abi in JSON filecl
with open('build/data.json', 'w') as outfile:
    data = {
        "abi": abi,
        "contract_address": contract_address
    }
    json.dump(data, outfile, indent=4, sort_keys=True)
