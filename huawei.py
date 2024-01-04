from connection import Net


class VRP8(Net):
    def __init__(self):
        super().__init__('huawei_vrpv8', '192.168.229.10', 'huawei', 'Yestar@123')

    # 获取配置
    ## 输出字符串形式的设备配置
    def get_config(self):
        cmd = 'display current-configuration'
        info = self.device.send_command(cmd)
        return info

    # 获取接口
    ## 输出列表形式的接口数据
    def get_interfaces(self):
        cmd = 'display ip interface brief'
        info = self.device.send_command(cmd)
        data_list = []
        for line in info.splitlines()[11:]:
            line_list = line.split()
            if_name = line_list[0]
            if_ip = line_list[1]
            status = line_list[2]
            protocol = line_list[3]
            data_list.append({'name': if_name,
                              'ip': if_ip,
                              ' Physical': status,
                              'Protocol':protocol})
        return data_list
        # 接口恢复UP
    def recover_interface(self, if_name):
        #self.reconnect()
        cmd_list = [f'interface {if_name}', 'undo shutdown', 'commit']
        self.device.send_config_set(cmd_list)

    # 获取路由表
    ## 输出字符串形式的设备路由表信息
    def get_route(self):
        cmd = 'display ip routing-table'
        info = self.device.send_command(cmd)
        data_str = '\n'.join([line for line in info.split('\n') if '/' in line])
        return data_str

    # 新增路由条目
    def post_route(self, dst_n, mask, next):
        self.reconnect()
        cmd_list = [f'ip route-static {dst_n} {mask} {next}', 'commit']
        self.device.send_config_set(cmd_list)

    # 自动化巡检
    ## 输出字典形式的CPU使用率数据
    def monitor(self):
        cpu_cmd = 'display cpu'
        cpu_info = self.device.send_command(cpu_cmd)
        line = cpu_info.splitlines()
        cpu_list = []
        for cpu_data in line:
            if cpu_data.startswith('cpu0'):
                cpu_list.append(cpu_data)
            if cpu_data.startswith('cpu1'):
                cpu_list.append(cpu_data)

        data_dict = {'cpu1_current': cpu_list[0].split()[1],
                     'cpu2_current': cpu_list[1].split()[1],
                     'cpu1_5s': cpu_list[0].split()[2],
                     'cpu2_5s': cpu_list[1].split()[2]}
        return data_dict