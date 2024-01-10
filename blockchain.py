
from ast import While
import hashlib
import json

from time import time
from uuid import uuid4


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        
        #create a genesis(ראשוני) block
        self.new_block(previous_hash=1, proof=100)
        
        
    def new_block(self, proof, previous_hash):
        """
        create a new Blockchain
        
        :param proof: <int> The proof given by Proof of work algorithm.
        :param previous_hash: (optional) <str> Hash of the previous Block.
        
        :return: <dict> New Block.
        """
        
        block = {
            'index': len(self.chain) +1,
            'timestamp': time(),
            'transaction': self.current_transactions,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        
        #Reset the current list of transactions
        self.current_transactions = []
        
        self.chain.append(block)
        return block
        
    
    
    def new_transaction(self, sender, recipient, amount):

        """
        Create a new transaction to go into the next mined Block.
        
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount 
        :return: <int> The index of the Block that will hold this transaction
        
        """
        
        # Append a new transaction to the current list of transactions.
        # This transaction is represented as a dictionary with keys 'sender', 
        # 'recipient', and 'amount', corresponding to the function's parameters.
        self.current_transactions.append({
            'sender':sender,
            'recipient':recipient,
            'amount':amount,
        })
        
        #After new_transaction() adds a transaction to the list, it returns the index of the block which the transaction will be added to—the next one to be mined. This will be useful later on, to the user submitting the transaction.
        return self.last_block['index'] +1
   
    
    @staticmethod
    def hash(block):
        
        """"
        Create a SHA-256 hash of a Block
        
        :param block: <dict> Block
        :return: <str>
        """
        #we must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes.
        
        #dumps:  converts a Python object (in this case, a dictionary representing a block) into a JSON-formatted string.
        
        #sort_keys:  ensures that the dictionary keys are sorted alphabetically, which is essential for generating consistent hashes regardless of the order of keys in the original dictionary.
        
        #hexdigest: A method in Python's hashlib that converts a hash into a readable hexadecimal string format.
        block_string = json.dumps(block, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()
    
    @property
    def last_block(self):
        #Returns the last block in the chain
        return self.chain[-1]



    def proof_of_work(self, last_proof):
        """
        Simple proof of work algorithm:
        
        -Find a number p' such that hash(pp') contains leading 4 zeros, where p is the previous p'.
        -p is the previous proof, and p' is the new proof. 
        
        :param last_proof: <int> 
        :return: <int> 
        
        """
        
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        
        return proof
    
    @staticmethod
    def valid_proof(last_proof, proof):
        """"
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeros?
        :param last_proof: <int> Previous Proof.
        :param proof: <int> Current Proof.
        
        :return: <bool> True if correct, False if not
        """
        
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        
        return guess_hash[:4] == "0000"