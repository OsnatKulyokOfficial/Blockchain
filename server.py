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
    # `blockchain.last_block`: Retrieves the last block in the blockchain.
    last_block = blockchain.last_block

    # `last_block['proof']`: Accesses the 'proof' value from the last block.
    last_proof = last_block['proof']

    # `blockchain.proof_of_work()`: Computes the proof of work for the new block.
    proof = blockchain.proof_of_work(last_proof)
    
    # `blockchain.new_transaction()`: Records a new transaction on the blockchain. 
    # In this case, it's used to award a mining reward to the node that mined the new block.
    blockchain.new_transaction(
        sender = "0",
        recipient = node_identifier,
        amount = 1,
    )
    
    # `blockchain.hash()`: Generates a hash of the last block, which will be used in the new block's creation.
    previous_hash = blockchain.hash(last_block)

    # `blockchain.new_block()`: Adds a new block to the blockchain using the provided proof and the previous hash.
    block = blockchain.new_block(proof, previous_hash)
    
    # Preparing the response object with details of the new block.
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    
    # `jsonify()`: Converts the Python dictionary to a JSON response.   
    return jsonify(response), 200






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
    # `blockchain.chain`: Accesses the entire blockchain, which is a list of blocks.
    response = {
        'chain': blockchain.chain,

        # `len(blockchain.chain)`: Calculates the total number of blocks in the blockchain.
        'length': len(blockchain.chain),
    }

    return jsonify(response), 200

# The following code block only runs if this script is executed as the main program.
if __name__ == '__main__':
    # `app.run()`: Starts the Flask web server.
    # `host='0.0.0.0'`: The server is accessible externally. '0.0.0.0' makes the server accessible 
    # to any device on the network.
    # `port=5000`: Specifies the port number that the server listens to.
    app.run(host='0.0.0.0', port=5000)

               
               