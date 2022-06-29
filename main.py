import datetime, json, hashlib
from flask import Flask, jsonify, request

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_blockchain(proof=1, previous_hash='0')


    def create_blockchain(self, proof, previous_hash):
        block = {
            'index' : len(self.chain) +1,
            'timestamp' : str(datetime.datetime.now()),
            'proof' : proof,
            'previous_hash' : previous_hash
        }   
        self.chain.append(block)
        return block


    def get_previous_block(self):
        last_block = self.chain[-1]
        return last_block

    #bloque de mineria
    def proof_of_work(self, previous_proof):
        # prueba de mineros enviadas
        new_proof = 1
        # estado de la prueba
        check_proof = False
        # algoritmo a resolver new_proof ** 2 - previous_proof ** 2
        #implementación
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            # resolución y validación de la prueba si da 4 ceros a la izquierda (la cantidad de 0 indica la dificultad de la prueba)
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1  
        return new_proof

    # creación del hash
    def hash(self, block):
        encode_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encode_block).hexdigest()
    
    #validación de la cadena
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            # bloque actual
            block = chain[block_index]
            # verifica que el bloque tenga el hash correcto
            if block["previous_hash"] != self.hash(previous_block):
                return False
            # obtiene la prueba de trabajo del bloque anterior
            previous_proof = previous_block['proof']
            # obtiene la prueba de trabajo actual
            current_proof = block['proof']
            # ejecuta la prueba de trabajo sobre el argoritmo
            hash_operation = hashlib.sha256(str(current_proof ** 2 - previous_proof **2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True


    def get_block_by_index(self, index):
        return blockchain.chain[index]


"""
Esto define la blockchain, pero para interacturar con ella hay que minarla, por lo tanto genrenamos la app
"""     

app = Flask(__name__)

blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    # objetenmos los datos necesarios para crear el bloque
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work((previous_proof))
    previous_hash = blockchain.hash(previous_block)
    # creamos el bloque
    block= blockchain.create_blockchain(proof, previous_hash)
    #respuesta en json
    response = {
        'message': 'Block mined!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    # retornamos la respuesta en jsonfy si el status es 200
    return jsonify(response), 200

@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    # retornamos la respuesta
    return jsonify(response), 200

@app.route('/is_chain_valid', methods=['GET'])
def is_chain_valid():
    response = {
        'chain_valid': blockchain.is_chain_valid(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/block_by_index', methods=['POST'])
def block_by_index():
    try:
        peticion = request.json
        index = peticion['index'] #type:ignore
        response = {
            f'block {index}': blockchain.get_block_by_index(index)
        }
        return jsonify(response), 200
    except:
        response={
            'error' : 'no existe ese indice'
        }
        return jsonify(response)

app.run(host='0.0.0.0', port=5000, debug=True)
