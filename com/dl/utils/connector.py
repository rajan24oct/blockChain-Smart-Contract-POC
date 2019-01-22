import json
from com.dl.utils.processor import BCProcessor, w3
from marshmallow import Schema, fields, ValidationError


class ShipmentSchema(Schema):
    waybill = fields.String(required=True)
    updated_at = fields.String(required=True)
    location = fields.String(required=True)
    status = fields.String(required=True)
    notes = fields.String(required=True)


class Shipments:

    def __init__(self):
        self.file_path = "build/data.json"
        with open(self.file_path, 'r') as f:
            datastore = json.load(f)
        self.datastore = datastore



    def getTransactions(self, start_block):
        w3.eth.defaultAccount = w3.eth.accounts[1]
        contract = w3.eth.contract(
            address=self.datastore["contract_address"], abi=self.datastore["abi"],
        )

        transArr = []
        totalArr = []
        end_block = w3.eth.blockNumber
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
                try:
                    data = contract.functions.getShipment().call(block_identifier=int(tx['blockNumber']))
                    tmpArr['decoded'] = data
                except:
                    tmpArr['decoded'] = "no data"

                totalArr.append(tmpArr)

                if to_matches or from_matches:
                    transArr.append(tmpArr)
                    #print('Found transaction with hash %s' % tx['hash'].hex())

        retval = {}
        retval['totalArr'] = totalArr
        retval['transArr'] = transArr

        return retval




    def createShipment(self, jsonData):
        w3.eth.defaultAccount = w3.eth.accounts[1]

        abi = self.datastore["abi"]
        contract_address = self.datastore["contract_address"]

        # Create the contract instance with the newly-deployed address
        user = w3.eth.contract(
            address=contract_address, abi=abi,
        )

        result, error = ShipmentSchema().load(jsonData)
        if error:
            return error


        tx_hash = user.functions.setShipment(
            result['waybill'], result['updated_at'], result['location'],  result['status'], result['notes']
        )
        tx_hash = tx_hash.transact()
        # Wait for transaction to be mined...
        w3.eth.waitForTransactionReceipt(tx_hash)
        shipment_data = user.functions.getShipment().call()

        return shipment_data



