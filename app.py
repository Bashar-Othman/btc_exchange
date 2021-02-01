
import os
from flask import Flask, request, flash, url_for, redirect, render_template,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from alpha_vantage.foreignexchange import ForeignExchange


DBUSER = 'postgres'
DBPASS = 'myPassword'
DBHOST = 'localhost'
DBPORT = '5432'
DBNAME = 'btc_exg'

API_KEY=os.environ['APP_KEY']

btc_records_seq = Sequence('btc_records_seq')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)


class tc_exchange_rate(db.Model ):
    id = db.Column('id', db.Integer,btc_records_seq, server_default=btc_records_seq.next_value(),primary_key=True)
    from_cc = db.Column(db.String(100))
    from_c_name = db.Column(db.String(50))
    to_cc = db.Column(db.String(200))
    to_c_name = db.Column(db.String(10))
    exchange_rate = db.Column(db.String(10))
    last_refreshed = db.Column(db.String(10))
    time_zone = db.Column(db.String(10))
    bid_price = db.Column(db.String(10))
    ask_price = db.Column(db.String(10))

    def __init__(self, from_cc, from_c_name, to_cc, to_c_name,exchange_rate,last_refreshed,time_zone,bid_price,ask_price,id):
        self.from_cc = from_cc
        self.from_c_name = from_c_name
        self.to_cc = to_cc
        self.to_c_name = to_c_name
        self.exchange_rate = exchange_rate
        self.last_refreshed = last_refreshed
        self.time_zone = time_zone
        self.bid_price = bid_price
        self.ask_price = ask_price
        # self.id=id

    def as_dict(self):
        return {"from_cc":self.from_cc,"from_c_name":self.from_c_name,"to_cc":self.to_cc,"to_c_name":self.to_c_name,
                "exchange_rate":self.exchange_rate,"last_refreshed":self.last_refreshed,"time_zone":self.time_zone,
                "bid_price":self.bid_price,"ask_price":self.ask_price}




def read_btc_exchange_rate():
        cc = ForeignExchange(key='GF42H1N71LWVF2MS')
        data, _ = cc.get_currency_exchange_rate(from_currency='BTC',to_currency='USD')
        return data


def update_records():
    print("*********************************************", btc_records_seq.next_value)
    data=read_btc_exchange_rate()
    btc_exc=tc_exchange_rate(data['1. From_Currency Code'],
                             data['2. From_Currency Name'],
                             data['3. To_Currency Code'],
                             data['4. To_Currency Name'],
                             data['5. Exchange Rate'],
                             data['6. Last Refreshed'],
                             data['7. Time Zone'],
                             data['8. Bid Price'],
                             data['9. Ask Price'],
                             btc_records_seq.next_value())
    print("Object : ",btc_exc)
    db.session.add(btc_exc)
    db.session.commit()

@app.route('/test')
def test():
    return "TEst is working ";


@app.route('/api/v1/quotes', methods=['GET', 'POST'])
def new():

    if request.method == 'POST':
        data = read_btc_exchange_rate()
        return data

    elif request.method == 'GET' :
        print( tc_exchange_rate.query.all())
        return jsonify(json_list=tc_exchange_rate.query.order_by("last_refreshed").first().as_dict())



if __name__ == '__main__':

    #app.run(debug=True, host='0.0.0.0')
    update_records()
    db.create_all()
    app.run(debug=True)
