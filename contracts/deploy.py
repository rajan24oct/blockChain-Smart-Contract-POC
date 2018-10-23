import json
from com.dl.utils.processor import BCProcessor

bcp = BCProcessor(['dlMembers.sol', 'stringUtils.sol'])
contract_address, abi = bcp.deploy_n_transact()

with open('build/data.json', 'w') as outfile:
    data = {
        "abi": abi,
        "contract_address": contract_address
    }
    json.dump(data, outfile, indent=4, sort_keys=True)


