import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './output.css';

const ShowProfile = () => {
  const navigate = useNavigate();
  const [userInfo, setUserInfo] = useState(null);

  useEffect(() => {
    fetch('/api/show-profile')
      .then((res) => res.json())
      .then((data) => setUserInfo(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <div className="bg-white shadow-lg rounded-lg p-8 max-w-md w-full">
        {userInfo ? (
          <div className="text-center">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              {userInfo.name}
            </h2>
            <p className="text-sm text-gray-600 mb-6">
              EVM Address: <span className="font-mono">{userInfo.evmAddress}</span>
            </p>
            <div className="flex justify-center mb-6">
              <img
                src={userInfo.qrCode}
                alt="User QR Code"
                className="w-48 h-48 object-contain border border-gray-300 rounded-md"
              />
            </div>
            <button
              onClick={() => navigate('/')}
              className="mt-4 bg-indigo-500 text-white py-2 px-4 rounded-lg shadow hover:bg-indigo-600 transition duration-300"
            >
              Go Back
            </button>
          </div>
        ) : (
          <div className="text-center">
            <p className="text-gray-600">Loading...</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ShowProfile;
