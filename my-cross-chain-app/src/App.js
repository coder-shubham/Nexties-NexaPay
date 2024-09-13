import logo from './logo.svg';
import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomeScreen from './HomeScreen';
import ShowProfile from './ShowProfile';
import AddWallet from './AddWallet';
import ShowBalances from './ShowBalances';
import PayViaQR from './PayViaQR';
import './output.css';


function App() {
  return (
    <Router>
            <div className="App">
                <Routes>
                    <Route path="/" element={<HomeScreen />} />
                    <Route path="/profile" element={<ShowProfile />} />
                    <Route path="/add-wallet" element={<AddWallet />} />
                    <Route path="/show-balance" element={<ShowBalances />} />
                    <Route path="/pay-via-qr" element={<PayViaQR />} />
                </Routes>
            </div>
        </Router>
  );
}

export default App;
