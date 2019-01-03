exec(open("./Blockchain.py").read())

def load_all():
    try:
        blockchain.load_chain()
        blockchain.load_pending_tx()
        blockchain.load_nodes()
    except:
        print("Could not load chain from file")
    finally:
        pass
def save_all():
    try:
        blockchain.save_chain()
        blockchain.save_pending_tx()
        blockchain.save_nodes()
    except:
        print("Could not save chain to file")
    finally:
        pass

load_all()
app = Flask(__name__)

@app.route('/chain', methods=['GET'])
def full_chain():
    load_all()
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400
 
    for node in nodes:
        blockchain.register_node(node)
 
    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201
 
@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    print(blockchain.nodes)
    replaced = blockchain.resolve_conflicts()
 
    if replaced:
        save_all()
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

 
    return jsonify(response), 200

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
