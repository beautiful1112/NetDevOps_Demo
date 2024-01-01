from connection import Net


class VRP8(Net):
    def __init__(self):
        super().__init__('huawei', '192.168.1.100', 'huawei', 'huawei@123')

    # 获取配置
    ## 输出字符串形式的设备配置
    def get_config(self):
        cmd = 'display cur'
        info = self.device.send_command(cmd)
        data_str = info.split('platform console serial\n!')[1]
        return data_str

    # 获取接口
    ## 输出列表形式的接口数据
    def get_interfaces(self):
        cmd = 'display ip interface brief'
        info = self.device.send_command(cmd)
        data_list = []
        for line in info.split('\n')[1:]:
            line_list = line.split()
            if_name = line_list[0]
            if_ip = line_list[1]
            status = line_list[-1]
            data_list.append({'name': if_name,
                              'ip': if_ip,
                              'status': status})
        return data_list