import datetime
from cisco import IOS_XE_17
from huawei import VRP8

# The device name, alarm type, and alarm description are used to obtain an HTML version of the email body
def create_mail_body(device_name, alert_type, alert_description):
    now_time = str(datetime.datetime.now()).split('.')[0]
    with open('template/head.html', encoding='utf-8') as f:
        text_head = f.read()
    with open('template/body.html', encoding='utf-8') as f:
        text_body = f.read()
    body = text_head + "\n" + text_body.format(device_name, alert_type, alert_description, now_time)
    return body


def cisco_runner():
    device_name = 'CiscoIOSXE'
    ios_xe = IOS_XE_17()

    # Task1. Obtain information to generate JSON data
    cisco_data = {}
    cisco_data['config'] = ios_xe.get_config()
    cisco_data['interfaces'] = ios_xe.get_interfaces()
    cisco_data['routeTable'] = ios_xe.get_route()
    cisco_data['monitor'] = {'cpu': ios_xe.monitor()}

    # Task2. Recovering and checking the interface
    for interface in cisco_data['interfaces']:
        if interface['status'] != 'up':
            # Create an email body and send alarms
            alert_des = f"{device_name} 的接口 {interface['name']} 被关闭了"
            body = create_mail_body(device_name, 'Error', alert_des)
            ios_xe.send_mail(subject='设备接口故障', body=body)

            # Start interface recovery
            ios_xe.recover_interface(interface['name'])
            cisco_data['interfaces'] = ios_xe.get_interfaces()
            print("接口已恢复")

    # Task3. Configure a new route
    dst = '172.16.10.0'
    mask = '255.255.255.0'
    next = '10.1.1.100'
    if dst not in cisco_data['routeTable']:
        ios_xe.post_route(dst, mask, next)
        cisco_data['routeTable'] = ios_xe.get_route()
        print(f'新增了一条路由指向 {dst}，数据已更新')

    # Task4. Generate JSON
    ios_xe.to_json(cisco_data, 'data/cisco.json')

    ios_xe.device.disconnect()

def huawei_runner():
    device_name = "huawei_vrpv8"
    ce12800 = VRP8()

    huawei_data = {}
    huawei_data['config'] = ce12800.get_config()
    huawei_data['interfaces'] = ce12800.get_interfaces()
    huawei_data['routeTable'] = ce12800.get_route()
    huawei_data['monitor'] = {'cpu': ce12800.monitor()}

    # Task2. Recovering and checking the interface
    for interface in huawei_data['interfaces']:
        if interface['Physical'] != 'up':
            # Create an email body and send alarms
            alert_des = f"{device_name} 的接口 {interface['name']} 被关闭了"
            body = create_mail_body(device_name, 'Error', alert_des)
            ce12800.send_mail(subject='设备接口故障', body=body)

            # Start interface recovery
            ce12800.recover_interface(interface['name'])
            huawei_data['interfaces'] = ce12800.get_interfaces()
            print("接口已恢复")

            # Task3. Configure a new route
            dst = '172.16.10.0'
            mask = '255.255.255.0'
            next = '10.1.1.100'
            if dst not in huawei_data['routeTable']:
                ce12800.post_route(dst, mask, next)
            huawei_data['routeTable'] = ce12800.get_route()
            print(f'新增了一条路由指向 {dst}，数据已更新')

            # Task4. Generate JSON
            ce12800.to_json(huawei_data, 'data/huawei.json')

            ce12800.device.disconnect()

huawei_runner()
