import json
from com.dl.utils.processor import BCProcessor, w3
from marshmallow import Schema, fields, ValidationError

def check_gender(data):
    valid_list = ["male", "female"]
    if data not in valid_list:
        raise ValidationError(
            'Invalid gender. Valid choices are'+ valid_list
        )


class UserSchema(Schema):
    name = fields.String(required=True)
    gender = fields.String(required=True, validate=check_gender)
    email = fields.String(required=True)


class Members:

    def __init__(self):
        self.file_path = "contracts/build/data.json"
        with open(self.file_path, 'r') as f:
            datastore = json.load(f)
        self.datastore = datastore


    def getTransactions(self, start_block, end_block=w3.eth.blockNumber):
        w3.eth.defaultAccount = w3.eth.accounts[1]
        transArr = []
        totalArr = []

        for idx in range(start_block, end_block):
            print('Fetching block %d, remaining: %d, progress: %d%%' % (
                idx, (end_block - idx), 100 * (idx - start_block) / (end_block - start_block)))

            block = w3.eth.getBlock(idx, full_transactions=True)

            for tx in block.transactions:
                if tx['to']:
                    to_matches = tx['to'].lower() == self.datastore["contract_address"].lower()
                else:
                    to_matches = False

                if tx['from']:
                    from_matches = tx['from'].lower() == self.datastore["contract_address"].lower()
                else:
                    from_matches = False

                tmpArr = {}
                tmpArr['to'] = tx['to']
                tmpArr['from'] = tx['from']
                tmpArr['value'] = tx['value']
                tmpArr['gas'] = tx['gas']
                tmpArr['gas_price'] = tx['gasPrice']
                tmpArr['input'] = tx['input']

                tmpArr['hash'] = str(tx['hash'].hex())
                tmpArr['nonce'] = tx['nonce']
                tmpArr['block'] = str(tx['blockHash'].hex())
                tmpArr['block_number'] = tx['blockNumber']
                tmpArr['transaction_index'] = tx['transactionIndex']

                totalArr.append(tmpArr)

                if to_matches or from_matches:
                    transArr.append(tmpArr)
                    #print('Found transaction with hash %s' % tx['hash'].hex())

        retval = {}
        retval['totalArr'] = totalArr
        retval['transArr'] = transArr

        return retval




    def createMember(self, jsonData):
        w3.eth.defaultAccount = w3.eth.accounts[1]

        abi = self.datastore["abi"]
        contract_address = self.datastore["contract_address"]

        # Create the contract instance with the newly-deployed address
        user = w3.eth.contract(
            address=contract_address, abi=abi,
        )

        result, error = UserSchema().load(jsonData)
        if error:
            return error


        tx_hash = user.functions.setUser(
            result['name'], result['gender'], result['email']
        )
        tx_hash = tx_hash.transact()
        # Wait for transaction to be mined...
        w3.eth.waitForTransactionReceipt(tx_hash)
        user_data = user.functions.getUser().call()

        return user_data



