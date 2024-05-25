import paramiko
import time
from getpass import getpass

username = input('username: ')
password = getpass('password: ')

f = open("ip_list.txt", "r")
for line in f.readlines():
    ip = line.strip()
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh_client.connect(hostname=ip, username=username, password=password, look_for_keys=False)
    print("Successfully connect to ", ip)
    remote_connection = ssh_client.invoke_shell()
    remote_connection.send("config t\n")
    remote_connection.send("router eigrp 1\n")
    remote_connection.send("end\n")
    remote_connection.send("wr mem\n")
    time.sleep(1)
    output = remote_connection.recv(65535)
    print (output.decode("ascii"))

f.close()
ssh_client.close()
