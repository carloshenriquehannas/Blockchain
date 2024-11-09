// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";
import "@chainlink/contracts/src/v0.8/ConfirmedOwner.sol";

contract BitcoinPredictionContract is ChainlinkClient, ConfirmedOwner {
    using Chainlink for Chainlink.Request;

    uint256 public predictionThreshold;
    address payable public recipient;
    address private oracle;
    bytes32 private jobId;
    uint256 private fee;
    uint256 public predictedPrice;

    // Construtor
    constructor(
        uint256 _predictionThreshold,
        address payable _recipient,
        address _oracle,
        bytes32 _jobId,
        uint256 _fee,
        address _link
    ) ConfirmedOwner(msg.sender) {
        _setChainlinkToken(_link);
        oracle = _oracle;
        jobId = _jobId;
        fee = _fee;
        predictionThreshold = _predictionThreshold;
        recipient = _recipient;
    }

    // Solicitação ao oráculo Chainlink para uma nova previsão
    function requestPrediction() public returns (bytes32 requestId) {
        Chainlink.Request memory request = _buildChainlinkRequest(jobId, address(this), this.fulfill.selector);
        return _sendChainlinkRequestTo(oracle, request, fee);
    }

    // Receber a previsão do oráculo
    function fulfill(bytes32 _requestId, uint256 _predictedPrice) public recordChainlinkFulfillment(_requestId) {
        predictedPrice = _predictedPrice;
        if (predictedPrice > predictionThreshold) {
            sendFunds();
        }
    }

    // Enviar fundos para o destinatário
    function sendFunds() internal {
        require(address(this).balance > 0, "Contrato sem saldo");
        recipient.transfer(address(this).balance);
    }

    // Função para o dono do contrato enviar fundos ao contrato para transferências
    function deposit() public payable onlyOwner {}

    // Função para o dono do contrato retirar fundos
    function withdraw(uint amount) public onlyOwner {
        require(address(this).balance >= amount, "Saldo insuficiente");
        payable(msg.sender).transfer(amount); // Usando msg.sender diretamente
    }
}
