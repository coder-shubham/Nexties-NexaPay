# NexaPay: One Scan, Endless Chains

## Project Description
NexaPay is a DeFi application, powered by ZetaChain, offers users the ability to conduct seamless cross-chain transactions and swaps. It enables users to add wallets, view balances, and complete payments effortlessly using QR codes, blending the power of decentralized finance with the ease of traditional payment apps. With a focus on cross-chain compatibility, this application serves as a powerful tool for users to interact with multiple blockchain networks in a user-friendly environment.

## Unique Value Proposition (UVP)
Our application stands out by providing a fully integrated cross-chain experience, allowing users to manage multiple blockchain wallets and execute transactions effortlessly. Unlike other DeFi platforms, we enable payment via QR codes, bringing convenience and simplicity to the world of crypto payments, mimicking the ease of popular traditional finance apps. This makes decentralized finance accessible and intuitive for everyday users.

### Key Features:
- **Cross-Chain Transactions**: Seamlessly transact across various blockchain networks.
- **Token Swaps**: Efficiently swap tokens between different chains in real time.
- **Wallet Management**: Easily add and manage multiple blockchain wallets within the app.
- **Transaction History**: View previous transactions and track balances across chains.
- **QR Code Payments**: Pay and receive payments directly via QR codes for an intuitive, frictionless experience.

### Code Structure
1. my-cross-chain-app: It's Frontend related Code which is frontline of Application written in React.
2. my-cross-chain-backend/venv: It's Backend Code where all API's and ZetaChain interaction methods are written which is consumed by Frontend Application. It is written in Python.
3. zetachain: It contains code related to ZetaChain Contract. It is written on Solidity and implemented using HardHat.


### ZetaChain Contract:
**ContractAddress**:  0xa5ac0bD9CC81f776700cB4e5F93B4A0027c8e42F
**ContractLink**: https://athens.explorer.zetachain.com/address/0xa5ac0bD9CC81f776700cB4e5F93B4A0027c8e42F

## Setup Instructions

### Prerequisites
- Node.js
- npm
- Python 3.12
- React
- HardHat
- ZetaChain 

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/coder-shubham/Nexties-NexaPay
    ```
    
## Frontend Application

1. Navigate to the frontend code directory from project root:
    ```bash
    cd my-cross-chain-app
    ```
    
2. Install dependencies:
    ```bash
    npm install
    ```

## Backend Application
1. Navigate to the frontend code directory from project root:
    ```bash
    cd my-cross-chain-backend/venv
    ```
    
2. Start Python Virtual Env:
    ```bash
    source bin/activate
    ```
    
3. Install Python Dependencies:
    ```bash
    pip install Flask qrcode[pil] requests web3
    ```

### Running the App

1. Start the server from Python Virtual Env:
    ```bash
    python3 app.py
    ```
2. Server started on `http://localhost:5000`.

3. Start the client Application from react directory:
    ```bash
    npm start
    ```
4. Open your browser and navigate to `http://localhost:3000`.

