# import flask dependencies
from flask import Flask, make_response, request, jsonify
import pandas as pd
import numpy as np
from datetime import datetime

# initialize the flask app
app = Flask(__name__)

# default route
@app.route('/')
def index():
  return "Hello World!"
# create a route for webhook
# @app.route('/webhook')
# def hello():
#     return 'Hello World!'

# function for responses
def results():
    # build a request object
    req = request.get_json(force=True)
    startDate = req['queryResult']['parameters']['date-period']['startDate']
    endDate = req['queryResult']['parameters']['date-period']['endDate']
    # fetch action from json
    action = req.get('queryResult').get('action')
    transactions = pd.read_csv('transactions.csv')
    transactions['Transaction Date'] = pd.to_datetime(transactions['Transaction Date'])

    mask = (transactions['Transaction Date'] > startDate) & (transactions['Transaction Date'] <= endDate)
    periodTransactions = transactions.loc[mask]

    spentAmount = np.mean(periodTransactions['Transaction Amount'])
    print(startDate)
    formattedStart = '{:%B %d, %Y}'.format(datetime.strptime(startDate.split("T")[0], '%Y-%m-%d'))

    formattedEnd = '{:%B %d, %Y}'.format(datetime.strptime(endDate.split("T")[0], '%Y-%m-%d'))
    response_string = 'You spent ' + str(spentAmount) + ' between ' + formattedStart + ' and ' + formattedEnd + "."

    print(periodTransactions)
    # return a fulfillment response
    return {'fulfillmentText': response_string}

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))

# run the app
if __name__ == '__main__':
   app.run()