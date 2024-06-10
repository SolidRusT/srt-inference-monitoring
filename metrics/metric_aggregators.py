def aggregate_cpu_usage(data):
    cpu_keys = [key for key in data.keys() if 'node_cpu_seconds_total' in key]
    cpu_usage = sum(data[key] for key in cpu_keys)
    return cpu_usage

def aggregate_disk_usage(data):
    disk_keys = [key for key in data.keys() if 'node_filesystem_avail_bytes' in key]
    disk_usage = sum(data[key] for key in disk_keys)
    return disk_usage

def aggregate_network_io(data):
    network_receive_keys = [key for key in data.keys() if 'node_network_receive_bytes_total' in key]
    network_transmit_keys = [key for key in data.keys() if 'node_network_transmit_bytes_total' in key]
    network_io = sum(data[key] for key in network_receive_keys + network_transmit_keys)
    return network_io
