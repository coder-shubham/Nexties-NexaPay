import React, { useEffect, useState } from 'react';

const ShowBalances = () => {
    const [balances, setBalances] = useState([]);
    const [transactions, setTransactions] = useState([]);

    useEffect(() => {
        fetch('/api/show-balances')
            .then(res => res.json())
            .then(data => setBalances(data.balances))
            .catch(err => console.error(err));

        fetch('/api/show-transactions')
            .then(res => res.json())
            .then(data => setTransactions(data.transactions))
            .catch(err => console.error(err));
    }, []);

    return (
        <div style={styles.container}>
            <h2 style={styles.header}>User Balances</h2>
            <table style={styles.table}>
                <thead>
                    <tr>
                        <th style={styles.th}>Network</th>
                        <th style={styles.th}>Balance</th>
                    </tr>
                </thead>
                <tbody>
                    {balances.map((balance, index) => (
                        <tr key={index}>
                            <td style={styles.td}>{balance.network}</td>
                            <td style={styles.td}>{balance.amount}</td>
                        </tr>
                    ))}
                </tbody>
            </table>

            <h2 style={{ ...styles.header, marginTop: '40px' }}>Transaction History</h2>
            <table style={styles.table}>
                <thead>
                    <tr>
                        <th style={styles.th}>Date</th>
                        <th style={styles.th}>Status</th>
                        <th style={styles.th}>Sent Amount</th>
                        <th style={styles.th}>Sent Token</th>
                        <th style={styles.th}>Destination Token</th>
                        <th style={styles.th}>Recipient Address</th>
                        <th style={styles.th}>Transaction Hash</th>
                    </tr>
                </thead>
                <tbody>
                    {transactions.map((tx, index) => (
                        <tr key={index}>
                            <td style={styles.td}>{new Date(tx.dateTime).toLocaleString() || 'Invalid Date'}</td>
                            <td style={styles.td}>{tx.status}</td>
                            <td style={styles.td}>{tx.sentAmount}</td>
                            <td style={styles.td}>{tx.sentToken}</td>
                            <td style={styles.td}>{tx.destinationToken}</td>
                            <td style={styles.td}>{tx.recipientAddress}</td>
                            <td style={styles.td}>
                                <a href={`https://sepolia.etherscan.io/tx/${tx.txnHash}`} style={styles.link} target="_blank" rel="noopener noreferrer">
                                    {tx.txnHash}
                                </a>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

const styles = {
    container: {
        fontFamily: '"Arial", sans-serif',
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '20px',
        backgroundColor: '#f9f9f9',
        borderRadius: '8px',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    },
    header: {
        textAlign: 'center',
        fontSize: '24px',
        fontWeight: 'bold',
        color: '#333',
        marginBottom: '20px',
    },
    table: {
        width: '100%',
        borderCollapse: 'collapse',
        backgroundColor: '#fff',
        border: '1px solid #ddd',
    },
    th: {
        padding: '12px',
        border: '1px solid #ddd',
        backgroundColor: '#f1f1f1',
        color: '#333',
        textAlign: 'left',
    },
    td: {
        padding: '12px',
        border: '1px solid #ddd',
        color: '#333',
        textAlign: 'left',
    },
    tdHash: {
        padding: '12px',
        border: '1px solid #ddd',
        color: '#333',
        textAlign: 'left',
        wordWrap: 'break-word',  // Added word wrap
        wordBreak: 'break-all',  // Added word break
    },
    link: {
        color: '#3498db',
        textDecoration: 'none',
    },
};


export default ShowBalances;
