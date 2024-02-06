import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import io from 'socket.io-client';

import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

const socket = io('http://localhost:54321'); // Adjust the URL/port as necessary

const Dashboard = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        socket.on('scoreUpdate', newData => {
            setData(currentData => [...currentData, newData]);
        });

        // Fetch initial data
        fetch('/data')
            .then(response => response.json())
            .then(setData);

        return () => socket.off('scoreUpdate');
    }, []);

    const options = {
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    };

    const chartData = {
        labels: data.map((_, index) => `Entry ${index + 1}`),
        datasets: [
            {
                label: 'Vectara Score',
                data: data.map(entry => entry.scores.vectara),
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
            },
            {
                label: 'Toxicity Score',
                data: data.map(entry => entry.scores.toxicity),
                borderColor: 'rgb(54, 162, 235)',
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
            },
        ],
    };

    return (
        <div>
            <h1>String Scorer Dashboard</h1>
            <div className="dashboard-container">
                <div className="chart-container">
                    <h2>Chart</h2>
                    <Line data={chartData} options={options} />
                </div>
                <div className="history-container">
                    <h2>History</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Text</th>
                                <th>Scores</th>
                            </tr>
                        </thead>
                        <tbody>
                            {data.slice().reverse().map((entry, index) => (
                                <tr key={index}>
                                    <td>{entry.text}</td>
                                    <td>Vectara: {entry.scores.vectara.toFixed(2)}, Toxicity: {entry.scores.toxicity.toFixed(2)}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;

