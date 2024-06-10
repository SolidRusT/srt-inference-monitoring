def aggregate_cpu_usage(data):
    cpu_idle_keys = [key for key in data.keys() if 'node_cpu_seconds_total' in key and 'idle' in key]
    cpu_total_keys = [key for key in data.keys() if 'node_cpu_seconds_total' in key]

    cpu_idle_time = sum(data[key] for key in cpu_idle_keys)
    cpu_total_time = sum(data[key] for key in cpu_total_keys)

    if cpu_total_time == 0:
        return 0

    cpu_usage_percentage = 100 * (1 - (cpu_idle_time / cpu_total_time))
    return cpu_usage_percentage

def aggregate_disk_usage(data):
    disk_total_keys = [key for key in data.keys() if 'node_filesystem_size_bytes' in key]
    disk_free_keys = [key for key in data.keys() if 'node_filesystem_avail_bytes' in key]

    disk_total = sum(data[key] for key in disk_total_keys)
    disk_free = sum(data[key] for key in disk_free_keys)

    if disk_total == 0:
        return 0

    disk_usage_percentage = 100 * ((disk_total - disk_free) / disk_total)
    return disk_usage_percentage

def aggregate_network_io(data, interface='eno1'):
    network_receive_key = f'node_network_receive_bytes_total{{device="{interface}"}}'
    network_transmit_key = f'node_network_transmit_bytes_total{{device="{interface}"}}'

    if network_receive_key not in data or network_transmit_key not in data:
        return 0

    network_receive = data[network_receive_key]
    network_transmit = data[network_transmit_key]

    # Assuming a maximum bandwidth of 1Gbps (adjust according to your network capabilities)
    max_bandwidth = 1 * 10**9  # 1 Gbps in bytes per second

    network_utilization_percentage = 100 * ((network_receive + network_transmit) / max_bandwidth)
    return network_utilization_percentage
