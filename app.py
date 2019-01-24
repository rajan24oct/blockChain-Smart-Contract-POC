import datetime

from flask import Flask, request, jsonify, flash
from flask import render_template

from com.dl.utils.connector import Shipments, w3
from com.dl.utils.nocache import nocache
from forms.form import ShipmentForm

now = datetime.datetime.now()

SECRET_KEY = 'development'

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
@app.route("/add", methods=['GET', 'POST'])
@nocache
def main():
    mm = Shipments()
    # form to add new members
    form = ShipmentForm()

    if request.method == 'POST':
        waybill = request.form['waybill']
        location = request.form['location']
        status = request.form['status']
        notes = request.form['notes']

        if form.validate():
            mm.createShipment(
                {"waybill": waybill, "updated_at": str(now), "location": location, "status": status, "notes": notes})
        else:
            flash('All the form fields are required. ')

    # check total etherium blocks

    total_blocks = w3.eth.blockNumber

    # check your transactions, contracts
    trns = mm.getTransactions(0)

    return render_template("base.html", total_blocks=total_blocks, trns=trns['transArr'], alltrns=trns['totalArr'],
                           form=form)


@app.route("/bc/shipment", methods=['GET', 'POST'])
def transaction():
    body = request.get_json()

    mm = Shipments()
    user_data = mm.createShipment(body)
    return jsonify({"data": user_data}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
