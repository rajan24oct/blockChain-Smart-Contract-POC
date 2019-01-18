import datetime
import json
import pprint

from web3 import Web3

ETH_URL = "http://127.0.0.1:7545"
now = datetime.datetime.now()
w3 = Web3(Web3.HTTPProvider(ETH_URL))
datastore = json.load(open("build/data.json"))


def get_transactions(start_block, end_block=w3.eth.blockNumber):
    w3.eth.defaultAccount = w3.eth.accounts[1]

    ret = []

    for idx in range(start_block, end_block):
        # print('Fetching block %d, remaining: %d, progress: %d%%' % (
        #     idx, (end_block - idx), 100 * (idx - start_block) / (end_block - start_block)))

        block = w3.eth.getBlock(idx, full_transactions=True)

        for tx in block.transactions:
            if tx['from'].lower() == datastore["contract_address"].lower() or tx['to'].lower() == datastore["contract_address"].lower():
                data = {
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
                ret.append(data)
    return ret


x = get_transactions(0)

pprint.pprint(x)
print("===============================================================================================================")
print("=================================================END===========================================================")
print("===============================================================================================================")
print("Total transaction for this block: {}".format(len(x)))
