import sys
sys.path.append(r"C:\Users\alex-zhao\PycharmProjects\NetDevOps_Demo\demo_code")
from utils import DataWriter
from netmiko import ConnectHandler
import time


cisco_writer = DataWriter()

device_info = {
    "device_type": "cisco_xe",
    "ip" : "192.168.229.4",
    "port" : "22",
    "username" : "cisco",
    "password" : "cisco@123",
}

cmd1 = "show process cpu"
cmd2 = "show processes memory"
cmd3 = "show interfaces summary"
#Initial connect
net_connect = ConnectHandler(**device_info)

def device_1(name):
    print(f"Device - {name} 开始监控！")
    cpu1 = cpu_data
    memory = memory_precent
    g1_drop_tx_ps = g1_drop_tx_data
    g1_drop_rx_ps = g1_drop_rx_data
    g1_tx_bandwidth_utilization = g1_tx_bandwidth_utilization_data
    g1_rx_bandwidth_utilization = g1_rx_bandwidth_utilization_data
    g1_tx_queue = g1_tx_queue_data
    g1_rx_queue = g1_rx_queue_data
    metric_list = [cpu1, memory, g1_drop_tx_ps, g1_drop_rx_ps, g1_tx_bandwidth_utilization, g1_rx_bandwidth_utilization, g1_tx_queue, g1_rx_queue]
    name_list = ['cpu1', 'memory', 'g1_drop_tx_ps', 'g1_drop_rx_ps', 'g1_tx_bandwidth_utilization', 'g1_rx_bandwidth_utilization', 'g1_tx_queue', 'g1_rx_queue']
    for i in range(len(metric_list)):
        cisco_writer.write_ts_data("demo_device", (name_list[i], metric_list[i]))

while True:
    result = net_connect.send_command(cmd1)
    cpu_data = int(result.splitlines()[0].split('CPU utilization for five seconds:')[1].split('%')[0])
    result = net_connect.send_command(cmd2)
    memory_data = int(result.splitlines()[0].split('Used:')[1].split()[0])
    memory_precent = round((memory_data/2121414332)*100)
    result = net_connect.send_command(cmd3)
    g1_drop_tx_data = int(result.splitlines()[10].split("* GigabitEthernet1")[1].split()[3])
    g1_drop_rx_data = int(result.splitlines()[10].split("* GigabitEthernet1")[1].split()[1])
    g1_tx_queue_data = int(result.splitlines()[10].split("* GigabitEthernet1")[1].split()[2])
    g1_rx_queue_data = int(result.splitlines()[10].split("* GigabitEthernet1")[1].split()[0])
    g1_tx_bandwidth_utilization_data = int(result.splitlines()[10].split("* GigabitEthernet1")[1].split()[-1])
    g1_rx_bandwidth_utilization_data = int(result.splitlines()[10].split("* GigabitEthernet1")[1].split()[-2])

    device_1('cisco')
    print(memory_precent)
    time.sleep(10)

