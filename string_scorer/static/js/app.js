async function fetchData() {
    try {
        const response = await fetch('/data');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
}

function renderGraph(data) {
    const ctx = document.getElementById('scoreGraph').getContext('2d');
    const labels = data.map((entry, index) => `Entry ${index + 1}`);
    const vectaraScores = data.map(entry => entry.scores.vectara);
    const toxicityScores = data.map(entry => entry.scores.toxicity);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Vectara Score',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: vectaraScores,
                fill: false,
            }, {
                label: 'Toxicity Score',
                fill: false,
                backgroundColor: 'rgb(54, 162, 235)',
                borderColor: 'rgb(54, 162, 235)',
                data: toxicityScores,
            }]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Text Scores'
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            }
        }
    });
}

function populateTable(data) {
    const tableBody = document.getElementById('historyTable').getElementsByTagName('tbody')[0];
    data.forEach(entry => {
        let row = tableBody.insertRow();
        let textCell = row.insertCell(0);
        textCell.textContent = entry.text;

        let scoresCell = row.insertCell(1);
        scoresCell.textContent = `Vectara: ${entry.scores.vectara.toFixed(2)}, Toxicity: ${entry.scores.toxicity.toFixed(2)}`;
    });
}

async function fetchDataAndRender() {
    const data = await fetchData();
    if (data) {
        renderGraph(data);
        populateTable(data);
    }
}

// This function call is referenced in the index.html to start fetching data and rendering the components once the DOM is fully loaded.