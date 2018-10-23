from flask import Flask
import json
from com.dl.utils.processor import w3
from flask import Flask, Response, request, jsonify
from marshmallow import Schema, fields, ValidationError


app = Flask(__name__)


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


@app.route('/')
def hello_world():
    return '<h1> Welcome to DigitalLab Blockchain Demo'


@app.route("/bc/member", methods=['GET', 'POST'])
def transaction():
    w3.eth.defaultAccount = w3.eth.accounts[1]
    with open("contracts/build/data.json", 'r') as f:
        datastore = json.load(f)
    abi = datastore["abi"]
    contract_address = datastore["contract_address"]

    # Create the contract instance with the newly-deployed address
    user = w3.eth.contract(
        address=contract_address, abi=abi,
    )
    body = request.get_json()
    print(body)
    result, error = UserSchema().load(body)
    if error:
        return jsonify(error), 422
    tx_hash = user.functions.setUser(
        result['name'], result['gender'], result['email']
    )
    tx_hash = tx_hash.transact()
    # Wait for transaction to be mined...
    w3.eth.waitForTransactionReceipt(tx_hash)
    user_data = user.functions.getUser().call()
    return jsonify({"data": user_data}), 200



if __name__ == '__main__':
    app.run()
