import React, { useState } from 'react';
import './output.css';


const AddWallet = () => {
  const [evmAddress, setEvmAddress] = useState('');
  const [privateKey, setPrivateKey] = useState('');

  const saveWallet = () => {
    fetch('/api/add-wallet', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ evmAddress, privateKey }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert('Wallet added successfully!');
        } else {
          alert('Error: ' + data.error);
        }
      })
      .catch((err) => console.error(err));
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <div className="bg-white shadow-lg rounded-lg p-8 max-w-md w-full">
        <h2 className="text-2xl font-semibold text-center text-indigo-600 mb-6">Add Wallet</h2>
        
        <div className="mb-4">
          <input
            type="text"
            placeholder="EVM Address"
            value={evmAddress}
            onChange={(e) => setEvmAddress(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
        
        <div className="mb-6">
          <input
            type="text"
            placeholder="Private Key"
            value={privateKey}
            onChange={(e) => setPrivateKey(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <button
          onClick={saveWallet}
          className="w-full bg-indigo-500 text-white py-3 px-4 rounded-lg shadow hover:bg-indigo-600 transition duration-300 focus:outline-none focus:ring-2 focus:ring-indigo-400"
        >
          Save Wallet
        </button>
      </div>
    </div>
  );
};

export default AddWallet;
