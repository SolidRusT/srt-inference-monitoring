document.addEventListener('DOMContentLoaded', function () {
  const cpuChartCtx = document.getElementById('cpuChart').getContext('2d');
  const memoryChartCtx = document.getElementById('memoryChart').getContext('2d');
  const gpuChartCtx = document.getElementById('gpuChart').getContext('2d');
  const diskChartCtx = document.getElementById('diskChart').getContext('2d');
  const networkChartCtx = document.getElementById('networkChart').getContext('2d');

  const cpuChart = new Chart(cpuChartCtx, {
      type: 'bar',
      data: {
          labels: [],
          datasets: [{
              label: 'CPU Usage',
              backgroundColor: 'rgba(54, 162, 235, 0.2)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1,
              data: []
          }]
      },
      options: {
          responsive: true,
          scales: {
              y: {
                  beginAtZero: true,
                  ticks: {
                      callback: function(value) {
                          return value + '%';
                      }
                  }
              }
          }
      }
  });

  const memoryChart = new Chart(memoryChartCtx, {
      type: 'bar',
      data: {
          labels: [],
          datasets: [{
              label: 'Memory Usage',
              backgroundColor: 'rgba(153, 102, 255, 0.2)',
              borderColor: 'rgba(153, 102, 255, 1)',
              borderWidth: 1,
              data: []
          }]
      },
      options: {
          responsive: true,
          scales: {
              y: {
                  beginAtZero: true
              }
          }
      }
  });

  const gpuChart = new Chart(gpuChartCtx, {
      type: 'bar',
      data: {
          labels: [],
          datasets: [{
              label: 'GPU Usage',
              backgroundColor: 'rgba(255, 159, 64, 0.2)',
              borderColor: 'rgba(255, 159, 64, 1)',
              borderWidth: 1,
              data: []
          }]
      },
      options: {
          responsive: true,
          scales: {
              y: {
                  beginAtZero: true,
                  ticks: {
                      callback: function(value) {
                          return value + '%';
                      }
                  }
              }
          }
      }
  });

  const diskChart = new Chart(diskChartCtx, {
      type: 'bar',
      data: {
          labels: [],
          datasets: [{
              label: 'Disk Usage',
              backgroundColor: 'rgba(255, 206, 86, 0.2)',
              borderColor: 'rgba(255, 206, 86, 1)',
              borderWidth: 1,
              data: []
          }]
      },
      options: {
          responsive: true,
          scales: {
              y: {
                  beginAtZero: true,
                  ticks: {
                      callback: function(value) {
                          return value + '%';
                      }
                  }
              }
          }
      }
  });

  const networkChart = new Chart(networkChartCtx, {
      type: 'bar',
      data: {
          labels: [],
          datasets: [{
              label: 'Network I/O',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1,
              data: []
          }]
      },
      options: {
          responsive: true,
          scales: {
              y: {
                  beginAtZero: true
              }
          }
      }
  });

  function updateCharts() {
      fetch('/metrics')
          .then(response => response.json())
          .then(data => {
              console.log('Metrics data:', data); // Debugging information
              const labels = Object.keys(data);
              const cpuUsage = labels.map(label => data[label].cpu_usage);
              const memoryUsage = labels.map(label => data[label].memory_usage);
              const gpuUsage = labels.map(label => data[label].gpu_usage);
              const diskUsage = labels.map(label => data[label].disk_usage);
              const networkIo = labels.map(label => data[label].network_io);

              cpuChart.data.labels = labels;
              cpuChart.data.datasets[0].data = cpuUsage;
              cpuChart.update();

              memoryChart.data.labels = labels;
              memoryChart.data.datasets[0].data = memoryUsage;
              memoryChart.update();

              gpuChart.data.labels = labels;
              gpuChart.data.datasets[0].data = gpuUsage;
              gpuChart.update();

              diskChart.data.labels = labels;
              diskChart.data.datasets[0].data = diskUsage;
              diskChart.update();

              networkChart.data.labels = labels;
              networkChart.data.datasets[0].data = networkIo;
              networkChart.update();
          })
          .catch(error => console.error('Error fetching metrics:', error)); // Debugging information
  }

  updateCharts();
  setInterval(updateCharts, 30000);
});
