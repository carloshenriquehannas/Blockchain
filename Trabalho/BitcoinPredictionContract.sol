// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BitcoinPredictionContract {
    address public owner;                 // Endereço do administrador do contrato
    uint public predictionThreshold;      // Limite de preço para acionar a transação
    address payable public recipient;     // Destinatário para o qual a quantia será enviada se a condição for atendida

    uint public lastPrediction;           // Última previsão de preço armazenada

    // Evento para logar previsões e transações
    event PredictionStored(uint prediction);
    event ThresholdBreached(uint prediction, address recipient, uint amount);

    // Modificador para funções exclusivas do dono
    modifier onlyOwner() {
        require(msg.sender == owner, "Somente o administrador pode executar esta funcao");
        _;
    }

    constructor(uint _predictionThreshold, address payable _recipient) {
        owner = msg.sender;                     // Define o dono do contrato
        predictionThreshold = _predictionThreshold;
        recipient = _recipient;
    }

    // Função para atualizar o limite
    function updateThreshold(uint _newThreshold) public onlyOwner {
        predictionThreshold = _newThreshold;
    }

    // Função para atualizar o destinatário
    function updateRecipient(address payable _newRecipient) public onlyOwner {
        recipient = _newRecipient;
    }

    // Função para armazenar a previsão e checar o limite
    function storePrediction(uint _prediction) public payable {
        lastPrediction = _prediction;
        emit PredictionStored(_prediction);    // Loga a previsão armazenada

        // Verifica se a previsão excede o limite
        if (_prediction > predictionThreshold) {
            uint amount = address(this).balance;   // Define o valor a ser enviado (pode ser ajustado)
            require(amount > 0, "Sem saldo suficiente para transferir");

            recipient.transfer(amount);
            emit ThresholdBreached(_prediction, recipient, amount);
        }
    }

    // Função para o dono do contrato enviar fundos ao contrato para transferências
    function deposit() public payable onlyOwner {}

    // Função para o dono do contrato retirar fundos
    function withdraw(uint amount) public onlyOwner {
        require(address(this).balance >= amount, "Saldo insuficiente");
        payable(owner).transfer(amount);
    }
}
