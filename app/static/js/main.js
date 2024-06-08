function fetchMetrics() {
  fetch('/api/metrics')
      .then(response => response.json())
      .then(data => {
          document.getElementById('cpu-usage').innerText = data.cpu_usage + '%';
          document.getElementById('memory-usage').innerText = data.memory_usage + '%';
          document.getElementById('gpu-usage').innerText = data.gpu_usage + '%';
      })
      .catch(error => console.error('Error fetching metrics:', error));
}

// Fetch metrics every 5 seconds
setInterval(fetchMetrics, 5000);
