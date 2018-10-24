from com.dl.utils.connector import Members, w3
from flask import Flask, Response, request, jsonify, flash
from marshmallow import Schema, fields, ValidationError
from flask import render_template
from com.dl.utils.nocache import nocache
from forms.form import MemberForm

SECRET_KEY = 'development'


app = Flask(__name__)
app.config.from_object(__name__)



@app.route('/')
@app.route("/add", methods=['GET', 'POST'])
@nocache
def main():
    mm = Members()
    # form to add new members
    form = MemberForm()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        gender = request.form['gender']

        if form.validate():
            user_data = mm.createMember({"name":name, "email":email, "gender":gender})
        else:
            flash('All the form fields are required. ')

    # check total etherium blocks

    total_blocks = w3.eth.blockNumber

    # check your transactions, contracts
    trns = mm.getTransactions(0)

    return render_template("base.html", total_blocks=total_blocks, trns=trns['transArr'], alltrns=trns['totalArr'],form=form)



@app.route("/bc/member", methods=['GET', 'POST'])
def transaction():
    body = request.get_json()
    mm = Members()
    user_data = mm.createMember(body)
    return jsonify({"data": user_data}), 200


if __name__ == '__main__':
    app.run()
