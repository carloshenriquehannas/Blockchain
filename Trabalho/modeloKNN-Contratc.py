from web3 import Web3
import joblib

# URL do Ganache (endereço RPC do Ganache)
ganache_url = 'http://127.0.0.1:7545'  # RPC URL do Ganache
w3 = Web3(Web3.HTTPProvider(ganache_url))

# Verificar conexão
if w3.isConnected():
    print("Conectado ao Ganache!")

# Definir o endereço do contrato e ABI
contract_address = '0x22B46AB6FbfF6E5A249ff3a13514826d523A18eA'  # Endereço do contrato
contract_abi = [
    {
        "constant": False,
        "inputs": [{"name": "_predictedPrice", "type": "uint256"}],
        "name": "storePrediction",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Carregar o contrato
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Carregar o modelo KNN
knn = joblib.load('knn_model.pkl')

# Fazer uma previsão
predicted_price = knn.predict([[10000]])  

# Preparar a transação para armazenar a previsão no contrato
tx = contract.functions.storePrediction(predicted_price[0]).buildTransaction({
    'from': w3.eth.accounts[0],  # Endereço da conta
    'gas': 2000000,
    'gasPrice': w3.toWei('20', 'gwei'),
})

# Assinar e enviar a transação
private_key = '0x4c0883a69102937d6231471b5dbb620b62a3d319c8b132e7d7ec0535c8a5632b'  # Chave privada
signed_tx = w3.eth.account.signTransaction(tx, private_key)
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

# Confirmar transação
print(f'Transação enviada com sucesso: {tx_hash.hex()}')
