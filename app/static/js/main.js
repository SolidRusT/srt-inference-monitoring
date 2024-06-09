const charts = {};

function createChart(server, metric) {
    const ctx = document.getElementById(`${server}-${metric}`).getContext('2d');
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: `${server} ${metric}`,
                data: [],
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill: false
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

function updateChart(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
}

function fetchMetrics() {
    fetch('/api/metrics')
        .then(response => response.json())
        .then(data => {
            const now = new Date().toLocaleTimeString();
            for (const server in data) {
                for (const metric in data[server]) {
                    if (!charts[`${server}-${metric}`]) {
                        charts[`${server}-${metric}`] = createChart(server, metric);
                    }
                    updateChart(charts[`${server}-${metric}`], now, data[server][metric]);
                }
            }
        })
        .catch(error => console.error('Error fetching metrics:', error));
}

// Fetch metrics every 5 seconds
setInterval(fetchMetrics, 5000);
