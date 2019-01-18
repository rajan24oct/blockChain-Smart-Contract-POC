import datetime
import json

from marshmallow import Schema, fields
from web3 import Web3

ETH_URL = "http://127.0.0.1:7545"
now = datetime.datetime.now()
w3 = Web3(Web3.HTTPProvider(ETH_URL))
datastore = json.load(open("build/data.json"))


class ShipmentSchema(Schema):
    waybill = fields.String(required=True)
    updated_at = fields.String(required=True)
    location = fields.String(required=True)
    status = fields.String(required=True)
    notes = fields.String(required=True)


def create_shipment(data):
    w3.eth.defaultAccount = w3.eth.accounts[1]

    abi = datastore["abi"]
    contract_address = datastore["contract_address"]

    # Create the contract instance with the newly-deployed address
    user = w3.eth.contract(
        address=contract_address, abi=abi,
    )

    result, error = ShipmentSchema().load(data)
    if error:
        return error

    tx_hash = user.functions.setShipment(
        result['waybill'], result['updated_at'], result['location'], result['status'], result['notes']
    )
    tx_hash = tx_hash.transact()
    # Wait for transaction to be mined...
    w3.eth.waitForTransactionReceipt(tx_hash)
    shipment_data = user.functions.getShipment().call()

    return shipment_data


x = create_shipment({
    "waybill": '99999999',
    "updated_at": str(now),
    "location": "location",
    "status": "OW",
    "notes": "Notes"
})
print(x)
# total_blocks = w3.eth.blockNumber
#
# # check your transactions, contracts
# trns = mm.getTransactions(0)
#
# print("Transaction done")
# print("Total Blocks:")
# print(total_blocks)
# print("==============================END====================================")
# print("trns")
# # print(trns)
# print("==============================END====================================")
