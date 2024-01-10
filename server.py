import hashlib 
import json
from blockchain import Blockchain

from time import time
from textwrap import dedent
from uuid import uuid4
from flask import Flask, jsonify, request


#Instance our Node
app = Flask(__name__)

#Generate a globally uniqe address for this node 
node_identifier = str(uuid4()).replace('_', "")

#Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    return "We'll mine a new Block"

@app.route('/transaction/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    
    #Chack that the required fields are in the Post'ed data.
    required = ['sender', 'recepient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    
    #Create a new transaction
    index = blockchain.new_transaction(values['sender'], values['recepient'], values['amount'])
    
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201
    
    

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
               