const cpuUsageChart = new Chart(document.getElementById('cpuUsageChart'), {
  type: 'line',
  data: {
      labels: [],
      datasets: [{
          label: 'CPU Usage',
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

const memoryUsageChart = new Chart(document.getElementById('memoryUsageChart'), {
  type: 'line',
  data: {
      labels: [],
      datasets: [{
          label: 'Memory Usage',
          data: [],
          borderColor: 'rgba(153, 102, 255, 1)',
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

const gpuUsageChart = new Chart(document.getElementById('gpuUsageChart'), {
  type: 'line',
  data: {
      labels: [],
      datasets: [{
          label: 'GPU Usage',
          data: [],
          borderColor: 'rgba(255, 159, 64, 1)',
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
          updateChart(cpuUsageChart, now, data.cpu_usage);
          updateChart(memoryUsageChart, now, data.memory_usage);
          updateChart(gpuUsageChart, now, data.gpu_usage);
      })
      .catch(error => console.error('Error fetching metrics:', error));
}

// Fetch metrics every 5 seconds
setInterval(fetchMetrics, 5000);
