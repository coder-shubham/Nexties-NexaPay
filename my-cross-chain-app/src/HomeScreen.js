import React from 'react';
import { useNavigate } from 'react-router-dom';

const HomeScreen = () => {
    const navigate = useNavigate();

    return (
        <div style={styles.container}>
            <h1 style={styles.title}>NexaPay</h1>
            <div style={styles.buttonContainer}>
                <button style={styles.button} onClick={() => navigate('/profile')}>Show Profile</button>
                <button style={styles.button} onClick={() => navigate('/pay-via-qr')}>Pay via QR</button>
                <button style={styles.button} onClick={() => navigate('/add-wallet')}>Add Wallet</button>
                <button style={styles.button} onClick={() => navigate('/show-balance')}>Show Balances/Transactions</button>
            </div>
        </div>
    );
};

const styles = {
    container: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        backgroundColor: '#f4f6f9',
        fontFamily: "'Roboto', sans-serif",
    },
    title: {
        fontSize: '48px',
        fontWeight: 'bold',
        color: '#2c3e50',
        marginBottom: '40px',
    },
    buttonContainer: {
        display: 'flex',
        justifyContent: 'center',
        flexWrap: 'wrap',
        gap: '20px', // Adds space between buttons
    },
    button: {
        backgroundColor: '#3498db',
        color: '#fff',
        padding: '15px 30px',
        fontSize: '18px',
        fontWeight: 'bold',
        border: 'none',
        borderRadius: '8px',
        cursor: 'pointer',
        transition: 'background-color 0.3s ease',
        boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
    },
    buttonHover: {
        backgroundColor: '#2980b9',
    },
};

export default HomeScreen;
