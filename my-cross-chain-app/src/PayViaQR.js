import React, { useState, useEffect } from 'react';
import { QrReader } from 'react-qr-reader';
import './output.css';

const PayViaQR = () => {
  const [scannedData, setScannedData] = useState('');
  const [recipientAddress, setRecipientAddress] = useState('');
  const [selectedChain, setSelectedChain] = useState('');
  const [selectedToken, setSelectedToken] = useState('');
  const [amount, setAmount] = useState('');
  const [fee, setFee] = useState(0);
  const [equivalentAmount, setEquivalentAmount] = useState(0);
  const [sourceTokens, setSourceTokens] = useState([]);
  const [destinationTokens, setDestinationTokens] = useState([]);
  const [isScanning, setIsScanning] = useState(true);
  const [isPayButtonEnabled, setIsPayButtonEnabled] = useState(false);

  useEffect(() => {
    const fetchUserBalances = async () => {
      try {
        const response = await fetch('/api/show-balances');
        const data = await response.json();
        setSourceTokens(data.balances.map(b => ({
          chainName: b.network,
          amount: b.amount
        })));
      } catch (error) {
        console.error('Error fetching user balances:', error);
      }
    };

    fetchUserBalances();
  }, []);

  useEffect(() => {
    if (recipientAddress) {
      const fetchDestinationTokens = async () => {
        try {
          const response = await fetch(`/api/get-destination-tokens?recipientAddress=${recipientAddress}`);
          const data = await response.json();
          setDestinationTokens(data.balances.map(b => ({
            chainName: b.network,
            amount: b.amount
          })));
        } catch (error) {
          console.error('Error fetching destination tokens:', error);
        }
      };

      fetchDestinationTokens();
    }
  }, [recipientAddress]);

  useEffect(() => {
    const isValid = selectedChain && selectedToken && amount && recipientAddress && fee && equivalentAmount;
    setIsPayButtonEnabled(isValid);
  }, [selectedChain, selectedToken, amount, recipientAddress, fee, equivalentAmount]);

  const handleScan = (data) => {
    if (data) {
      console.log('Scanned Data:', data);
      setScannedData(data);
      setRecipientAddress(data);
      setIsScanning(false);
    }
  };

  const handleError = (error) => {
    console.error('Scan Error:', error);
  };

  const fetchTransactionFee = async () => {
    try {
      const response = await fetch('/api/get-trans-eqv-fee', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          selectedToken,
          selectedChain,
          amount
        })
      });

      const result = await response.json();
      if (result.fees) {
        setFee(result.fees.transFee);
        setEquivalentAmount(result.fees.eqvFee);
        setIsPayButtonEnabled(true);
      } else {
        alert('Error: ' + result.error);
        setIsPayButtonEnabled(false);
      }
    } catch (error) {
      console.error('Error fetching transaction fee:', error);
      alert('Failed to fetch transaction fee. Please try again.');
      setIsPayButtonEnabled(false);
    }
  };

  const handlePay = async () => {
    try {
      const response = await fetch('/api/pay', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          recipientAddress,
          selectedChain,
          selectedToken,
          amount
        })
      });

      const result = await response.json();
      if (result.success) {
        alert(`Payment successful! Transaction Hash: ${result.transactionHash}`);
      } else {
        alert(`Payment failed: ${result.errorReason}`);
      }
    } catch (error) {
      console.error('Error during payment:', error);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <div className="bg-white shadow-lg rounded-lg p-8 max-w-lg w-full">
        <h1 className="text-4xl font-bold text-center text-indigo-600 mb-8">Pay via QR</h1>
        {isScanning ? (
          <div className="flex justify-center items-center mb-6">
            <div className="w-64 h-64 border-2 border-dashed border-indigo-500 rounded-md flex justify-center items-center">
              <QrReader
                onResult={(result, error) => {
                  if (result) {
                    handleScan(result?.text);
                  }
                  if (error) {
                    handleError(error);
                  }
                }}
                constraints={{ facingMode: "environment" }}
                style={{ width: '250px', height: '250px' }}
                videoContainerStyle={{ width: '250px', height: '250px' }}
              />
            </div>
          </div>
        ) : (
          <div>
            <div className="mb-4">
              <input
                type="text"
                value={recipientAddress}
                onChange={(e) => setRecipientAddress(e.target.value)}
                placeholder="Recipient Address"
                className="w-full p-3 border border-gray-300 rounded-md bg-gray-100 text-gray-700"
                disabled
              />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-semibold text-gray-600 mb-2">Select Source Token</label>
              <select
                value={selectedToken}
                onChange={(e) => setSelectedToken(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="">Select Token</option>
                {sourceTokens.map((token, index) => (
                  <option key={index} value={token.chainName}>
                    {token.chainName} ({token.amount})
                  </option>
                ))}
              </select>
            </div>
            <div className="mb-4">
              <label className="block text-sm font-semibold text-gray-600 mb-2">Select Destination Token</label>
              <select
                value={selectedChain}
                onChange={(e) => setSelectedChain(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="">Select Token</option>
                {destinationTokens.map((token, index) => (
                  <option key={index} value={token.chainName}>
                    {token.chainName} ({token.amount})
                  </option>
                ))}
              </select>
            </div>
            <div className="mb-4">
              <input
                type="number"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="Amount"
                className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            <div className="flex items-center justify-between mb-6">
              <p className="text-sm text-gray-700">Fee: <span className="font-semibold">{fee}</span></p>
              <p className="text-sm text-gray-700">Equivalent Amount: <span className="font-semibold">{equivalentAmount}</span></p>
            </div>
            <div className="flex justify-between">
              <button
                onClick={fetchTransactionFee}
                className="bg-indigo-500 text-white py-3 px-6 rounded-lg shadow hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-400"
                disabled={isPayButtonEnabled}
              >
                Check Fee
              </button>
              <button
                onClick={handlePay}
                className={`py-3 px-6 rounded-lg shadow ${
                  isPayButtonEnabled
                    ? 'bg-green-500 hover:bg-green-600 text-white'
                    : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                } focus:outline-none focus:ring-2 focus:ring-green-400`}
                disabled={!isPayButtonEnabled}
              >
                Send Token
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PayViaQR;
